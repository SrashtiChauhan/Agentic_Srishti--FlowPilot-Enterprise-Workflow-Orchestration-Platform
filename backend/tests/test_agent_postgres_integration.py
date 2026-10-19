
import unittest
import uuid

from sqlalchemy.orm import Session

from backend.database.database import engine
from backend.database.models.agent import AgentDB


class AgentPostgresIntegrationTests(unittest.TestCase):
    def test_agent_create_read_update_delete_persists(self):
        agent_id = str(uuid.uuid4())
        unique_name = f"Persistence Test {agent_id[:8]}"

        agent_data = {
            "id": agent_id,
            "name": unique_name,
            "description": "Temporary PostgreSQL integration test",
            "provider": "ollama",
            "model_name": "gemma3:4b",
            "system_prompt": "You are a temporary test agent.",
            "temperature": 0.2,
            "tool_bindings": [],
            "risk_score": "low",
        }

        try:
            with Session(engine) as db:
                agent = AgentDB(**agent_data)
                db.add(agent)
                db.commit()

            # Verify that the new record can be read in a new session.
            with Session(engine) as db:
                saved = db.get(AgentDB, agent_id)
                self.assertIsNotNone(saved)
                self.assertEqual(saved.name, unique_name)
                self.assertEqual(saved.provider, "ollama")

                saved.name = f"{unique_name} Updated"
                saved.risk_score = "medium"
                db.commit()

            # Verify that the update persisted in PostgreSQL.
            with Session(engine) as db:
                updated = db.get(AgentDB, agent_id)
                self.assertIsNotNone(updated)
                self.assertEqual(updated.name, f"{unique_name} Updated")
                self.assertEqual(updated.risk_score, "medium")

                db.delete(updated)
                db.commit()

            # Verify that deletion persisted.
            with Session(engine) as db:
                self.assertIsNone(db.get(AgentDB, agent_id))

        finally:
            # Cleanup only this test's uniquely generated record.
            with Session(engine) as db:
                remaining = db.get(AgentDB, agent_id)
                if remaining is not None:
                    db.delete(remaining)
                    db.commit()


if __name__ == "__main__":
    unittest.main()
