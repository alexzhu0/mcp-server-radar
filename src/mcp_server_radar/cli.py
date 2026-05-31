"""Scan MCP server manifests into a capability index."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Sequence


RISK_CATEGORIES = {
    "filesystem": ["filesystem", "file", "path"],
    "write": ["write", "create", "update"],
    "admin": ["admin", "root", "sudo"],
    "delete": ["delete", "remove", "destroy"],
    "network": ["network", "http", "web"],
    "secret": ["secret", "token", "api key", "apikey", "credential"],
}


def load_servers(path: str) -> List[Dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        for key in ("servers", "items", "repositories", "mcpServers"):
            if isinstance(payload.get(key), list):
                payload = payload[key]
                break
        else:
            payload = [payload]
    return [item for item in payload if isinstance(item, dict)]


def listify(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, dict):
        return [str(key) for key in value]
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def infer_capabilities(server: Dict[str, Any]) -> List[str]:
    capabilities: List[str] = []
    for key in ("capabilities", "tools", "tags", "categories", "keywords"):
        capabilities.extend(listify(server.get(key)))
    description = str(server.get("description") or "").lower()
    for term in ("filesystem", "github", "database", "browser", "memory", "search", "slack"):
        if term in description:
            capabilities.append(term)
    return sorted(set(capabilities))


def infer_risk_categories(server: Dict[str, Any], capabilities: Sequence[str]) -> List[str]:
    haystack = " ".join(
        str(item).lower()
        for item in (
            listify(server.get("scopes"))
            + listify(server.get("permissions"))
            + listify(server.get("auth"))
            + listify(server.get("authentication"))
            + listify(server.get("description"))
            + listify(server.get("url"))
            + list(capabilities)
        )
    )
    risk_categories = []
    for category, terms in RISK_CATEGORIES.items():
        if any(term in haystack for term in terms):
            risk_categories.append(category)
    return sorted(set(risk_categories))


def index_servers(path: str) -> Dict[str, Any]:
    servers = load_servers(path)
    capability_index: Dict[str, List[str]] = {}
    server_rows = []
    risky = []
    for server in servers:
        name = str(server.get("name") or server.get("id") or server.get("repo") or server.get("full_name") or "unknown")
        capabilities = infer_capabilities(server)
        for capability in capabilities:
            capability_index.setdefault(capability, []).append(name)
        risk_categories = infer_risk_categories(server, capabilities)
        if risk_categories:
            risky.append(name)
        server_rows.append(
            {
                "name": name,
                "transport": str(server.get("transport") or server.get("protocol") or "unknown"),
                "auth": str(server.get("auth") or server.get("authentication") or "unknown"),
                "url": str(server.get("url") or server.get("repo_url") or server.get("html_url") or ""),
                "capabilities": sorted(capabilities),
                "risk_categories": sorted(set(risk_categories)),
                "risk_score": len(set(risk_categories)),
            }
        )
    return {
        "server_count": len(servers),
        "servers": server_rows,
        "capabilities": capability_index,
        "risk_review": sorted(set(risky)),
    }


def format_text(index: Dict[str, Any]) -> str:
    lines = [f"Servers: {index['server_count']}", "", "Capabilities:"]
    for capability, servers in sorted(index["capabilities"].items()):
        lines.append(f"- {capability}: {', '.join(sorted(servers))}")
    lines.extend(["", "Needs risk review:"])
    lines.extend(f"- {name}" for name in index["risk_review"]) if index["risk_review"] else lines.append("- none")
    return "\n".join(lines)


def format_markdown(index: Dict[str, Any]) -> str:
    lines = [
        "# MCP Server Radar",
        "",
        f"Servers: {index['server_count']}",
        "",
        "| Server | Transport | Auth | Capabilities | Risk | Score |",
        "| --- | --- | --- | --- | --- | ---: |",
    ]
    for server in index["servers"]:
        lines.append(
            "| {name} | {transport} | {auth} | {capabilities} | {risk} | {score} |".format(
                name=server["name"],
                transport=server["transport"],
                auth=server["auth"],
                capabilities=", ".join(server["capabilities"]) or "-",
                risk=", ".join(server["risk_categories"]) or "none",
                score=server["risk_score"],
            )
        )
    return "\n".join(lines)


def run(input_path: str, output_format: str = "text") -> str:
    index = index_servers(input_path)
    if output_format == "json":
        return json.dumps(index, indent=2, sort_keys=True)
    if output_format == "markdown":
        return format_markdown(index)
    return format_text(index)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scan MCP server manifests into a capability index.")
    parser.add_argument("input", help="JSON file with servers")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(run(args.input, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
