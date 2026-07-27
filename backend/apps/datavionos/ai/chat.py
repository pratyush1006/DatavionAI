"""
Chat model contracts.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from enum import StrEnum
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


class ChatRole(
    StrEnum,
):
    """
    Supported chat message roles.
    """

    SYSTEM = "system"

    USER = "user"

    ASSISTANT = "assistant"

    TOOL = "tool"


@dataclass(
    frozen=True,
    slots=True,
)
class ChatMessage:
    """
    Immutable chat message.
    """

    role: ChatRole

    content: str

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class ChatRequest:
    """
    Immutable chat request.
    """

    messages: tuple[ChatMessage, ...]

    temperature: float = 0.7

    max_tokens: int | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class ChatResponse:
    """
    Immutable chat response.
    """

    message: ChatMessage

    finish_reason: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@runtime_checkable
class ChatModel(
    Protocol,
):
    """
    Conversational AI model.
    """

    async def complete(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """
        Generate a chat completion.
        """

    async def stream(
        self,
        request: ChatRequest,
    ) -> AsyncIterator[str]:
        """
        Stream a chat completion.
        """


from collections.abc import AsyncIterator

__all__ = [
    "ChatMessage",
    "ChatRequest",
    "ChatResponse",
    "ChatRole",
    "ChatModel",
]
