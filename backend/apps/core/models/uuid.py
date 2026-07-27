"""
Reusable UUID primary key model.

Provides an abstract UUID primary key model for DatavionOS
business entities.

Design Principles:
- UUID v4 identifiers
- Distributed-system friendly
- Multi-tenant SaaS compatible
- Prevents sequential ID enumeration
- API-safe identifiers
"""

from __future__ import annotations

import uuid

from django.db import models


class UUIDModel(
    models.Model,
):
    """
    Abstract base model providing UUID primary keys.

    All DatavionOS domain models that require globally unique
    identifiers should inherit from this model.

    Benefits:
        - Globally unique identifiers
        - Safe distributed architecture
        - Multi-tenant SaaS compatibility
        - Prevents ID enumeration attacks
        - Suitable for microservice communication
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="Identifier",
        help_text="Globally unique UUID v4 identifier.",
    )

    class Meta:
        """
        Django model metadata.
        """

        abstract = True


__all__: tuple[str, ...] = ("UUIDModel",)
