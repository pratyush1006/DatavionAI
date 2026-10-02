"""
Service result objects for the Accounts application.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.platform.accounts.models import OTP


@dataclass(
    frozen=True,
    slots=True,
)
class OTPCreateResult:
    """
    Result returned after OTP creation.

    The OTP database object stores only the hash.
    The plain code exists only during delivery flow.
    """

    otp: OTP

    code: str


__all__ = [
    "OTPCreateResult",
]
