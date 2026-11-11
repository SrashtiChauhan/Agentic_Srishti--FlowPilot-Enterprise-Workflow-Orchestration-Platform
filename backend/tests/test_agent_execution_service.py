
import unittest
from unittest.mock import MagicMock, patch

from backend.services.agent_execution_service import (
    AgentExecutionError,
    execute_agent,
    execute_agent_with_tools,
)
from backend.services.tool_execution_service import ToolExecutionError


class TestAgentExecutionService(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()

    def test_missing_agent_is_rejected(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with self.assertRaisesRegex(AgentExecutionError, "Agent not found"):
            execute_agent("missing-agent", "Hello", self.db)

    def test_unsupported_provider_is_rejected(self):
        agent = MagicMock()
        agent.provider = "huggingface"

        self.db.query.return_value.filter.return_value.first.return_value = agent

        with self.assertRaisesRegex(
            AgentExecutionError,
            "not implemented yet",
        ):
            execute_agent("agent-123", "Hello", self.db)

    def test_missing_model_is_rejected(self):
        agent = MagicMock()
        agent.provider = "ollama"
        agent.model_name = "  "

        self.db.query.return_value.filter.return_value.first.return_value = agent

        with self.assertRaisesRegex(
            AgentExecutionError,
            "model configured",
        ):
            execute_agent("agent-123", "Hello", self.db)

    @patch("backend.services.agent_execution_service.generate_response")
    def test_successful_agent_execution(self, mock_generate):
        agent = MagicMock()
        agent.id = "agent-123"
        agent.name = "Test Agent"
        agent.provider = "ollama"
        agent.tool_bindings = []
        agent.model_name = "gemma3:4b"
        agent.system_prompt = "You are a helpful assistant."
        agent.temperature = 0.2

        self.db.query.return_value.filter.return_value.first.return_value = agent
        mock_generate.return_value = "Hello from FlowPilot!"

        result = execute_agent("agent-123", "Say hello", self.db)

        self.assertEqual(result["agent_id"], "agent-123")
        self.assertEqual(result["agent_name"], "Test Agent")
        self.assertEqual(result["model_name"], "gemma3:4b")
        self.assertEqual(result["output"], "Hello from FlowPilot!")

        mock_generate.assert_called_once_with(
            model_name="gemma3:4b",
            system_prompt="You are a helpful assistant.",
            user_input="Say hello",
            temperature=0.2,
        )

    @patch("backend.services.agent_execution_service.generate_response")
    def test_model_failure_is_wrapped(self, mock_generate):
        agent = MagicMock()
        agent.provider = "ollama"
        agent.tool_bindings = []
        agent.model_name = "gemma3:4b"
        agent.system_prompt = "You are helpful."
        agent.temperature = 0.2

        self.db.query.return_value.filter.return_value.first.return_value = agent
        mock_generate.side_effect = RuntimeError("Ollama is unavailable")

        with self.assertRaisesRegex(
            AgentExecutionError,
            "Ollama is unavailable",
        ):
            execute_agent("agent-123", "Hello", self.db)


    
    @patch("backend.services.agent_execution_service.execute_tool")
    @patch("backend.services.agent_execution_service.chat_with_ollama")
    def test_agent_executes_authorized_tool_and_returns_final_response(
        self,
        mock_chat,
        mock_execute_tool,
    ):
        agent = MagicMock()
        agent.id = "agent-123"
        agent.name = "Security Agent"
        agent.provider = "ollama"
        agent.model_name = "qwen3:4b"
        agent.system_prompt = "You are a security assistant."
        agent.temperature = 0.2
        agent.tool_bindings = ["ip_reputation"]

        self.db.query.return_value.filter.return_value.first.return_value = agent

        mock_chat.side_effect = [
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "id": "call-123",
                        "function": {
                            "name": "ip_reputation",
                            "arguments": {"ip_address": "8.8.8.8"},
                        },
                    }
                ],
            },
            {
                "role": "assistant",
                "content": "The IP has a low simulated risk score of 10.",
            },
        ]

        mock_execute_tool.return_value = {
            "ip_address": "8.8.8.8",
            "risk_level": "low",
            "score": 10,
        }

        result = execute_agent("agent-123", "Investigate 8.8.8.8", self.db)

        self.assertEqual(
            result["output"],
            "The IP has a low simulated risk score of 10.",
        )

        mock_execute_tool.assert_called_once_with(
            tool_id="ip_reputation",
            arguments={"ip_address": "8.8.8.8"},
            allowed_tool_ids=["ip_reputation"],
        )

        self.assertEqual(mock_chat.call_count, 2)

        second_call_messages = mock_chat.call_args_list[1].kwargs["messages"]

        self.assertEqual(second_call_messages[-1]["role"], "tool")
        self.assertEqual(second_call_messages[-1]["tool_name"], "ip_reputation")


    
    @patch("backend.services.agent_execution_service.chat_with_ollama")
    def test_unimplemented_selected_tool_is_rejected(self, mock_chat):
        agent = MagicMock()
        agent.tool_bindings = ["aws_api"]
        agent.model_name = "qwen3:4b"

        with self.assertRaisesRegex(
            AgentExecutionError,
            "not executable yet",
        ):
            execute_agent_with_tools(agent, "Inspect an AWS resource")

        mock_chat.assert_not_called()

    @patch("backend.services.agent_execution_service.execute_tool")
    @patch("backend.services.agent_execution_service.chat_with_ollama")
    def test_unauthorized_model_tool_request_is_rejected(
        self,
        mock_chat,
        mock_execute_tool,
    ):
        agent = MagicMock()
        agent.tool_bindings = ["ip_reputation"]
        agent.model_name = "qwen3:4b"
        agent.system_prompt = "You are a security assistant."
        agent.temperature = 0.2

        mock_chat.return_value = {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "id": "call-456",
                    "function": {
                        "name": "aws_api",
                        "arguments": {
                            "operation": "inspect_resource",
                            "resource_id": "test-resource",
                        },
                    },
                }
            ],
        }

        mock_execute_tool.side_effect = ToolExecutionError(
            "Agent is not authorized to use tool 'aws_api'."
        )

        with self.assertRaisesRegex(
            AgentExecutionError,
            "not authorized",
        ):
            execute_agent_with_tools(agent, "Inspect this resource")

        mock_execute_tool.assert_called_once()

    @patch("backend.services.agent_execution_service.chat_with_ollama")
    def test_tool_call_round_limit_is_enforced(self, mock_chat):
        agent = MagicMock()
        agent.tool_bindings = ["ip_reputation"]
        agent.model_name = "qwen3:4b"
        agent.system_prompt = "You are a security assistant."
        agent.temperature = 0.2

        mock_chat.return_value = {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "id": "call-repeat",
                    "function": {
                        "name": "ip_reputation",
                        "arguments": {"ip_address": "8.8.8.8"},
                    },
                }
            ],
        }

        with patch(
            "backend.services.agent_execution_service.execute_tool",
            return_value={
                "ip_address": "8.8.8.8",
                "risk_level": "low",
                "score": 10,
            },
        ):
            with self.assertRaisesRegex(
                AgentExecutionError,
                "maximum number of tool-call rounds",
            ):
                execute_agent_with_tools(agent, "Investigate this IP")

        self.assertEqual(mock_chat.call_count, 4)




if __name__ == "__main__":
    unittest.main()
