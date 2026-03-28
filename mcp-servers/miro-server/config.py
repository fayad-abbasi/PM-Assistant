"""Configuration for the Miro MCP server."""

import os

from dotenv import load_dotenv

load_dotenv()

MIRO_API_BASE = "https://api.miro.com/v2"

MIRO_ACCESS_TOKEN: str = os.environ.get("MIRO_ACCESS_TOKEN", "")

if not MIRO_ACCESS_TOKEN:
    raise EnvironmentError(
        "MIRO_ACCESS_TOKEN is not set. "
        "Add it to your .env file or export it as an environment variable."
    )
