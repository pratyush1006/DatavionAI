"""
Public serializer API for the Accounts application.
"""

from __future__ import annotations

from .authentication import (
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    GoogleLoginSerializer,
    LoginSerializer,
    LogoutSerializer,
    MeSerializer,
    MicrosoftLoginSerializer,
    RefreshSerializer,
    RegisterSerializer,
    ResendOTPSerializer,
    ResetPasswordSerializer,
    VerifyOTPSerializer,
)
from .base import UserBaseSerializer
from .create import UserCreateSerializer
from .detail import UserDetailSerializer
from .list import UserListSerializer
from .summary import UserSummarySerializer
from .update import UserUpdateSerializer

__all__ = [
    "ChangePasswordSerializer",
    "ForgotPasswordSerializer",
    "GoogleLoginSerializer",
    "LoginSerializer",
    "LogoutSerializer",
    "MeSerializer",
    "MicrosoftLoginSerializer",
    "RefreshSerializer",
    "RegisterSerializer",
    "ResendOTPSerializer",
    "ResetPasswordSerializer",
    "UserBaseSerializer",
    "UserCreateSerializer",
    "UserDetailSerializer",
    "UserListSerializer",
    "UserSummarySerializer",
    "UserUpdateSerializer",
    "VerifyOTPSerializer",
]
