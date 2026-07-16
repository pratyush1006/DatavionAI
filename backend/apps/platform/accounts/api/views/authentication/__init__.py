"""
Public API for authentication views.
"""

from __future__ import annotations

from .auth import (
    LoginAPIView,
    LogoutAPIView,
    RefreshAPIView,
    RegisterAPIView,
)
from .me import MeAPIView
from .oauth import (
    GoogleLoginAPIView,
    MicrosoftLoginAPIView,
)
from .otp import (
    ResendOTPAPIView,
    VerifyOTPAPIView,
)
from .password import (
    ChangePasswordAPIView,
    ForgotPasswordAPIView,
    ResetPasswordAPIView,
)

__all__ = [
    "ChangePasswordAPIView",
    "ForgotPasswordAPIView",
    "GoogleLoginAPIView",
    "LoginAPIView",
    "LogoutAPIView",
    "MeAPIView",
    "MicrosoftLoginAPIView",
    "RefreshAPIView",
    "RegisterAPIView",
    "ResendOTPAPIView",
    "ResetPasswordAPIView",
    "VerifyOTPAPIView",
]
