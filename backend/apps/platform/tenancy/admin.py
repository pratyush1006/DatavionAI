"""
Tenant administration.
"""

from django.contrib import admin

from apps.platform.tenancy.models import (
    Tenant,
    TenantDomain,
    TenantMembership,
    TenantSettings,
)


@admin.register(Tenant)
class TenantAdmin(
    admin.ModelAdmin,
):
    list_display = (
        "name",
        "slug",
        "tenant_type",
        "status",
    )

    search_fields = (
        "name",
        "slug",
    )


@admin.register(TenantMembership)
class TenantMembershipAdmin(
    admin.ModelAdmin,
):
    list_display = (
        "tenant",
        "user",
        "status",
        "is_owner",
    )

    list_filter = (
        "status",
        "is_owner",
    )


@admin.register(TenantDomain)
class TenantDomainAdmin(
    admin.ModelAdmin,
):
    list_display = (
        "tenant",
        "domain",
    )


@admin.register(TenantSettings)
class TenantSettingsAdmin(
    admin.ModelAdmin,
):
    list_display = ("tenant",)
