"""AI domain exceptions."""

from __future__ import annotations


class AIError(Exception):
    """Base AI platform exception."""


class AIConfigurationError(AIError):
    """Invalid or missing AI configuration."""


class AIProviderError(AIError):
    """Provider execution failure."""


class AIProviderUnavailable(AIProviderError):
    """Provider is not configured or temporarily unavailable."""


class AIValidationError(AIError):
    """Invalid AI request or domain state."""


class AIAuthorizationError(AIError):
    """AI resource is outside the caller's tenant/organization scope."""
