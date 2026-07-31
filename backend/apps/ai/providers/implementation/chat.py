"""
Concrete OpenAI-compatible chat model implementation.
"""

from __future__ import annotations

import os

from apps.datavionos.ai.chat import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    ChatRole,
)
from apps.datavionos.ai.exceptions import ChatModelError


class OpenAIChatModel:
    """
    Chat model backed by an OpenAI-compatible API.

    Falls back to a deterministic local echo when no ``OPENAI_API_KEY`` is
    configured so the system remains usable in offline/development
    environments.
    """

    def __init__(
        self,
        *,
        model: str = "gpt-4o-mini",
        api_key: str | None = None,
        base_url: str | None = None,
        max_retries: int = 2,
    ) -> None:
        self._model = model
        self._api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self._base_url = base_url or os.environ.get("OPENAI_BASE_URL")
        self._max_retries = max_retries

    @property
    def model(self) -> str:
        """Return the configured model name."""

        return self._model

    async def complete(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """Generate a chat completion."""

        if not self._api_key:
            return self._offline_complete(request)

        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(
                api_key=self._api_key,
                base_url=self._base_url,
            )

            response = await client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": message.role.value,
                        "content": message.content,
                    }
                    for message in request.messages
                ],
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )

            choice = response.choices[0]
            return ChatResponse(
                message=ChatMessage(
                    role=ChatRole.ASSISTANT,
                    content=choice.message.content or "",
                ),
                finish_reason=choice.finish_reason,
                metadata={"model": self._model},
            )
        except Exception as exc:  # noqa: BLE001
            raise ChatModelError(str(exc)) from exc

    async def stream(
        self,
        request: ChatRequest,
    ):
        """Stream a chat completion token-by-token."""

        completion = await self.complete(request)
        yield completion.message.content

    def _offline_complete(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        last_user = next(
            (
                message.content
                for message in reversed(request.messages)
                if message.role is ChatRole.USER
            ),
            "",
        )

        return ChatResponse(
            message=ChatMessage(
                role=ChatRole.ASSISTANT,
                content=(f"[offline] Acknowledged your message: {last_user[:120]}"),
            ),
            finish_reason="stop",
            metadata={"offline": True},
        )


__all__ = [
    "OpenAIChatModel",
]
