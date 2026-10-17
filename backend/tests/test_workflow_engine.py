
import unittest

from backend.services.workflow_engine import (
    WorkflowValidationError,
    get_execution_order,
)


class TestWorkflowEngine(unittest.TestCase):
    def test_valid_linear_workflow(self):
        nodes = [
            {"id": "trigger"},
            {"id": "agent"},
            {"id": "action"},
        ]
        edges = [
            {"source": "trigger", "target": "agent"},
            {"source": "agent", "target": "action"},
        ]

        result = get_execution_order(nodes, edges)

        self.assertEqual(
            result,
            ["trigger", "agent", "action"],
        )

    def test_missing_node_reference(self):
        nodes = [{"id": "trigger"}]
        edges = [
            {"source": "trigger", "target": "missing"}
        ]

        with self.assertRaises(WorkflowValidationError):
            get_execution_order(nodes, edges)

    def test_cycle_is_rejected(self):
        nodes = [
            {"id": "a"},
            {"id": "b"},
            {"id": "c"},
        ]
        edges = [
            {"source": "a", "target": "b"},
            {"source": "b", "target": "c"},
            {"source": "c", "target": "a"},
        ]

        with self.assertRaises(WorkflowValidationError):
            get_execution_order(nodes, edges)

    def test_self_connection_is_rejected(self):
        nodes = [{"id": "a"}]
        edges = [{"source": "a", "target": "a"}]

        with self.assertRaises(WorkflowValidationError):
            get_execution_order(nodes, edges)

    def test_duplicate_node_ids_are_rejected(self):
        nodes = [{"id": "a"}, {"id": "a"}]

        with self.assertRaises(WorkflowValidationError):
            get_execution_order(nodes, [])

    def test_duplicate_edges_are_rejected(self):
        nodes = [{"id": "a"}, {"id": "b"}]
        edges = [
            {"source": "a", "target": "b"},
            {"source": "a", "target": "b"},
        ]

        with self.assertRaises(WorkflowValidationError):
            get_execution_order(nodes, edges)


if __name__ == "__main__":
    unittest.main()
