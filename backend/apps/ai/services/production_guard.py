"""DatavionAI runtime request guardrails."""

from __future__ import annotations

import hashlib

from django.core.cache import cache

from apps.ai.production import production_config


class AIRateLimitExceeded(Exception):
    pass


class AIPromptLimitExceeded(Exception):
    pass


def enforce_prompt_limit(messages):
    limit = production_config().max_prompt_length
    size = sum(len(str(item.get("content", ""))) for item in messages)
    if size > limit:
        raise AIPromptLimitExceeded("AI prompt exceeds configured limit")


def enforce_rate_limit(*, tenant, organization, actor=None):
    cfg = production_config()
    raw = f"{tenant.pk}:{organization.pk}:{getattr(actor, 'pk', 'anonymous')}"
    key = "datavion:ai:rate:" + hashlib.sha256(raw.encode()).hexdigest()
    try:
        count = cache.incr(key)
    except ValueError:
        cache.add(key, 1, timeout=cfg.rate_limit_window_seconds)
        count = 1
    if count > cfg.rate_limit_requests:
        raise AIRateLimitExceeded("AI request rate limit exceeded")


def safe_provider_error(_exc):
    return "AI provider request failed."
