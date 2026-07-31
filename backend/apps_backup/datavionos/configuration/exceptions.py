"""
Configuration exceptions.
"""

from __future__ import annotations


class ConfigurationError(Exception):
    """
    Base exception for the configuration subsystem.
    """


class ConfigurationProviderError(ConfigurationError):
    """
    Raised when configuration provider operations fail.
    """


class SecretProviderError(ConfigurationError):
    """
    Raised when secret provider operations fail.
    """


class ConfigurationValidationError(ConfigurationError):
    """
    Raised when configuration validation fails.
    """


__all__ = [
    "ConfigurationError",
    "ConfigurationProviderError",
    "SecretProviderError",
    "ConfigurationValidationError",
]
