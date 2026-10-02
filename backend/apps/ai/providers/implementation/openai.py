from __future__ import annotations

from collections.abc import Iterable

from django.conf import settings

from apps.ai.exceptions import AIProviderError, AIProviderUnavailable
from apps.ai.providers.interfaces import ChatRequest, ChatResponse


class OpenAIProvider:
    name = "openai"

    def __init__(self, *, api_key: str | None = None, base_url: str | None = None):
        configured_key = str(getattr(settings, "OPENAI_API_KEY", "") or "").strip()
        configured_base = str(getattr(settings, "OPENAI_BASE_URL", "") or "").strip()
        self.api_key = api_key or configured_key
        self.base_url = base_url or configured_base or None
        if not self.api_key:
            raise AIProviderUnavailable("OPENAI_API_KEY is not configured")

    def _client(self):
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise AIProviderUnavailable(
                "Install the openai package to use the OpenAI provider"
            ) from exc
        kwargs = {"api_key": self.api_key}
        if self.base_url:
            kwargs["base_url"] = self.base_url
        try:
            from apps.ai.services.provider_http import provider_call_kwargs

            kwargs.update(provider_call_kwargs())
        except Exception:
            pass
        return OpenAI(**kwargs)

    def complete(self, request: ChatRequest) -> ChatResponse:
        try:
            response = self._client().chat.completions.create(
                model=request.model,
                messages=[
                    {"role": m.role, "content": m.content} for m in request.messages
                ],
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )
            choice = response.choices[0]
            usage = response.usage
            return ChatResponse(
                content=choice.message.content or "",
                model=response.model,
                provider=self.name,
                prompt_tokens=getattr(usage, "prompt_tokens", 0) or 0,
                completion_tokens=getattr(usage, "completion_tokens", 0) or 0,
                metadata={"finish_reason": choice.finish_reason},
            )
        except AIProviderUnavailable:
            raise
        except Exception as exc:
            raise AIProviderError(str(exc)) from exc

    def stream(self, request: ChatRequest) -> Iterable[str]:
        try:
            stream = self._client().chat.completions.create(
                model=request.model,
                messages=[
                    {"role": m.role, "content": m.content} for m in request.messages
                ],
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                stream=True,
            )
            for event in stream:
                delta = event.choices[0].delta.content if event.choices else None
                if delta:
                    yield delta
        except AIProviderUnavailable:
            raise
        except Exception as exc:
            raise AIProviderError(str(exc)) from exc
