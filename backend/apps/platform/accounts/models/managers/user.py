"""
Custom user manager for the Accounts application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction

if TYPE_CHECKING:
    from apps.platform.accounts.models.user import User


class UserManager(BaseUserManager):
    """
    Custom manager for the User model using
    email authentication.
    """

    use_in_migrations: bool = True

    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> User:
        """
        Create and return a regular user.
        """

        if not email or not email.strip():
            raise ValueError(
                "The email address must be provided.",
            )

        email = self.normalize_email(
            email.strip(),
        )

        extra_fields.setdefault(
            "username",
            email,
        )

        extra_fields.setdefault(
            "is_active",
            True,
        )

        with transaction.atomic():
            user = self.model(
                email=email,
                **extra_fields,
            )

            if password:
                user.set_password(
                    password,
                )
            else:
                user.set_unusable_password()

            user.save(
                using=self._db,
            )

        return user

    def create_superuser(
        self,
        email: str,
        password: str,
        **extra_fields: Any,
    ) -> User:
        """
        Create and return a superuser.
        """

        extra_fields.setdefault(
            "is_staff",
            True,
        )

        extra_fields.setdefault(
            "is_superuser",
            True,
        )

        extra_fields.setdefault(
            "is_active",
            True,
        )

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True.",
            )

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True.",
            )

        if not password:
            raise ValueError(
                "Superuser must have a password.",
            )

        return self.create_user(
            email=email,
            password=password,
            **extra_fields,
        )


__all__ = [
    "UserManager",
]
