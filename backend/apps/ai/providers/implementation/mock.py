"""Deterministic provider for local development and contract tests."""

from __future__ import annotations

from collections.abc import Iterable

from apps.ai.providers.interfaces import ChatRequest, ChatResponse


class MockProvider:
    name = "mock"

    def complete(self, request: ChatRequest) -> ChatResponse:
        user = next(
            (m.content for m in reversed(request.messages) if m.role == "user"), ""
        )
        content = f"Mock AI response: {user}".strip()
        return ChatResponse(
            content=content,
            model=request.model,
            provider=self.name,
            prompt_tokens=sum(len(m.content.split()) for m in request.messages),
            completion_tokens=len(content.split()),
        )

    def stream(self, request: ChatRequest) -> Iterable[str]:
        response = self.complete(request).content
        for token in response.split():
            yield token + " "
