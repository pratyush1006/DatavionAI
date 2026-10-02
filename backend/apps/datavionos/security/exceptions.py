"""
Security runtime exceptions.
"""

from __future__ import annotations


class SecurityError(Exception):
    """
    Base security runtime exception.
    """


class AuthenticationError(SecurityError):
    """
    Raised when authentication fails.
    """


class AuthorizationError(SecurityError):
    """
    Raised when authorization fails.
    """


class IdentityNotFoundError(SecurityError):
    """
    Raised when an identity cannot be resolved.
    """


class PrincipalNotFoundError(SecurityError):
    """
    Raised when a principal cannot be resolved.
    """


class PermissionDeniedError(SecurityError):
    """
    Raised when a required permission is missing.
    """


class PolicyEvaluationError(SecurityError):
    """
    Raised when a security policy cannot be evaluated.
    """


class InvalidCredentialError(AuthenticationError):
    """
    Raised when supplied credentials are invalid.
    """


class SessionExpiredError(AuthenticationError):
    """
    Raised when the current session has expired.
    """


class MultiFactorAuthenticationRequiredError(AuthenticationError):
    """
    Raised when multi-factor authentication
    is required before continuing.
    """
