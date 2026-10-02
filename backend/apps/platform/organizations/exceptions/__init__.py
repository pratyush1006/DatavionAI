"""
Organization exception exports.
"""

from __future__ import annotations

from .organization import (
    OrganizationActivationError,
    OrganizationAlreadyActiveError,
    OrganizationAlreadyExistsError,
    OrganizationAlreadyInactiveError,
    OrganizationAlreadySuspendedError,
    OrganizationAlreadyVerifiedError,
    OrganizationBrandingError,
    OrganizationDeactivationError,
    OrganizationDeletionError,
    OrganizationError,
    OrganizationFeatureError,
    OrganizationHierarchyError,
    OrganizationModuleError,
    OrganizationNotFoundError,
    OrganizationRestorationError,
    OrganizationSettingsError,
    OrganizationSuspensionError,
    OrganizationValidationError,
    OrganizationVerificationError,
)

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
