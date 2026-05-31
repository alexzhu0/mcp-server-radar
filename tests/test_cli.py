import json
import tempfile
import unittest
from pathlib import Path

from mcp_server_radar.cli import index_servers, run


class McpServerRadarTests(unittest.TestCase):
    def test_indexes_capabilities_and_risk(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "servers.json"
            path.write_text(json.dumps({"servers": [{"name": "fs", "capabilities": ["read"], "scopes": ["filesystem-write"]}]}), encoding="utf-8")
            index = index_servers(str(path))
        self.assertEqual(index["capabilities"]["read"], ["fs"])
        self.assertEqual(index["risk_review"], ["fs"])

    def test_text_output_lists_server_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "servers.json"
            path.write_text('[{"name":"search","tools":["web-search"]}]', encoding="utf-8")
            output = run(str(path))
        self.assertIn("Servers: 1", output)
        self.assertIn("web-search", output)


if __name__ == "__main__":
    unittest.main()
