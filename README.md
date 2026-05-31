# MCP Server Radar

Scan MCP server manifests, registry exports, and awesome-list style JSON into a capability and risk index.

For agent builders choosing MCP servers before wiring them into Codex, Claude Code, Cursor, Copilot, or a custom runtime.

```bash
PYTHONPATH=src python3 -m mcp_server_radar examples/registry-items.json --format markdown
```

## Why

MCP server lists are growing quickly, but a star count does not tell you whether a server needs tokens, file access, network access, write permissions, or delete/admin capabilities.

MCP Server Radar is a local-first scanner for comparing capability, transport, auth, and risk before installing a server into an agent harness.

## Install

```bash
git clone https://github.com/alexzhu0/mcp-server-radar.git
cd mcp-server-radar
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Quickstart

```bash
PYTHONPATH=src python3 -m mcp_server_radar examples/registry-items.json --format markdown
```

## Examples

Human-readable output:

```bash
PYTHONPATH=src python3 -m mcp_server_radar examples/servers.json --format markdown
```

Registry or awesome-list style input:

```bash
PYTHONPATH=src python3 -m mcp_server_radar examples/registry-items.json --format markdown
```

Machine-readable output:

```bash
PYTHONPATH=src python3 -m mcp_server_radar examples/servers.json --format json
```

## CLI Reference

- `PYTHONPATH=src python3 -m mcp_server_radar --help`
- Main demo: `PYTHONPATH=src python3 -m mcp_server_radar examples/registry-items.json --format markdown`
- CI gate: `PYTHONPATH=src python3 -m unittest discover -s tests`

## Features

- Capability indexing
- Transport and auth summary
- Risk category tagging
- Risk score per server
- Registry/list shapes: `servers`, `items`, `repositories`, and `mcpServers`
- Capability inference from tags, categories, keywords, and descriptions
- Text, Markdown, and JSON output
- Simple manifest shape for examples and CI

## API

The public Python surface is intentionally small:

```python
from mcp_server_radar.cli import index_servers
```

Use the CLI first. Import the Python functions when you want to embed the same behavior in a larger tool.

## Why Star This

Star this if you want a fast local way to compare MCP servers by capability and risk before installing them.

## Related Tools

- Use `agent-skill-lint` after choosing MCP tools for an agent skill.
- Use `context-window-doctor` when a long MCP/tool instruction file starts to rot.
- Use `agent-runbook-kit` to generate the release checklist for an MCP-powered agent repo.

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## FAQ

**Does this call external AI APIs?**

No. The current release uses the Python standard library only.

**Is this production-ready?**

Treat this as a focused utility. Run it in CI or local review first, then adapt thresholds and examples to your workflow.

**Can I contribute examples?**

Yes. The most useful issue or pull request includes a real input file, expected output, and the workflow where it helps.

## Contributing

Issues and pull requests are welcome when they include a concrete use case or failing example.

Run tests before opening a pull request:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## License

MIT
