"""
Authentication API URLs.
"""

from __future__ import annotations

from django.urls import path

from apps.platform.accounts.api.views.authentication import (
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

app_name = "authentication"

urlpatterns = [
    #
    # Authentication
    #
    path(
        "register/",
        RegisterAPIView.as_view(),
        name="register",
    ),
    path(
        "login/",
        LoginAPIView.as_view(),
        name="login",
    ),
    path(
        "refresh/",
        RefreshAPIView.as_view(),
        name="refresh",
    ),
    path(
        "logout/",
        LogoutAPIView.as_view(),
        name="logout",
    ),
    #
    # Current User
    #
    path(
        "me/",
        MeAPIView.as_view(),
        name="me",
    ),
    #
    # Password Management
    #
    path(
        "change-password/",
        ChangePasswordAPIView.as_view(),
        name="change-password",
    ),
    path(
        "forgot-password/",
        ForgotPasswordAPIView.as_view(),
        name="forgot-password",
    ),
    path(
        "reset-password/",
        ResetPasswordAPIView.as_view(),
        name="reset-password",
    ),
    #
    # Email Verification
    #
    path(
        "verify-email/",
        VerifyOTPAPIView.as_view(),
        name="verify-email",
    ),
    path(
        "resend-verification/",
        ResendOTPAPIView.as_view(),
        name="resend-verification",
    ),
    #
    # OAuth
    #
    path(
        "oauth/google/",
        GoogleLoginAPIView.as_view(),
        name="google-login",
    ),
    path(
        "oauth/microsoft/",
        MicrosoftLoginAPIView.as_view(),
        name="microsoft-login",
    ),
]

__all__ = [
    "urlpatterns",
]
