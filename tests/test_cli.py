import json
import tempfile
import unittest
from pathlib import Path

from mcp_server_radar.cli import format_markdown, index_servers, load_servers, run


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
                    "url": "",
                    "capabilities": ["issues"],
                    "risk_categories": ["write"],
                    "risk_score": 1,
                }
            ],
        }

        output = format_markdown(index)

        self.assertIn("| Server | Transport | Auth |", output)
        self.assertIn("| github | stdio | token | issues | write | 1 |", output)

    def test_run_markdown_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "servers.json"
            path.write_text('[{"name":"fs","transport":"stdio","auth":"none","tools":["read"],"scopes":["filesystem-write"]}]', encoding="utf-8")

            output = run(str(path), "markdown")

        self.assertIn("filesystem, write", output)

    def test_loads_registry_items_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "registry.json"
            path.write_text(json.dumps({"items": [{"name": "memory", "tags": ["memory"]}]}), encoding="utf-8")

            servers = load_servers(str(path))

        self.assertEqual(servers[0]["name"], "memory")

    def test_infers_risk_from_auth_url_and_description(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "servers.json"
            path.write_text(
                json.dumps(
                    {
                        "items": [
                            {
                                "repo": "github-mcp",
                                "url": "https://example.com",
                                "auth": "token",
                                "description": "GitHub issue writer over HTTP",
                                "tags": ["issues"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            index = index_servers(str(path))

        self.assertEqual(index["servers"][0]["name"], "github-mcp")
        self.assertIn("network", index["servers"][0]["risk_categories"])
        self.assertIn("secret", index["servers"][0]["risk_categories"])
        self.assertIn("write", index["servers"][0]["risk_categories"])


if __name__ == "__main__":
    unittest.main()
