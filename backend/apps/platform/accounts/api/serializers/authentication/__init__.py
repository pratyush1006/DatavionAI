"""
Public authentication serializer API for the Accounts application.
"""

from __future__ import annotations

from .auth import (
    LoginSerializer,
    LogoutSerializer,
    RefreshSerializer,
    RegisterSerializer,
    ResendLoginOTPSerializer,
    VerifyLoginOTPSerializer,
)
from .me import (
    MeSerializer,
)
from .oauth import (
    GoogleLoginSerializer,
    MicrosoftLoginSerializer,
)
from .otp import (
    ResendOTPSerializer,
    VerifyOTPSerializer,
)
from .password import (
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from .token import (
    TokenResponseSerializer,
)

__all__ = (
    "ChangePasswordSerializer",
    "ForgotPasswordSerializer",
    "GoogleLoginSerializer",
    "LoginSerializer",
    "LogoutSerializer",
    "MeSerializer",
    "MicrosoftLoginSerializer",
    "RefreshSerializer",
    "RegisterSerializer",
    "ResendLoginOTPSerializer",
    "ResendOTPSerializer",
    "ResetPasswordSerializer",
    "TokenResponseSerializer",
    "VerifyLoginOTPSerializer",
    "VerifyOTPSerializer",
)
