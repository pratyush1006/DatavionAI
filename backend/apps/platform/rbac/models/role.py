"""
Role model.
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.platform.rbac.constants import (
    DEFAULT_DISPLAY_ORDER,
    DEFAULT_ROLE_CATEGORY,
    DEFAULT_ROLE_PRIORITY,
    DEFAULT_ROLE_SCOPE,
    DEFAULT_ROLE_TYPE,
    RoleCategory,
    RoleScope,
    RoleType,
)
from apps.platform.rbac.managers import (
    RoleManager,
)


class Role(
    BaseModel,
):
    """
    Represents a reusable authorization role.
    """

    # ======================================================================
    # Identity
    # ======================================================================

    name = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
        help_text=_(
            "Human-readable role name.",
        ),
    )

    code = models.CharField(
        max_length=150,
        unique=True,
        editable=False,
        db_index=True,
        help_text=_(
            "Unique system role code.",
        ),
    )

    description = models.TextField(
        blank=True,
        help_text=_(
            "Optional role description.",
        ),
    )

    # ======================================================================
    # Classification
    # ======================================================================

    role_type = models.CharField(
        max_length=30,
        choices=RoleType.choices,
        default=DEFAULT_ROLE_TYPE,
        db_index=True,
        help_text=_(
            "Role ownership classification.",
        ),
    )

    scope = models.CharField(
        max_length=30,
        choices=RoleScope.choices,
        default=DEFAULT_ROLE_SCOPE,
        db_index=True,
        help_text=_(
            "Scope where the role applies.",
        ),
    )

    category = models.CharField(
        max_length=30,
        choices=RoleCategory.choices,
        default=DEFAULT_ROLE_CATEGORY,
        db_index=True,
        help_text=_(
            "Role category.",
        ),
    )

    # ======================================================================
    # Relationships
    # ======================================================================

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="children",
        help_text=_(
            "Parent role used for role inheritance.",
        ),
    )

    # ======================================================================
    # Authorization
    # ======================================================================

    priority = models.PositiveIntegerField(
        default=DEFAULT_ROLE_PRIORITY,
        db_index=True,
        help_text=_(
            "Authorization evaluation priority.",
        ),
    )

    display_order = models.PositiveIntegerField(
        default=DEFAULT_DISPLAY_ORDER,
        help_text=_(
            "Display order in the user interface.",
        ),
    )

    # ======================================================================
    # Behavior
    # ======================================================================

    is_system = models.BooleanField(
        default=False,
        db_index=True,
        help_text=_(
            "Whether this is a built-in platform role.",
        ),
    )

    is_default = models.BooleanField(
        default=False,
        db_index=True,
        help_text=_(
            "Whether this role is assigned by default.",
        ),
    )

    is_assignable = models.BooleanField(
        default=True,
        help_text=_(
            "Whether users may be assigned this role.",
        ),
    )

    is_editable = models.BooleanField(
        default=True,
        help_text=_(
            "Whether this role may be modified.",
        ),
    )

    is_deletable = models.BooleanField(
        default=True,
        help_text=_(
            "Whether this role may be deleted.",
        ),
    )

    # ======================================================================
    # Manager
    # ======================================================================

    objects = RoleManager()

    # ======================================================================
    # Metadata
    # ======================================================================

    class Meta:
        """
        Model metadata.
        """

        db_table = "rbac_role"

        verbose_name = _("Role")

        verbose_name_plural = _("Roles")

        ordering = (
            "display_order",
            "name",
        )

        indexes = [
            models.Index(
                fields=[
                    "role_type",
                ],
            ),
            models.Index(
                fields=[
                    "scope",
                ],
            ),
            models.Index(
                fields=[
                    "category",
                ],
            ),
            models.Index(
                fields=[
                    "priority",
                ],
            ),
            models.Index(
                fields=[
                    "is_system",
                ],
            ),
            models.Index(
                fields=[
                    "is_default",
                ],
            ),
            models.Index(
                fields=[
                    "is_active",
                ],
            ),
        ]

    # ======================================================================
    # Entity Behavior
    # ======================================================================

    def activate(
        self,
    ) -> None:
        """
        Activate the role.
        """

        self.is_active = True

    def deactivate(
        self,
    ) -> None:
        """
        Deactivate the role.
        """

        self.is_active = False

    def make_default(
        self,
    ) -> None:
        """
        Mark the role as default.
        """

        self.is_default = True

    # ======================================================================
    # Dunder Methods
    # ======================================================================

    def __str__(
        self,
    ) -> str:
        """
        Return the role name.
        """

        return self.name


__all__ = [
    "Role",
]
