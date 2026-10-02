from __future__ import annotations

from collections.abc import Sequence

from django.conf import settings

from apps.ai.exceptions import AIProviderError, AIProviderUnavailable


class MockEmbeddingProvider:
    name = "mock"

    def embed(self, texts: Sequence[str], model: str) -> list[list[float]]:
        result = []
        for text in texts:
            value = float(sum(ord(ch) for ch in text) % 10000) / 10000.0
            result.append([value, float(len(text) % 1000) / 1000.0])
        return result


class OpenAIEmbeddingProvider:
    name = "openai"

    def __init__(self, *, api_key: str | None = None):
        configured_key = str(getattr(settings, "OPENAI_API_KEY", "") or "").strip()
        self.api_key = api_key or configured_key
        if not self.api_key:
            raise AIProviderUnavailable("OPENAI_API_KEY is not configured")

    def embed(self, texts: Sequence[str], model: str) -> list[list[float]]:
        try:
            from openai import OpenAI

            from apps.ai.services.provider_http import provider_call_kwargs

            client = OpenAI(api_key=self.api_key, **provider_call_kwargs())
            response = client.embeddings.create(model=model, input=list(texts))
            return [item.embedding for item in response.data]
        except AIProviderUnavailable:
            raise
        except Exception as exc:
            raise AIProviderError(str(exc)) from exc
