"""Async Slack API client using httpx."""

import httpx
from config import SLACK_BOT_TOKEN, SLACK_USER_TOKEN, SLACK_BASE_URL


class SlackClient:
    """Async client for Slack Web API."""

    def __init__(self):
        self.bot_token = SLACK_BOT_TOKEN
        self.user_token = SLACK_USER_TOKEN
        self.base_url = SLACK_BASE_URL

    def _headers(self, use_user_token: bool = False) -> dict:
        token = self.user_token if use_user_token else self.bot_token
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        }

    async def search_messages(
        self, query: str, count: int = 10, sort: str = "timestamp"
    ) -> dict:
        """Search messages across channels (requires user token)."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/search.messages",
                headers=self._headers(use_user_token=True),
                params={"query": query, "count": count, "sort": sort},
            )
            resp.raise_for_status()
            return resp.json()

    async def post_message(
        self, channel: str, text: str, thread_ts: str | None = None
    ) -> dict:
        """Post a message to a channel or thread."""
        payload = {"channel": channel, "text": text}
        if thread_ts:
            payload["thread_ts"] = thread_ts
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/chat.postMessage",
                headers=self._headers(),
                json=payload,
            )
            resp.raise_for_status()
            return resp.json()

    async def get_channel_history(
        self, channel: str, limit: int = 20, oldest: str | None = None
    ) -> dict:
        """Get recent messages from a channel."""
        params = {"channel": channel, "limit": limit}
        if oldest:
            params["oldest"] = oldest
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/conversations.history",
                headers=self._headers(),
                params=params,
            )
            resp.raise_for_status()
            return resp.json()

    async def list_channels(self, limit: int = 100) -> dict:
        """List public channels."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/conversations.list",
                headers=self._headers(),
                params={"limit": limit, "types": "public_channel,private_channel"},
            )
            resp.raise_for_status()
            return resp.json()

    async def get_user_info(self, user_id: str) -> dict:
        """Get user profile information."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/users.info",
                headers=self._headers(),
                params={"user": user_id},
            )
            resp.raise_for_status()
            return resp.json()

    async def add_reaction(
        self, channel: str, timestamp: str, name: str
    ) -> dict:
        """Add a reaction to a message."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/reactions.add",
                headers=self._headers(),
                json={"channel": channel, "timestamp": timestamp, "name": name},
            )
            resp.raise_for_status()
            return resp.json()

    async def get_thread_replies(
        self, channel: str, thread_ts: str, limit: int = 50
    ) -> dict:
        """Get replies in a thread."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/conversations.replies",
                headers=self._headers(),
                params={"channel": channel, "ts": thread_ts, "limit": limit},
            )
            resp.raise_for_status()
            return resp.json()
