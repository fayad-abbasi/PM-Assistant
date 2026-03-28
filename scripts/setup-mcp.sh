#!/usr/bin/env bash
# setup-mcp.sh — Configure MCP servers
# Run: bash scripts/setup-mcp.sh

set -euo pipefail

echo "Setting up MCP servers..."

for server_dir in mcp-servers/*/; do
  if [ -f "$server_dir/pyproject.toml" ]; then
    echo "Installing dependencies for $server_dir..."
    (cd "$server_dir" && uv sync)
  fi
done

echo "Done. Make sure .env is configured with your API tokens."
