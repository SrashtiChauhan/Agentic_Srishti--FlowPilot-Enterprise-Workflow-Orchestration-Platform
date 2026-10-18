
import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException

from backend.routes.workflows import run_workflow
from backend.schemas.workflow import WorkflowRunRequest
from backend.services.workflow_execution_service import WorkflowExecutionError


class TestRunWorkflowEndpoint(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.request = WorkflowRunRequest(
            initial_input="Summarize this support ticket."
        )

    def test_missing_workflow_returns_404(self):
        self.db.execute.return_value.scalar_one_or_none.return_value = None

        with self.assertRaises(HTTPException) as context:
            run_workflow(
                workflow_id="missing-workflow",
                request=self.request,
                db=self.db,
            )

        self.assertEqual(context.exception.status_code, 404)

    @patch("backend.routes.workflows.execute_workflow")
    def test_valid_workflow_executes(self, mock_execute):
        workflow = MagicMock()
        workflow.nodes = [{"id": "trigger", "type": "trigger"}]
        workflow.edges = []

        self.db.execute.return_value.scalar_one_or_none.return_value = workflow
        mock_execute.return_value = {
            "status": "completed",
            "final_output": "Ticket summary",
            "outputs": {},
        }

        result = run_workflow(
            workflow_id="workflow-123",
            request=self.request,
            db=self.db,
        )

        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["final_output"], "Ticket summary")

        mock_execute.assert_called_once_with(
            nodes=workflow.nodes,
            edges=workflow.edges,
            db=self.db,
            initial_input="Summarize this support ticket.",
        )

    @patch("backend.routes.workflows.execute_workflow")
    def test_execution_error_returns_422(self, mock_execute):
        workflow = MagicMock()
        workflow.nodes = []
        workflow.edges = []

        self.db.execute.return_value.scalar_one_or_none.return_value = workflow
        mock_execute.side_effect = WorkflowExecutionError(
            "Cannot execute an empty workflow."
        )

        with self.assertRaises(HTTPException) as context:
            run_workflow(
                workflow_id="workflow-123",
                request=self.request,
                db=self.db,
            )

        self.assertEqual(context.exception.status_code, 422)
        self.assertIn("empty workflow", context.exception.detail)


if __name__ == "__main__":
    unittest.main()
