"""
Provider selectors.

Read layer for Provider bounded context.

Responsibilities:

- Tenant aware reads
- Organization scoped queries
- Optimized ORM loading
- Provider identity search
- Backward compatible selector exports

DatavionOS Healthcare Platform.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import (
    Q,
    QuerySet,
)

from apps.clinical.providers.constants import (
    ProviderStatus,
)
from apps.clinical.providers.models import (
    Provider,
)
from apps.platform.organizations.models import (
    Organization,
)


class ProviderSelector:
    """
    Selector layer for provider reads.
    """

    @staticmethod
    def queryset() -> QuerySet[Provider]:
        """
        Base optimized provider queryset.
        """

        return Provider.objects.select_related(
            "organization",
            "employee",
            "employee__user",
        ).prefetch_related(
            "specializations",
            "credentials",
            "availability",
            "assignments",
        )

    @staticmethod
    def list() -> QuerySet[Provider]:
        """
        Return all providers.
        """

        return ProviderSelector.queryset()

    @staticmethod
    def get(
        *,
        provider_id: UUID,
    ) -> Provider:
        """
        Return provider by id.
        """

        return ProviderSelector.queryset().get(
            id=provider_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[Provider]:
        """
        Return providers scoped to organization.
        """

        return ProviderSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def list_active(
        *,
        organization: Organization,
    ) -> QuerySet[Provider]:
        """
        Return active providers.
        """

        return ProviderSelector.list_by_organization(
            organization=organization,
        ).filter(
            status=ProviderStatus.ACTIVE,
        )

    @staticmethod
    def list_accepting_patients(
        *,
        organization: Organization,
    ) -> QuerySet[Provider]:
        """
        Return providers accepting patients.
        """

        return ProviderSelector.list_by_organization(
            organization=organization,
        ).filter(
            is_accepting_patients=True,
        )

    @staticmethod
    def list_by_provider_type(
        *,
        organization: Organization,
        provider_type: str,
    ) -> QuerySet[Provider]:
        """
        Filter providers by provider type.
        """

        return ProviderSelector.list_by_organization(
            organization=organization,
        ).filter(
            provider_type=provider_type,
        )

    @staticmethod
    def search(
        *,
        organization: Organization,
        query: str,
    ) -> QuerySet[Provider]:
        """
        Search providers.

        Searches:

        - Employee first name
        - Employee last name
        - Employee code
        - Employee work email
        - Provider number

        License search is intentionally excluded.
        License management belongs to credential/compliance
        bounded context.
        """

        return (
            ProviderSelector.list_by_organization(
                organization=organization,
            )
            .filter(
                Q(employee__user__first_name__icontains=query)
                | Q(employee__user__last_name__icontains=query)
                | Q(employee__employee_code__icontains=query)
                | Q(employee__work_email__icontains=query)
                | Q(provider_number__icontains=query)
            )
            .distinct()
        )

    @staticmethod
    def exists(
        *,
        provider_id: UUID,
    ) -> bool:
        """
        Check provider existence.
        """

        return (
            ProviderSelector.queryset()
            .filter(
                id=provider_id,
            )
            .exists()
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Count providers in organization.
        """

        return ProviderSelector.list_by_organization(
            organization=organization,
        ).count()


# ----------------------------------------------------------------------
# Legacy compatibility aliases
# ----------------------------------------------------------------------

get_providers = ProviderSelector.list

get_provider_by_id = ProviderSelector.get

get_organization_providers = ProviderSelector.list_by_organization


__all__ = (
    "ProviderSelector",
    "get_providers",
    "get_provider_by_id",
    "get_organization_providers",
)
