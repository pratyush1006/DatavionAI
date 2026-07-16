"""
Public API for the Accounts views.
"""

from __future__ import annotations

from .authentication import (
    ChangePasswordAPIView,
    ForgotPasswordAPIView,
    GoogleLoginAPIView,
    LoginAPIView,
    LogoutAPIView,
    MeAPIView,
    MicrosoftLoginAPIView,
    RefreshAPIView,
    RegisterAPIView,
    ResendOTPAPIView,
    ResetPasswordAPIView,
    VerifyOTPAPIView,
)
from .list_create import UserListCreateAPIView
from .retrieve_update_destroy import (
    UserRetrieveUpdateDestroyAPIView,
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
    "UserListCreateAPIView",
    "UserRetrieveUpdateDestroyAPIView",
    "VerifyOTPAPIView",
]
