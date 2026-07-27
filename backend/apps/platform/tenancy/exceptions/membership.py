"""
Membership domain exceptions.
"""

from __future__ import annotations


class MembershipError(Exception):
    """
    Base exception for membership domain errors.
    """


class MembershipNotFoundError(MembershipError):
    """
    Raised when a membership cannot be found.
    """


class MembershipAlreadyExistsError(MembershipError):
    """
    Raised when attempting to create a duplicate membership.
    """


class MembershipValidationError(MembershipError):
    """
    Raised when membership validation fails.
    """


class MembershipInvitationError(MembershipError):
    """
    Raised when membership invitation operations fail.
    """


class MembershipAlreadyInvitedError(MembershipInvitationError):
    """
    Raised when the user has already been invited.
    """


class MembershipAcceptanceError(MembershipError):
    """
    Raised when membership acceptance fails.
    """


class MembershipDeclineError(MembershipError):
    """
    Raised when membership decline fails.
    """


class MembershipActivationError(MembershipError):
    """
    Raised when membership activation fails.
    """


class MembershipAlreadyActiveError(MembershipActivationError):
    """
    Raised when the membership is already active.
    """


class MembershipDeactivationError(MembershipError):
    """
    Raised when membership deactivation fails.
    """


class MembershipAlreadyInactiveError(MembershipDeactivationError):
    """
    Raised when the membership is already inactive.
    """


class MembershipSuspensionError(MembershipError):
    """
    Raised when membership suspension fails.
    """


class MembershipAlreadySuspendedError(MembershipSuspensionError):
    """
    Raised when the membership is already suspended.
    """


class MembershipRoleError(MembershipError):
    """
    Raised when membership role operations fail.
    """


class MembershipPermissionError(MembershipError):
    """
    Raised when membership permission operations fail.
    """


class MembershipRemovalError(MembershipError):
    """
    Raised when membership removal fails.
    """


__all__: tuple[str, ...] = (
    "MembershipAcceptanceError",
    "MembershipActivationError",
    "MembershipAlreadyActiveError",
    "MembershipAlreadyExistsError",
    "MembershipAlreadyInactiveError",
    "MembershipAlreadyInvitedError",
    "MembershipAlreadySuspendedError",
    "MembershipDeactivationError",
    "MembershipDeclineError",
    "MembershipError",
    "MembershipInvitationError",
    "MembershipNotFoundError",
    "MembershipPermissionError",
    "MembershipRemovalError",
    "MembershipRoleError",
    "MembershipSuspensionError",
    "MembershipValidationError",
)
