
import unittest
from unittest.mock import MagicMock, patch

from backend.services.agent_execution_service import (
    AgentExecutionError,
    execute_agent,
)


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


if __name__ == "__main__":
    unittest.main()
