"""Configuration for the Jira MCP server.

Reads connection settings from environment variables. Required vars are
validated at import time so the server fails fast with a clear message
rather than producing cryptic errors on first API call.
"""

import os


class JiraConfigError(Exception):
    """Raised when required Jira configuration is missing."""


def _require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise JiraConfigError(
            f"Environment variable {name} is not set. "
            f"Add it to your .env file or set it in .claude/settings.json "
            f"under mcpServers.jira.env."
        )
    return value


# Required
JIRA_BASE_URL: str = _require_env("JIRA_BASE_URL").rstrip("/")
JIRA_EMAIL: str = _require_env("JIRA_EMAIL")
JIRA_API_TOKEN: str = _require_env("JIRA_API_TOKEN")

# Optional — can be overridden per tool call
JIRA_PROJECT_KEY: str = os.environ.get("JIRA_PROJECT_KEY", "").strip() or None

# Derived
JIRA_API_BASE: str = f"{JIRA_BASE_URL}/rest/api/3"
