from __future__ import annotations

import os
from dataclasses import dataclass

from django.conf import settings

TRUE = {"1", "true", "yes", "on"}
FALSE = {"0", "false", "no", "off"}


def _setting(name: str, default=""):
    return getattr(settings, name, default)


def env_bool(name: str, default: bool = False) -> bool:
    value = _setting(name, default)
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in TRUE:
        return True
    if normalized in FALSE:
        return False
    raise ValueError(f"{name} must be boolean")


def env_int(name: str, default: int, minimum: int, maximum: int) -> int:
    value = int(_setting(name, default))
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} out of range")
    return value


@dataclass(frozen=True)
class AIProductionConfig:
    provider: str
    model: str
    embedding_provider: str
    embedding_model: str
    allow_mock: bool
    timeout_seconds: int
    retry_count: int
    max_tokens: int
    max_prompt_length: int
    rate_limit_requests: int
    rate_limit_window_seconds: int

    @classmethod
    def from_settings(cls) -> AIProductionConfig:
        provider = str(_setting("AI_PROVIDER", "")).strip().lower()
        model = str(_setting("AI_MODEL", "")).strip()
        embedding = (
            str(_setting("AI_EMBEDDING_PROVIDER", provider) or provider).strip().lower()
        )
        embedding_model = str(
            _setting("AI_EMBEDDING_MODEL", "text-embedding-3-small")
        ).strip()
        allow_mock = env_bool("AI_ALLOW_MOCK_PROVIDER", False)

        if not provider:
            raise RuntimeError("AI_PROVIDER is required")
        if not model:
            raise RuntimeError("AI_MODEL is required")
        if provider == "mock" and not allow_mock:
            raise RuntimeError("Mock AI provider is disabled")
        if embedding == "mock" and not allow_mock:
            raise RuntimeError("Mock embedding provider is disabled")
        if not embedding_model:
            raise RuntimeError("AI_EMBEDDING_MODEL is required")

        return cls(
            provider=provider,
            model=model,
            embedding_provider=embedding,
            embedding_model=embedding_model,
            allow_mock=allow_mock,
            timeout_seconds=env_int("AI_PROVIDER_TIMEOUT_SECONDS", 30, 1, 300),
            retry_count=env_int("AI_PROVIDER_RETRY_COUNT", 2, 0, 5),
            max_tokens=env_int("AI_MAX_TOKENS", 2048, 1, 32768),
            max_prompt_length=env_int("AI_MAX_PROMPT_LENGTH", 100000, 1, 1000000),
            rate_limit_requests=env_int("AI_RATE_LIMIT_REQUESTS", 60, 1, 10000),
            rate_limit_window_seconds=env_int(
                "AI_RATE_LIMIT_WINDOW_SECONDS", 60, 1, 86400
            ),
        )


def production_config() -> AIProductionConfig:
    return AIProductionConfig.from_settings()


def _provider_credentials(provider: str) -> tuple[str, ...]:
    return {
        "openai": ("OPENAI_API_KEY",),
        "azure_openai": ("AZURE_OPENAI_API_KEY",),
        "azure": ("AZURE_OPENAI_API_KEY",),
        "gemini": ("GEMINI_API_KEY", "GOOGLE_API_KEY"),
        "google": ("GOOGLE_API_KEY", "GEMINI_API_KEY"),
        "anthropic": ("ANTHROPIC_API_KEY",),
    }.get(provider, ())


def credential_configured(provider: str) -> bool:
    keys = _provider_credentials(provider)
    if not keys:
        return provider == "mock"
    return any(bool(str(_setting(key, "")).strip()) for key in keys)


def validate_production_environment() -> list[str]:
    errors: list[str] = []

    if not os.environ.get("DJANGO_SETTINGS_MODULE", "").strip():
        errors.append("DJANGO_SETTINGS_MODULE is not configured")

    if not str(_setting("REDIS_URL", "")).strip():
        errors.append("REDIS_URL is not configured")

    provider = str(_setting("AI_PROVIDER", "")).strip().lower()
    model = str(_setting("AI_MODEL", "")).strip()

    if not provider:
        errors.append("AI_PROVIDER is not configured")
    elif provider == "mock" and not env_bool("AI_ALLOW_MOCK_PROVIDER", False):
        errors.append("AI_PROVIDER=mock is forbidden")
    elif provider != "mock" and not credential_configured(provider):
        errors.append(f"Credentials for {provider} are not configured")

    if not model:
        errors.append("AI_MODEL is not configured")

    embedding_provider = (
        str(_setting("AI_EMBEDDING_PROVIDER", provider) or provider).strip().lower()
    )
    if embedding_provider == "mock" and not env_bool("AI_ALLOW_MOCK_PROVIDER", False):
        errors.append("AI_EMBEDDING_PROVIDER=mock is forbidden")
    elif embedding_provider != "mock" and not credential_configured(embedding_provider):
        errors.append(
            f"Credentials for embedding provider {embedding_provider} are not configured"
        )

    if not str(_setting("AI_EMBEDDING_MODEL", "")).strip():
        errors.append("AI_EMBEDDING_MODEL is not configured")

    try:
        production_config()
    except Exception as exc:
        errors.append(f"AI configuration failed: {type(exc).__name__}")

    return errors
