"""Scan MCP server manifests into a capability index."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Sequence


def load_servers(path: str) -> List[Dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        payload = payload.get("servers", [payload])
    return [item for item in payload if isinstance(item, dict)]


def index_servers(path: str) -> Dict[str, Any]:
    servers = load_servers(path)
    capability_index: Dict[str, List[str]] = {}
    risky = []
    for server in servers:
        name = str(server.get("name") or server.get("id") or "unknown")
        capabilities = server.get("capabilities") or server.get("tools") or []
        if isinstance(capabilities, dict):
            capabilities = list(capabilities)
        for capability in capabilities:
            capability_index.setdefault(str(capability), []).append(name)
        scopes = " ".join(str(item).lower() for item in server.get("scopes", []))
        if any(term in scopes for term in ["write", "admin", "delete", "filesystem"]):
            risky.append(name)
    return {"server_count": len(servers), "capabilities": capability_index, "risk_review": sorted(set(risky))}


def format_text(index: Dict[str, Any]) -> str:
    lines = [f"Servers: {index['server_count']}", "", "Capabilities:"]
    for capability, servers in sorted(index["capabilities"].items()):
        lines.append(f"- {capability}: {', '.join(sorted(servers))}")
    lines.extend(["", "Needs risk review:"])
    lines.extend(f"- {name}" for name in index["risk_review"]) if index["risk_review"] else lines.append("- none")
    return "\n".join(lines)


def run(input_path: str, output_format: str = "text") -> str:
    index = index_servers(input_path)
    if output_format == "json":
        return json.dumps(index, indent=2, sort_keys=True)
    return format_text(index)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scan MCP server manifests into a capability index.")
    parser.add_argument("input", help="JSON file with servers")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(run(args.input, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
