import unittest

from backend.services.tool_execution_service import (
    ToolExecutionError,
    execute_tool,
)


class TestToolExecutionService(unittest.TestCase):

    def test_valid_ip_execution(self):
        result = execute_tool(
            "ip_reputation",
            {"ip_address": "8.8.8.8"},
            ["ip_reputation"],
        )

        self.assertEqual(result["ip_address"], "8.8.8.8")
        self.assertEqual(result["risk_level"], "low")
        self.assertEqual(result["score"], 10)
        self.assertEqual(result["mode"], "simulated")

    def test_invalid_ip_is_rejected(self):
        with self.assertRaisesRegex(
            ToolExecutionError,
            "valid IPv4 or IPv6",
        ):
            execute_tool(
                "ip_reputation",
                {"ip_address": "999.999.999.999"},
                ["ip_reputation"],
            )

    def test_unauthorized_tool_is_rejected(self):
        with self.assertRaisesRegex(
            ToolExecutionError,
            "not authorized",
        ):
            execute_tool(
                "ip_reputation",
                {"ip_address": "8.8.8.8"},
                ["siem_search"],
            )

    def test_unknown_tool_is_rejected(self):
        with self.assertRaisesRegex(
            ToolExecutionError,
            "not registered",
        ):
            execute_tool(
                "unknown_tool",
                {},
                ["unknown_tool"],
            )

    def test_missing_argument_is_rejected(self):
        with self.assertRaisesRegex(
            ToolExecutionError,
            "ip_address",
        ):
            execute_tool(
                "ip_reputation",
                {},
                ["ip_reputation"],
            )

    def test_extra_argument_is_rejected(self):
        with self.assertRaisesRegex(
            ToolExecutionError,
            "only the 'ip_address'",
        ):
            execute_tool(
                "ip_reputation",
                {
                    "ip_address": "8.8.8.8",
                    "extra": "unexpected",
                },
                ["ip_reputation"],
            )


if __name__ == "__main__":
    unittest.main()