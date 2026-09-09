"""
Provider domain services.

Exports all provider services
used by workflows and APIs.
"""

from .assignment import (
    ProviderAssignmentService,
    create_provider_assignment,
    delete_provider_assignment,
    update_provider_assignment,
)
from .availability import (
    ProviderAvailabilityService,
    create_provider_availability,
    delete_provider_availability,
    update_provider_availability,
)
from .credential import (
    ProviderCredentialService,
    create_provider_credential,
    delete_provider_credential,
    update_provider_credential,
)
from .license import (
    ProviderLicenseService,
    create_provider_license,
    delete_provider_license,
    update_provider_license,
)
from .provider import (
    ProviderService,
    create_provider,
    delete_provider,
    update_provider,
)
from .specialization import (
    ProviderSpecializationService,
    create_provider_specialization,
    delete_provider_specialization,
    update_provider_specialization,
)

__all__ = [
    # Provider
    "ProviderService",
    "create_provider",
    "update_provider",
    "delete_provider",
    # Specialization
    "ProviderSpecializationService",
    "create_provider_specialization",
    "update_provider_specialization",
    "delete_provider_specialization",
    # Credential
    "ProviderCredentialService",
    "create_provider_credential",
    "update_provider_credential",
    "delete_provider_credential",
    # License
    "ProviderLicenseService",
    "create_provider_license",
    "update_provider_license",
    "delete_provider_license",
    # Availability
    "ProviderAvailabilityService",
    "create_provider_availability",
    "update_provider_availability",
    "delete_provider_availability",
    "ProviderAssignmentService",
    "create_provider_assignment",
    "update_provider_assignment",
    "delete_provider_assignment",
]
