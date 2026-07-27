"""
Provider selectors.
"""

from __future__ import annotations

from django.core.paginator import Paginator
from django.db.models import Q, QuerySet

from apps.clinical.providers.models import Provider
from apps.platform.organizations.models import Organization


class ProviderSelector:
    """
    Selector layer for provider read operations.
    """

    @staticmethod
    def queryset() -> QuerySet[Provider]:
        """
        Return the base provider queryset.
        """

        return Provider.objects.select_related(
            "organization",
            "employee",
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
        provider_id: int,
    ) -> Provider:
        """
        Return a provider by ID.
        """

        return ProviderSelector.queryset().get(
            id=provider_id,
        )

    @staticmethod
    def get_by_provider_number(
        *,
        organization: Organization,
        provider_number: str,
    ) -> Provider:
        """
        Return a provider by provider number.
        """

        return ProviderSelector.queryset().get(
            organization=organization,
            provider_number=provider_number,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[Provider]:
        """
        Return providers belonging to an organization.
        """

        return ProviderSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def list_active() -> QuerySet[Provider]:
        """
        Return active providers.
        """

        return ProviderSelector.queryset().filter(
            is_active=True,
        )

    @staticmethod
    def list_inactive() -> QuerySet[Provider]:
        """
        Return inactive providers.
        """

        return ProviderSelector.queryset().filter(
            is_active=False,
        )

    @staticmethod
    def list_accepting_patients() -> QuerySet[Provider]:
        """
        Return providers accepting new patients.
        """

        return ProviderSelector.queryset().filter(
            is_accepting_patients=True,
        )

    @staticmethod
    def list_by_provider_type(
        *,
        organization: Organization,
        provider_type: str,
    ) -> QuerySet[Provider]:
        """
        Return providers by provider type.
        """

        return ProviderSelector.queryset().filter(
            organization=organization,
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
        """

        return (
            ProviderSelector.queryset()
            .filter(
                organization=organization,
            )
            .filter(
                Q(employee__first_name__icontains=query)
                | Q(employee__last_name__icontains=query)
                | Q(provider_number__icontains=query)
                | Q(license_number__icontains=query)
            )
        )

    @staticmethod
    def exists(
        *,
        provider_id: int,
    ) -> bool:
        """
        Return whether a provider exists.
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
        Return the provider count for an organization.
        """

        return (
            ProviderSelector.queryset()
            .filter(
                organization=organization,
            )
            .count()
        )

    @staticmethod
    def paginated(
        *,
        organization: Organization,
        page: int,
        per_page: int,
    ):
        """
        Return a paginated provider list.
        """

        paginator = Paginator(
            ProviderSelector.list_by_organization(
                organization=organization,
            ),
            per_page,
        )

        return paginator.get_page(page)


# ----------------------------------------------------------------------
# Legacy aliases
# ----------------------------------------------------------------------

get_providers = ProviderSelector.list

get_provider_by_id = ProviderSelector.get

get_organization_providers = ProviderSelector.list_by_organization


__all__ = [
    "ProviderSelector",
    "get_provider_by_id",
    "get_providers",
    "get_organization_providers",
]
