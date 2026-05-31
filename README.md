# Mcp Server Radar

Scan MCP server manifests into a searchable capability index.

## Why

MCP server lists are hard to compare by capability, transport, and risk.

This repository is intentionally small: it should be useful in one command, easy to inspect, and simple to fork.

## Install

```bash
git clone https://github.com/alexzhu0/mcp-server-radar.git
cd mcp-server-radar
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Quickstart

```bash
PYTHONPATH=src python3 -m mcp_server_radar examples/servers.json
```

## Examples

```bash
PYTHONPATH=src python3 -m mcp_server_radar examples/servers.json
```

## API

The first release is CLI-first. Public Python APIs can be added after real usage proves the right shape.

## FAQ

**Does this call external AI APIs?**

No. The generated starter uses the Python standard library only.

**Is this production-ready?**

Treat `v0.1.0` as a focused utility release. Pin versions and review output before adding it to CI.

## Contributing

Issues and pull requests are welcome when they include a concrete use case or failing example.

## License

MIT
