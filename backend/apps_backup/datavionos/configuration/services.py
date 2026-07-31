"""
Configuration service aggregation.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.configuration.provider import (
    ConfigurationProvider,
)
from apps.datavionos.configuration.secrets import (
    SecretProvider,
)
from apps.datavionos.configuration.validation import (
    ConfigurationValidator,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ConfigurationServices:
    """
    Aggregate of configuration services.
    """

    provider: ConfigurationProvider

    secrets: SecretProvider

    validator: ConfigurationValidator


__all__ = [
    "ConfigurationServices",
]
