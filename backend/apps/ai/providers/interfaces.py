"""Provider-neutral contracts for chat and embeddings."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str


@dataclass(frozen=True)
class ChatRequest:
    model: str
    messages: Sequence[ChatMessage]
    temperature: float = 0.0
    max_tokens: int = 2048
    metadata: dict = field(default_factory=dict)


@dataclass(frozen=True)
class ChatResponse:
    content: str
    model: str
    provider: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    metadata: dict = field(default_factory=dict)


class ChatProvider(Protocol):
    name: str

    def complete(self, request: ChatRequest) -> ChatResponse: ...
    def stream(self, request: ChatRequest) -> Iterable[str]: ...


class EmbeddingProvider(Protocol):
    name: str

    def embed(self, texts: Sequence[str], model: str) -> list[list[float]]: ...
