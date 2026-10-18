
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.main import app
from backend.database.database import get_db
from backend.routes.workflows import router


class FakeWorkflow:
    def __init__(self, workflow_id="workflow-123"):
        self.id = workflow_id
        self.nodes = []
        self.edges = []


class FakeResult:
    def __init__(self, workflow):
        self.workflow = workflow

    def scalar_one_or_none(self):
        return self.workflow


class FakeDatabase:
    def __init__(self, workflow=None):
        self.workflow = workflow

    def execute(self, statement):
        return FakeResult(self.workflow)


class WorkflowAPITests(unittest.TestCase):
    def setUp(self):
        self.workflow = FakeWorkflow()
        self.database = FakeDatabase(self.workflow)

        def override_get_db():
            yield self.database

        app.dependency_overrides[get_db] = override_get_db
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()
        app.dependency_overrides.clear()

    @patch("backend.routes.workflows.execute_workflow")
    def test_run_workflow_returns_success(self, mock_execute):
        mock_execute.return_value = {
            "status": "completed",
            "outputs": {"trigger-1": "Hello"},
            "final_output": "Hello",
        }

        response = self.client.post(
            "/workflows/workflow-123/run",
            json={"initial_input": "Hello"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "completed")
        mock_execute.assert_called_once()

    def test_missing_workflow_returns_404(self):
        self.database.workflow = None

        response = self.client.post(
            "/workflows/missing-workflow/run",
            json={"initial_input": "Hello"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Workflow not found.")

    @patch("backend.routes.workflows.execute_workflow")
    def test_execution_error_returns_422(self, mock_execute):
        from backend.services.workflow_execution_service import (
            WorkflowExecutionError,
        )

        mock_execute.side_effect = WorkflowExecutionError(
            "Workflow contains disconnected nodes."
        )

        response = self.client.post(
            "/workflows/workflow-123/run",
            json={"initial_input": "Hello"},
        )

        self.assertEqual(response.status_code, 422)
        self.assertIn("disconnected", response.json()["detail"])

    def test_empty_input_returns_422(self):
        response = self.client.post(
            "/workflows/workflow-123/run",
            json={"initial_input": ""},
        )

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
