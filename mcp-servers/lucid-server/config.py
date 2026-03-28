"""Configuration for the Lucid MCP server.

Reads the API token from environment variables. Validates it is set at
import time so the server fails fast with a clear message.
"""

import os

from dotenv import load_dotenv

load_dotenv()

LUCID_API_BASE = "https://api.lucid.co/v1"

LUCID_API_TOKEN: str = os.environ.get("LUCID_API_TOKEN", "")

if not LUCID_API_TOKEN:
    raise EnvironmentError(
        "LUCID_API_TOKEN is not set. "
        "Add it to your .env file or export it as an environment variable."
    )
