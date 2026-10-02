"""AI reliability regression tests."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from django.test import override_settings

from apps.ai.exceptions import AIProviderError
from apps.ai.providers.interfaces import ChatRequest, ChatResponse
from apps.ai.services.reliability import (
    CircuitOpenError,
    acquire_idempotency_lock,
    complete_with_reliability,
    release_idempotency_lock,
    request_fingerprint,
)


def _request():
    return ChatRequest(model="gpt-4o-mini", messages=[])


def test_idempotency_lock_is_exclusive():
    key = request_fingerprint(
        tenant_id="t1",
        organization_id="o1",
        application_id="a1",
        module_reference_id="m1",
        provider_name="mock",
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "hello"}],
        temperature=0.0,
        max_tokens=10,
        idempotency_key="request-1",
    )
    release_idempotency_lock(key)
    assert acquire_idempotency_lock(key, 30) is True
    assert acquire_idempotency_lock(key, 30) is False
    release_idempotency_lock(key)


def test_provider_retries_and_succeeds():
    class Provider:
        calls = 0

        def complete(self, request):
            self.calls += 1
            if self.calls < 3:
                raise AIProviderError("temporary failure")
            return ChatResponse(
                content="ok",
                model=request.model,
                provider="test",
                prompt_tokens=1,
                completion_tokens=1,
            )

    provider = Provider()
    with (
        override_settings(
            AI_PROVIDER="mock",
            AI_ALLOW_MOCK_PROVIDER=True,
            AI_PROVIDER_TIMEOUT_SECONDS=5,
            AI_PROVIDER_RETRY_COUNT=2,
        ),
        patch("apps.ai.services.reliability.time.sleep"),
    ):
        response = complete_with_reliability(
            provider=provider,
            request=_request(),
            provider_name="test-retry",
            model="gpt-4o-mini",
        )

    assert response.content == "ok"
    assert provider.calls == 3


def test_provider_timeout_fails_closed():
    with (
        override_settings(
            AI_PROVIDER="mock",
            AI_ALLOW_MOCK_PROVIDER=True,
            AI_PROVIDER_TIMEOUT_SECONDS=1,
            AI_PROVIDER_RETRY_COUNT=0,
        ),
        patch(
            "apps.ai.services.reliability._bounded_call",
            side_effect=AIProviderError("AI provider timeout"),
        ),
        pytest.raises(AIProviderError, match="timeout"),
    ):
        complete_with_reliability(
            provider=object(),
            request=_request(),
            provider_name="test-timeout",
            model="gpt-4o-mini",
        )


def test_circuit_breaker_opens_after_repeated_failures():
    class Provider:
        def complete(self, request):
            raise AIProviderError("provider down")

    with override_settings(
        AI_PROVIDER="mock",
        AI_ALLOW_MOCK_PROVIDER=True,
        AI_PROVIDER_TIMEOUT_SECONDS=5,
        AI_PROVIDER_RETRY_COUNT=0,
    ):
        provider = Provider()
        for _ in range(5):
            with pytest.raises(AIProviderError):
                complete_with_reliability(
                    provider=provider,
                    request=_request(),
                    provider_name="test-circuit",
                    model="gpt-4o-mini",
                )
        with pytest.raises(CircuitOpenError):
            complete_with_reliability(
                provider=provider,
                request=_request(),
                provider_name="test-circuit",
                model="gpt-4o-mini",
            )
