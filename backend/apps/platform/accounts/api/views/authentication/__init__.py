"""
Public API for authentication views.
"""

from __future__ import annotations

from .auth import (
    ChangePasswordAPIView,
    LoginAPIView,
    LogoutAPIView,
    RefreshAPIView,
    RegisterAPIView,
    VerifyLoginOTPAPIView,
)
from .me import (
    MeAPIView,
)
from .oauth import (
    GoogleLoginAPIView,
    MicrosoftLoginAPIView,
)
from .otp import (
    ResendOTPAPIView,
    VerifyOTPAPIView,
)
from .password import (
    ForgotPasswordAPIView,
    ResetPasswordAPIView,
)

__all__ = (
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
    "VerifyLoginOTPAPIView",
    "VerifyOTPAPIView",
)
