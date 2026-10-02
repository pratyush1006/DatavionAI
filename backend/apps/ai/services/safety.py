"""DatavionAI safety and governance guardrails."""

from __future__ import annotations

import hashlib
import re

from apps.ai.exceptions import AIValidationError

_INJECTION_PATTERNS = (
    re.compile(
        r"(?i)\bignore\s+(all|any|the)\s+(previous|prior|above)\s+instructions\b"
    ),
    re.compile(
        r"(?i)\bdisregard\s+(all|any|the)\s+(previous|prior|above)\s+instructions\b"
    ),
    re.compile(r"(?i)\breveal\s+(the\s+)?(system|developer)\s+instructions\b"),
)

_SAFE_ERROR_TYPES = {
    "AIProviderError",
    "AIProviderUnavailable",
    "CircuitOpenError",
    "TimeoutError",
}


def configured_limits():
    from apps.ai.production import production_config

    return production_config()


def validate_input_messages(messages) -> list[dict]:
    cfg = configured_limits()
    if not isinstance(messages, (list, tuple)) or not messages:
        raise AIValidationError("At least one AI message is required.")
    normalized = []
    total_length = 0
    for message in messages:
        if not isinstance(message, dict):
            raise AIValidationError("Each AI message must be an object.")
        role = message.get("role")
        content = message.get("content")
        if role not in {"system", "user", "assistant", "tool"}:
            raise AIValidationError("Invalid AI message role.")
        if not isinstance(content, str) or not content.strip():
            raise AIValidationError("AI message content is required.")
        total_length += len(content)
        if total_length > cfg.max_prompt_length:
            raise AIValidationError("AI prompt exceeds the configured safety limit.")
        normalized.append({"role": role, "content": content})
    return normalized


def validate_generation_limits(*, max_tokens: int, temperature: float) -> None:
    cfg = configured_limits()
    if not 1 <= int(max_tokens) <= cfg.max_tokens:
        raise AIValidationError(f"max_tokens must be between 1 and {cfg.max_tokens}.")
    if not 0.0 <= float(temperature) <= 2.0:
        raise AIValidationError("temperature must be between 0 and 2.")


def injection_signals(messages) -> tuple[str, ...]:
    signals = []
    for message in messages:
        content = str(message.get("content", ""))
        for pattern in _INJECTION_PATTERNS:
            if pattern.search(content):
                signals.append(pattern.pattern)
    return tuple(dict.fromkeys(signals))


def build_untrusted_context(context: str) -> str:
    if not context:
        return ""
    return (
        "\n<untrusted_retrieved_context>\n"
        + context
        + "\n</untrusted_retrieved_context>\n"
    )


def safe_error_message(exc: Exception) -> str:
    name = type(exc).__name__
    if name in _SAFE_ERROR_TYPES:
        return f"{name}: provider operation failed"
    digest = hashlib.sha256(name.encode("utf-8")).hexdigest()[:16]
    return f"AI operation failed (ref={digest})"


def validate_provider_selection(provider_name: str) -> None:
    from django.conf import settings

    from apps.ai.production import env_bool

    configured = str(getattr(settings, "AI_PROVIDER", "")).strip().lower()
    selected = str(provider_name).strip().lower()

    if not selected:
        raise AIValidationError("AI provider is required.")
    if selected == "mock":
        if not env_bool("AI_ALLOW_MOCK_PROVIDER", False):
            raise AIValidationError("Mock AI provider is disabled.")
        return
    if configured and selected != configured:
        raise AIValidationError("Requested AI provider is not permitted.")
    if not configured:
        raise AIValidationError("AI_PROVIDER is not configured for this deployment.")


def validate_embedding_provider_selection(provider_name: str) -> None:
    """Ensure RAG uses only the embedding provider approved at deployment."""
    from apps.ai.production import production_config

    selected = str(provider_name).strip().lower()
    configured = production_config().embedding_provider
    if not selected:
        raise AIValidationError("Embedding provider is required.")
    if selected != configured:
        raise AIValidationError("Requested embedding provider is not permitted.")


__all__ = (
    "build_untrusted_context",
    "injection_signals",
    "safe_error_message",
    "validate_generation_limits",
    "validate_embedding_provider_selection",
    "validate_input_messages",
    "validate_provider_selection",
)
