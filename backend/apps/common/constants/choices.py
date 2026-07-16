"""
Reusable framework choice definitions.

Only generic, framework-wide choice helpers belong here.
Business-specific choices should live inside their
respective feature applications.
"""

from __future__ import annotations

from django.db import models


class TextChoices(
    models.TextChoices,
):
    """
    Base TextChoices class for Datavion AI.

    Feature applications should inherit from this class when
    defining string-based choices.
    """


class IntegerChoices(
    models.IntegerChoices,
):
    """
    Base IntegerChoices class for Datavion AI.

    Feature applications should inherit from this class when
    defining integer-based choices.
    """


YES_NO: tuple[tuple[bool, str], ...] = (
    (
        True,
        "Yes",
    ),
    (
        False,
        "No",
    ),
)


__all__ = [
    "IntegerChoices",
    "TextChoices",
    "YES_NO",
]
