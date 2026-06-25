from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "organization_type",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )

    list_filter = (
        "organization_type",
        "is_active",
    )