"""
Configuration services.
"""

from __future__ import annotations

import json
from typing import Any

from django.db import transaction

from apps.configuration.constants import (
    CONFIGURATION_TYPE_BOOLEAN,
    CONFIGURATION_TYPE_FLOAT,
    CONFIGURATION_TYPE_INTEGER,
    CONFIGURATION_TYPE_JSON,
)
from apps.configuration.models import (
    Configuration,
    FeatureFlag,
)


@transaction.atomic
def create_configuration(
    *,
    key: str,
    category: str,
    name: str,
    description: str = "",
    value: Any,
    value_type: str,
    is_editable: bool = True,
) -> Configuration:
    """
    Create a new configuration.
    """

    return Configuration.objects.create(
        key=key,
        category=category,
        name=name,
        description=description,
        value=_serialize_value(value=value),
        value_type=value_type,
        is_editable=is_editable,
    )


@transaction.atomic
def update_configuration(
    *,
    configuration: Configuration,
    **fields: Any,
) -> Configuration:
    """
    Update an existing configuration.
    """

    if "value" in fields:
        fields["value"] = _serialize_value(
            value=fields["value"],
        )

    for field, value in fields.items():
        setattr(
            configuration,
            field,
            value,
        )

    configuration.save()

    return configuration


@transaction.atomic
def delete_configuration(
    *,
    configuration: Configuration,
) -> None:
    """
    Soft delete a configuration.
    """

    configuration.is_active = False
    configuration.save(
        update_fields=[
            "is_active",
        ],
    )


def get_configuration(
    *,
    key: str,
    default: Any = None,
) -> Any:
    """
    Return a configuration value converted to its native Python type.
    """

    try:
        configuration = Configuration.objects.get(
            key=key,
            is_active=True,
        )
    except Configuration.DoesNotExist:
        return default

    return _deserialize_value(
        value=configuration.value,
        value_type=configuration.value_type,
    )


@transaction.atomic
def set_configuration(
    *,
    key: str,
    value: Any,
) -> Configuration:
    """
    Create or update a configuration value.
    """

    configuration, _ = Configuration.objects.update_or_create(
        key=key,
        defaults={
            "value": _serialize_value(
                value=value,
            ),
        },
    )

    return configuration


def is_feature_enabled(
    *,
    key: str,
) -> bool:
    """
    Return whether a feature flag is enabled.
    """

    try:
        feature = FeatureFlag.objects.get(
            key=key,
            is_active=True,
        )
    except FeatureFlag.DoesNotExist:
        return False

    return feature.is_enabled


def _serialize_value(
    *,
    value: Any,
) -> str:
    """
    Convert a Python value to a string for storage.
    """

    if isinstance(
        value,
        (
            dict,
            list,
        ),
    ):
        return json.dumps(value)

    return str(value)


def _deserialize_value(
    *,
    value: str,
    value_type: str,
) -> Any:
    """
    Convert a stored string into its native Python type.
    """

    if value_type == CONFIGURATION_TYPE_BOOLEAN:
        return value.lower() in (
            "true",
            "1",
            "yes",
        )

    if value_type == CONFIGURATION_TYPE_INTEGER:
        return int(value)

    if value_type == CONFIGURATION_TYPE_FLOAT:
        return float(value)

    if value_type == CONFIGURATION_TYPE_JSON:
        return json.loads(value)

    return value
