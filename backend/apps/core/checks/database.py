"""
Database system checks for the DatavionOS platform.
"""

from __future__ import annotations

from django.conf import settings
from django.core.checks import Error, Tags, register
from django.db import connections
from django.db.utils import OperationalError


@register(Tags.database)
def database_check(
    app_configs,
    **kwargs,
):
    """
    Verify database configuration and connectivity.
    """

    errors = []

    databases = getattr(
        settings,
        "DATABASES",
        {},
    )

    if not databases.get("default"):
        errors.append(
            Error(
                "Default database is not configured.",
                hint="Configure DATABASES['default'] in settings.",
                id="datavion.E001",
            )
        )

        return errors

    connection = connections["default"]

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

            cursor.fetchone()

        if not connection.is_usable():
            errors.append(
                Error(
                    "Database connection is not usable.",
                    hint="Check database availability.",
                    id="datavion.E002",
                )
            )

    except OperationalError as exc:
        errors.append(
            Error(
                "Database connection failed.",
                hint=str(exc),
                id="datavion.E003",
            )
        )

    return errors
