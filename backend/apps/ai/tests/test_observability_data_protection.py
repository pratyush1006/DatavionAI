"""AI observability and data-protection regression tests."""

from __future__ import annotations

import logging

from apps.ai.services.audit import build_audit_event
from apps.ai.services.observability import (
    AIRequestMetrics,
    AIRequestTimer,
    correlation_id,
    emit_failure_event,
    sanitize_metadata,
)


def test_sensitive_metadata_is_removed():
    safe = sanitize_metadata(
        {
            "tenant_id": "tenant-1",
            "prompt": "patient diagnosis",
            "patient_name": "Jane Doe",
            "api_key": "secret",
            "latency_ms": 12,
        }
    )
    assert safe == {"tenant_id": "tenant-1", "latency_ms": 12}


def test_nested_sensitive_metadata_is_removed():
    safe = sanitize_metadata(
        {"request": {"content": "PHI", "status": "success"}, "module": "laboratory"}
    )
    assert safe == {"request": {"status": "success"}, "module": "laboratory"}


def test_metrics_are_structured_and_nonnegative():
    p = AIRequestMetrics(
        "abc", "success", -10, "openai", "gpt-4o-mini", -1, -4, -2, -1
    ).as_dict()
    assert (
        p["latency_ms"]
        == p["retry_count"]
        == p["tokens_input"]
        == p["tokens_output"]
        == 0
    )
    assert p["estimated_cost"] == 0.0


def test_correlation_id_is_deterministic_and_non_reversible():
    v = correlation_id("tenant-1", "request-1")
    assert v == correlation_id("tenant-1", "request-1")
    assert "tenant-1" not in v and "request-1" not in v


def test_timer_returns_nonnegative_duration():
    assert AIRequestTimer().elapsed_ms() >= 0


def test_audit_event_contains_identity_without_content():
    e = build_audit_event(
        "ai.request.completed",
        tenant_id="tenant-1",
        organization_id="org-1",
        actor_id="user-1",
        request_id="request-1",
        metadata={"prompt": "PHI", "status": "success"},
    )
    assert e["fingerprint"]
    assert "prompt" not in e["metadata"]
    assert "PHI" not in repr(e)


def test_failure_event_does_not_log_exception_text(caplog):
    caplog.set_level(logging.WARNING, logger="datavion.ai")
    secret = "patient diagnosis secret payload"
    emit_failure_event(
        "ai.request.failed",
        correlation="abc123",
        provider="openai",
        model="gpt-4o-mini",
        exc=RuntimeError(secret),
    )
    rendered = "\n".join(r.getMessage() for r in caplog.records)
    assert secret not in rendered
    assert "RuntimeError" in rendered and "abc123" in rendered
