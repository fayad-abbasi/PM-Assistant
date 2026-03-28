"""Slack MCP tools for PM Assistant."""

from slack_client import SlackClient

client = SlackClient()


async def search_messages(query: str, count: int = 10) -> dict:
    """Search Slack messages across channels.

    Use for: finding stakeholder discussions, past decisions, context for meetings.
    Requires user token (SLACK_USER_TOKEN).

    Args:
        query: Search query (supports Slack search modifiers like from:, in:, has:)
        count: Max results to return (default 10)
    """
    result = await client.search_messages(query=query, count=count)
    if not result.get("ok"):
        return {"error": result.get("error", "Unknown error")}
    messages = result.get("messages", {}).get("matches", [])
    return {
        "total": result.get("messages", {}).get("total", 0),
        "messages": [
            {
                "text": m.get("text", ""),
                "user": m.get("username", m.get("user", "")),
                "channel": m.get("channel", {}).get("name", ""),
                "timestamp": m.get("ts", ""),
                "permalink": m.get("permalink", ""),
            }
            for m in messages
        ],
    }


async def post_message(
    channel: str, text: str, thread_ts: str | None = None
) -> dict:
    """Post a message to a Slack channel or thread.

    Use for: sharing status updates, decisions, asking stakeholders questions.
    IMPORTANT: Always confirm with the user before posting.

    Args:
        channel: Channel ID or name (e.g., #product-team)
        text: Message text (supports Slack markdown)
        thread_ts: Optional thread timestamp to reply in a thread
    """
    result = await client.post_message(
        channel=channel, text=text, thread_ts=thread_ts
    )
    if not result.get("ok"):
        return {"error": result.get("error", "Unknown error")}
    return {
        "ok": True,
        "channel": result.get("channel", ""),
        "ts": result.get("ts", ""),
    }


async def get_channel_history(
    channel: str, limit: int = 20, oldest: str | None = None
) -> dict:
    """Get recent messages from a Slack channel.

    Use for: catching up on channel activity, finding recent discussions.

    Args:
        channel: Channel ID
        limit: Max messages to return (default 20)
        oldest: Only return messages after this timestamp
    """
    result = await client.get_channel_history(
        channel=channel, limit=limit, oldest=oldest
    )
    if not result.get("ok"):
        return {"error": result.get("error", "Unknown error")}
    return {
        "messages": [
            {
                "text": m.get("text", ""),
                "user": m.get("user", ""),
                "timestamp": m.get("ts", ""),
                "thread_ts": m.get("thread_ts"),
                "reply_count": m.get("reply_count", 0),
            }
            for m in result.get("messages", [])
        ]
    }


async def list_channels(limit: int = 100) -> dict:
    """List available Slack channels.

    Args:
        limit: Max channels to return (default 100)
    """
    result = await client.list_channels(limit=limit)
    if not result.get("ok"):
        return {"error": result.get("error", "Unknown error")}
    return {
        "channels": [
            {
                "id": c.get("id", ""),
                "name": c.get("name", ""),
                "purpose": c.get("purpose", {}).get("value", ""),
                "num_members": c.get("num_members", 0),
            }
            for c in result.get("channels", [])
        ]
    }


async def get_thread(channel: str, thread_ts: str, limit: int = 50) -> dict:
    """Get all replies in a Slack thread.

    Use for: reading full discussions, extracting decisions and action items.

    Args:
        channel: Channel ID
        thread_ts: Timestamp of the parent message
        limit: Max replies to return (default 50)
    """
    result = await client.get_thread_replies(
        channel=channel, thread_ts=thread_ts, limit=limit
    )
    if not result.get("ok"):
        return {"error": result.get("error", "Unknown error")}
    return {
        "messages": [
            {
                "text": m.get("text", ""),
                "user": m.get("user", ""),
                "timestamp": m.get("ts", ""),
            }
            for m in result.get("messages", [])
        ]
    }
