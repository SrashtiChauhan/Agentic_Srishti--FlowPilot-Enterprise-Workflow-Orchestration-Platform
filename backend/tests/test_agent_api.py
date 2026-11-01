
import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from backend.main import app
from backend.database.database import get_db
from backend.database.models.agent import AgentDB


VALID_AGENT = {
    "name": "Test Agent",
    "description": "Agent API test",
    "provider": "ollama",
    "model_name": "gemma3:4b",
    "system_prompt": "You are a helpful assistant.",
    "temperature": 0.2,
    "tool_bindings": [],
    "risk_score": "low",
}


class AgentAPITests(unittest.TestCase):
    def setUp(self):
        self.database = MagicMock()

        def override_get_db():
            yield self.database

        app.dependency_overrides[get_db] = override_get_db
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()
        app.dependency_overrides.clear()

    def test_create_agent_returns_saved_agent(self):
        response = self.client.post("/agents/", json=VALID_AGENT)

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["message"], "Agent created successfully")
        self.assertEqual(body["agent"]["name"], VALID_AGENT["name"])
        self.assertEqual(body["agent"]["provider"], "ollama")
        self.assertTrue(body["agent"]["id"])

        self.database.add.assert_called_once()
        self.database.commit.assert_called_once()
        self.database.refresh.assert_called_once()

    def test_list_agents_returns_agents(self):
        agent = AgentDB(id="agent-123", **VALID_AGENT)
        self.database.query.return_value.order_by.return_value.all.return_value = [
            agent
        ]

        response = self.client.get("/agents/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["agents"]), 1)
        self.assertEqual(
            response.json()["agents"][0]["id"],
            "agent-123",
        )

    def test_get_agent_returns_existing_agent(self):
        agent = AgentDB(id="agent-123", **VALID_AGENT)
        self.database.query.return_value.filter.return_value.first.return_value = (
            agent
        )

        response = self.client.get("/agents/agent-123")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], "agent-123")
        self.assertEqual(response.json()["name"], VALID_AGENT["name"])

    def test_get_missing_agent_returns_404(self):
        self.database.query.return_value.filter.return_value.first.return_value = (
            None
        )

        response = self.client.get("/agents/missing-agent")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Agent not found")

    def test_update_agent_changes_existing_agent(self):
        agent = AgentDB(id="agent-123", **VALID_AGENT)
        self.database.query.return_value.filter.return_value.first.return_value = (
            agent
        )

        updated_data = {
            **VALID_AGENT,
            "name": "Updated Agent",
            "risk_score": "medium",
        }

        response = self.client.put(
            "/agents/agent-123",
            json=updated_data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["agent"]["name"],
            "Updated Agent",
        )
        self.assertEqual(
            response.json()["agent"]["risk_score"],
            "medium",
        )
        self.database.commit.assert_called_once()
        self.database.refresh.assert_called_once()

    def test_update_missing_agent_returns_404(self):
        self.database.query.return_value.filter.return_value.first.return_value = (
            None
        )

        response = self.client.put(
            "/agents/missing-agent",
            json=VALID_AGENT,
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_agent_removes_existing_agent(self):
        agent = AgentDB(id="agent-123", **VALID_AGENT)
        self.database.query.return_value.filter.return_value.first.return_value = (
            agent
        )

        response = self.client.delete("/agents/agent-123")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["message"],
            "Agent deleted successfully",
        )
        self.database.delete.assert_called_once_with(agent)
        self.database.commit.assert_called_once()

    def test_delete_missing_agent_returns_404(self):
        self.database.query.return_value.filter.return_value.first.return_value = (
            None
        )

        response = self.client.delete("/agents/missing-agent")

        self.assertEqual(response.status_code, 404)

    def test_invalid_temperature_is_rejected(self):
        invalid_agent = {**VALID_AGENT, "temperature": 2.0}

        response = self.client.post("/agents/", json=invalid_agent)

        self.assertEqual(response.status_code, 422)
        self.database.add.assert_not_called()
        self.database.commit.assert_not_called()

    def test_invalid_risk_score_is_rejected(self):
        invalid_agent = {**VALID_AGENT, "risk_score": "extreme"}

        response = self.client.post("/agents/", json=invalid_agent)

        self.assertEqual(response.status_code, 422)
        self.database.add.assert_not_called()
        self.database.commit.assert_not_called()


    def test_create_agent_rejects_unknown_tool_ids(self):
        invalid_agent = {
            **VALID_AGENT,
            "tool_bindings": ["unknown_tool"],
        }

        response = self.client.post("/agents/", json=invalid_agent)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()["detail"]["unknown_tool_ids"],
            ["unknown_tool"],
        )
        self.database.add.assert_not_called()
        self.database.commit.assert_not_called()

    def test_update_agent_rejects_unknown_tool_ids(self):
        agent = AgentDB(id="agent-123", **VALID_AGENT)
        self.database.query.return_value.filter.return_value.first.return_value = (
            agent
        )

        invalid_agent = {
            **VALID_AGENT,
            "tool_bindings": ["unknown_tool"],
        }

        response = self.client.put(
            "/agents/agent-123",
            json=invalid_agent,
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()["detail"]["unknown_tool_ids"],
            ["unknown_tool"],
        )
        self.database.commit.assert_not_called()


if __name__ == "__main__":
    unittest.main()
