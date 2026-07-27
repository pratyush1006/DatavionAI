"""
DatavionOS provider registry.

Defines external service providers available to the platform.

Providers include:

- AI models
- Storage systems
- Messaging services
- Payment gateways
- Identity providers
- Healthcare integrations
"""

from __future__ import annotations

from dataclasses import dataclass

from .base import Registry


@dataclass(
    frozen=True,
    slots=True,
)
class ProviderDefinition:
    """
    Defines an external platform provider.

    Examples:

        azure_openai

        aws_s3

        twilio

        fhir_server
    """

    key: str

    name: str

    provider_type: str

    description: str = ""

    version: str = "1.0.0"

    enabled: bool = True

    configurable: bool = True

    tenant_selectable: bool = False

    category: str = "integration"


provider_registry = Registry[ProviderDefinition]()


__all__: tuple[str, ...] = (
    "ProviderDefinition",
    "provider_registry",
)
