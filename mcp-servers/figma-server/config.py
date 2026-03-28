"""Configuration for the Figma MCP server.

Reads FIGMA_ACCESS_TOKEN from environment variables. Validates at import
time so the server fails fast with a clear message rather than producing
cryptic errors on first API call.
"""

import os


class FigmaConfigError(Exception):
    """Raised when required Figma configuration is missing."""


def _require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise FigmaConfigError(
            f"Environment variable {name} is not set. "
            f"Add it to your .env file or set it in .claude/settings.json "
            f"under mcpServers.figma.env."
        )
    return value


# Required
FIGMA_ACCESS_TOKEN: str = _require_env("FIGMA_ACCESS_TOKEN")

# Figma REST API base URL
FIGMA_API_BASE: str = "https://api.figma.com/v1"
