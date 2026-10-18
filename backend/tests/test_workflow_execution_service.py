import unittest
from unittest.mock import MagicMock, patch

from backend.services.workflow_engine import WorkflowValidationError
from backend.services.workflow_execution_service import (
    WorkflowExecutionError,
    execute_workflow,
    prepare_workflow_execution,
)

class TestPrepareWorkflowExecution(unittest.TestCase):
    def test_nodes_are_returned_in_execution_order(self):
        nodes = [
            {
                "id": "action",
                "type": "action",
                "title": "Send Notification",
            },
            {
                "id": "trigger",
                "type": "trigger",
                "title": "Manual Trigger",
            },
            {
                "id": "agent",
                "type": "agent",
                "title": "AI Agent",
            },
        ]

        edges = [
            {"source": "trigger", "target": "agent"},
            {"source": "agent", "target": "action"},
        ]

        result = prepare_workflow_execution(nodes, edges)

        self.assertEqual(
            [node["id"] for node in result],
            ["trigger", "agent", "action"],
        )

        # The complete node configuration must be preserved.
        self.assertEqual(result[1]["title"], "AI Agent")
        self.assertEqual(result[2]["type"], "action")

    def test_invalid_workflow_is_rejected(self):
        nodes = [
            {"id": "trigger", "type": "trigger"},
        ]

        edges = [
            {"source": "trigger", "target": "missing"},
        ]

        with self.assertRaises(WorkflowValidationError):
            prepare_workflow_execution(nodes, edges)

    
   
    @patch("backend.services.workflow_execution_service.execute_agent")
    def test_trigger_and_agent_execute_successfully(self, mock_execute_agent):
        nodes = [
            {
                "id": "trigger",
                "type": "trigger",
                "config": {},
            },
            {
                "id": "agent",
                "type": "agent",
                "config": {"agentId": "agent-123"},
            },
        ]
        edges = [
            {"source": "trigger", "target": "agent"},
        ]

        mock_execute_agent.return_value = {
            "agent_id": "agent-123",
            "agent_name": "Test Agent",
            "model_name": "gemma3:4b",
            "output": "Hello from the agent!",
        }

        db = MagicMock()

        result = execute_workflow(
            nodes=nodes,
            edges=edges,
            db=db,
            initial_input="Say hello",
        )

        self.assertEqual(result["status"], "completed")
        self.assertEqual(
            result["outputs"]["trigger"]["output"],
            "Say hello",
        )
        self.assertEqual(
            result["outputs"]["agent"]["output"],
            "Hello from the agent!",
        )
        self.assertEqual(
            result["final_output"],
            "Hello from the agent!",
        )

        mock_execute_agent.assert_called_once_with(
            agent_id="agent-123",
            user_input="Say hello",
            db=db,
        )


    def test_agent_node_without_agent_id_is_rejected(self):
        nodes = [
            {
                "id": "trigger",
                "type": "trigger",
                "config": {},
            },
            {
                "id": "agent",
                "type": "agent",
                "config": {},
            },
        ]
        edges = [
            {"source": "trigger", "target": "agent"},
        ]

        with self.assertRaisesRegex(
            WorkflowExecutionError,
            "no configured agentId",
        ):
            execute_workflow(
                nodes=nodes,
                edges=edges,
                db=MagicMock(),
                initial_input="Hello",
            )

    def test_unsupported_node_type_is_rejected(self):
        nodes = [
            {
                "id": "trigger",
                "type": "trigger",
                "config": {},
            },
            {
                "id": "action",
                "type": "action",
                "config": {},
            },
        ]
        edges = [
            {"source": "trigger", "target": "action"},
        ]

        with self.assertRaisesRegex(
            WorkflowExecutionError,
            "unsupported type",
        ):
            execute_workflow(
                nodes=nodes,
                edges=edges,
                db=MagicMock(),
                initial_input="Hello",
            )



if __name__ == "__main__":
    unittest.main()
