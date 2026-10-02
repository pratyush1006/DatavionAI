"""Application service for provider-neutral AI chat with mandatory domain references."""

from __future__ import annotations

import time

from django.db import transaction
from django.utils import timezone

from apps.ai.exceptions import AIValidationError
from apps.ai.models import AIRequest, AIUsageRecord
from apps.ai.providers import ChatMessage, ChatRequest, get_chat_provider
from apps.ai.services.reliability import (
    acquire_idempotency_lock,
    complete_with_reliability,
    release_idempotency_lock,
    request_fingerprint,
)
from apps.ai.services.safety import (
    safe_error_message,
    validate_generation_limits,
    validate_input_messages,
    validate_provider_selection,
)
from apps.ai.services.scope import validate_application_scope


@transaction.atomic
def generate(
    *,
    application,
    tenant,
    organization,
    messages,
    module_reference,
    provider_name=None,
    model=None,
    temperature=0.0,
    max_tokens=2048,
    conversation=None,
    idempotency_key=None,
):
    from apps.ai.production import production_config

    deployment = production_config()
    provider_name = provider_name or deployment.provider
    model = model or deployment.model
    validate_application_scope(application, tenant=tenant, organization=organization)
    if module_reference is None:
        raise AIValidationError(
            "A canonical module reference is required for every AI request."
        )
    if (
        module_reference.tenant_id != tenant.id
        or module_reference.organization_id != organization.id
    ):
        raise AIValidationError(
            "AI module reference is outside the current tenant/organization scope."
        )
    messages = validate_input_messages(messages)
    validate_generation_limits(max_tokens=max_tokens, temperature=temperature)
    validate_provider_selection(provider_name)
    if not messages:
        raise AIValidationError("At least one message is required")

    if idempotency_key is not None:
        idempotency_key = str(idempotency_key).strip()
        if not idempotency_key or len(idempotency_key) > 200:
            raise AIValidationError("Invalid idempotency_key")

    fingerprint = None
    lock_acquired = False
    if idempotency_key:
        fingerprint = request_fingerprint(
            tenant_id=tenant.pk,
            organization_id=organization.pk,
            application_id=application.pk,
            module_reference_id=module_reference.pk,
            provider_name=provider_name,
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            idempotency_key=idempotency_key,
        )
        lock_acquired = acquire_idempotency_lock(fingerprint, 120)
        if not lock_acquired:
            raise AIValidationError("An identical AI request is already in progress.")

    start = time.monotonic()
    try:
        request_record = AIRequest.objects.create(
            tenant=tenant,
            organization=organization,
            application=application,
            module_reference=module_reference,
            conversation=conversation,
            provider=provider_name,
            model=model,
            request_metadata={
                "reliability": {
                    "idempotency_key": idempotency_key,
                    "fingerprint": fingerprint,
                }
            },
        )
        try:
            provider = get_chat_provider(provider_name)
            request = ChatRequest(
                model=model,
                messages=[ChatMessage(m["role"], m["content"]) for m in messages],
                temperature=float(temperature),
                max_tokens=max_tokens,
            )
            response = complete_with_reliability(
                provider=provider,
                request=request,
                provider_name=provider_name,
                model=model,
            )
            latency = max(0, int((time.monotonic() - start) * 1000))
            request_record.status = "succeeded"
            request_record.prompt_tokens = response.prompt_tokens
            request_record.completion_tokens = response.completion_tokens
            request_record.latency_ms = latency
            request_record.completed_at = timezone.now()
            request_record.save(
                update_fields=(
                    "status",
                    "prompt_tokens",
                    "completion_tokens",
                    "latency_ms",
                    "completed_at",
                )
            )
            AIUsageRecord.objects.create(
                request=request_record,
                tenant=tenant,
                organization=organization,
                provider=response.provider,
                model=response.model,
                prompt_tokens=response.prompt_tokens,
                completion_tokens=response.completion_tokens,
                total_tokens=response.prompt_tokens + response.completion_tokens,
            )
            return response
        except Exception as exc:
            request_record.status = "failed"
            request_record.error = safe_error_message(exc)
            request_record.latency_ms = max(0, int((time.monotonic() - start) * 1000))
            request_record.completed_at = timezone.now()
            request_record.save(
                update_fields=("status", "error", "latency_ms", "completed_at")
            )
            raise
    finally:
        if lock_acquired and fingerprint:
            release_idempotency_lock(fingerprint)


__all__ = ("generate",)
