# MCP Server Radar

Scan MCP server manifests into a searchable capability index.

## Why

MCP server lists are hard to compare by capability, transport, auth, and risk surface.

This is a baseline HighStar AI developer tool: dependency-light, local-first, and built around one quick command.

## Install

```bash
git clone https://github.com/alexzhu0/mcp-server-radar.git
cd mcp-server-radar
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Quickstart

```bash
PYTHONPATH=src python3 -m mcp_server_radar examples/servers.json --format markdown
```

## Examples

Human-readable output:

```bash
PYTHONPATH=src python3 -m mcp_server_radar examples/servers.json --format markdown
```

Machine-readable output:

```bash
PYTHONPATH=src python3 -m mcp_server_radar examples/servers.json --format json
```

## CLI Reference

- `PYTHONPATH=src python3 -m mcp_server_radar --help`
- Main demo: `PYTHONPATH=src python3 -m mcp_server_radar examples/servers.json --format markdown`
- CI gate: `PYTHONPATH=src python3 -m unittest discover -s tests`

## Features

- Capability indexing
- Transport and auth summary
- Risk category tagging
- Text, Markdown, and JSON output
- Simple manifest shape for examples and CI

## API

The public Python surface is intentionally small:

```python
from mcp_server_radar.cli import index_servers
```

Use the CLI first. Import the Python functions when you want to embed the same behavior in a larger tool.

## Why Star This

It helps agent builders compare MCP options before wiring them into a runtime.

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
