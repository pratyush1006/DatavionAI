"""
Organization domain exceptions.
"""

from __future__ import annotations


class OrganizationError(Exception):
    """
    Base exception for all organization domain errors.
    """


class OrganizationNotFoundError(OrganizationError):
    """
    Raised when an organization cannot be found.
    """


class OrganizationAlreadyExistsError(OrganizationError):
    """
    Raised when attempting to create an organization that already exists.
    """


class OrganizationValidationError(OrganizationError):
    """
    Raised when organization validation fails.
    """


class OrganizationActivationError(OrganizationError):
    """
    Raised when organization activation fails.
    """


class OrganizationAlreadyActiveError(OrganizationActivationError):
    """
    Raised when the organization is already active.
    """


class OrganizationDeactivationError(OrganizationError):
    """
    Raised when organization deactivation fails.
    """


class OrganizationAlreadyInactiveError(OrganizationDeactivationError):
    """
    Raised when the organization is already inactive.
    """


class OrganizationSuspensionError(OrganizationError):
    """
    Raised when organization suspension fails.
    """


class OrganizationAlreadySuspendedError(OrganizationSuspensionError):
    """
    Raised when the organization is already suspended.
    """


class OrganizationRestorationError(OrganizationError):
    """
    Raised when organization restoration fails.
    """


class OrganizationVerificationError(OrganizationError):
    """
    Raised when organization verification fails.
    """


class OrganizationAlreadyVerifiedError(OrganizationVerificationError):
    """
    Raised when the organization has already been verified.
    """


class OrganizationDeletionError(OrganizationError):
    """
    Raised when organization deletion fails.
    """


class OrganizationHierarchyError(OrganizationError):
    """
    Raised when organization hierarchy operations fail.
    """


class OrganizationFeatureError(OrganizationError):
    """
    Raised when organization feature operations fail.
    """


class OrganizationModuleError(OrganizationError):
    """
    Raised when organization module operations fail.
    """


class OrganizationBrandingError(OrganizationError):
    """
    Raised when organization branding operations fail.
    """


class OrganizationSettingsError(OrganizationError):
    """
    Raised when organization settings operations fail.
    """


__all__: tuple[str, ...] = (
    "OrganizationActivationError",
    "OrganizationAlreadyActiveError",
    "OrganizationAlreadyExistsError",
    "OrganizationAlreadyInactiveError",
    "OrganizationAlreadySuspendedError",
    "OrganizationAlreadyVerifiedError",
    "OrganizationBrandingError",
    "OrganizationDeactivationError",
    "OrganizationDeletionError",
    "OrganizationError",
    "OrganizationFeatureError",
    "OrganizationHierarchyError",
    "OrganizationModuleError",
    "OrganizationNotFoundError",
    "OrganizationRestorationError",
    "OrganizationSettingsError",
    "OrganizationSuspensionError",
    "OrganizationValidationError",
    "OrganizationVerificationError",
)
