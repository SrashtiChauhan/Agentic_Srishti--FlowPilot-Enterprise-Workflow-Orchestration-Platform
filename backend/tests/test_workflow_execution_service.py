
import unittest

from backend.services.workflow_execution_service import (
    prepare_workflow_execution,
)
from backend.services.workflow_engine import WorkflowValidationError


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


if __name__ == "__main__":
    unittest.main()
