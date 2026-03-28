"""Slack MCP server configuration."""

import os


SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
SLACK_USER_TOKEN = os.environ.get("SLACK_USER_TOKEN", "")
SLACK_BASE_URL = "https://slack.com/api"

# Required bot token scopes:
# - channels:read, channels:history (read public channels)
# - groups:read, groups:history (read private channels)
# - im:read, im:history (read DMs)
# - chat:write (post messages)
# - search:read (search messages) — requires user token
# - users:read (resolve user names)
# - reactions:write (add reactions)
# - files:read (read shared files)
