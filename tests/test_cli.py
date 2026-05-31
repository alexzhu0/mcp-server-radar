import json
import tempfile
import unittest
from pathlib import Path

from mcp_server_radar.cli import format_markdown, index_servers, run


class McpServerRadarTests(unittest.TestCase):
    def test_indexes_capabilities_and_risk(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "servers.json"
            path.write_text(json.dumps({"servers": [{"name": "fs", "capabilities": ["read"], "scopes": ["filesystem-write"]}]}), encoding="utf-8")
            index = index_servers(str(path))
        self.assertEqual(index["capabilities"]["read"], ["fs"])
        self.assertEqual(index["risk_review"], ["fs"])
        self.assertEqual(index["servers"][0]["risk_categories"], ["filesystem", "write"])

    def test_text_output_lists_server_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "servers.json"
            path.write_text('[{"name":"search","tools":["web-search"]}]', encoding="utf-8")
            output = run(str(path))
        self.assertIn("Servers: 1", output)
        self.assertIn("web-search", output)

    def test_markdown_output_contains_transport_and_auth(self):
        index = {
            "server_count": 1,
            "servers": [
                {
                    "name": "github",
                    "transport": "stdio",
                    "auth": "token",
                    "capabilities": ["issues"],
                    "risk_categories": ["write"],
                }
            ],
        }

        output = format_markdown(index)

        self.assertIn("| Server | Transport | Auth |", output)
        self.assertIn("| github | stdio | token | issues | write |", output)

    def test_run_markdown_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "servers.json"
            path.write_text('[{"name":"fs","transport":"stdio","auth":"none","tools":["read"],"scopes":["filesystem-write"]}]', encoding="utf-8")

            output = run(str(path), "markdown")

        self.assertIn("filesystem, write", output)


if __name__ == "__main__":
    unittest.main()
