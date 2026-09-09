"""
Root URL configuration for DatavionAI.

DatavionOS API Gateway routing layer.

Responsibilities:

- Admin
- API Documentation
- Platform modules
- Identity & Access
- SaaS Platform
- Organization operations
- Document Management
- Clinical modules
- AI Platform
- Device Platform
- Infrastructure
"""

from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # ==========================================================================
    # Django Administration
    # ==========================================================================
    path(
        "admin/",
        admin.site.urls,
    ),
    # ==========================================================================
    # API Documentation
    # ==========================================================================
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema",
        ),
        name="swagger-ui",
    ),
    # ==========================================================================
    # Platform APIs
    # ==========================================================================
    path(
        "api/auth/",
        include(
            "apps.platform.accounts.urls",
        ),
    ),
    path(
        "api/audit/",
        include(
            "apps.platform.audit.urls",
        ),
    ),
    path(
        "api/notifications/",
        include(
            "apps.platform.notifications.urls",
        ),
    ),
    path(
        "api/tenancy/",
        include(
            "apps.platform.tenancy.api.urls",
        ),
    ),
    path(
        "api/geography/",
        include(
            "apps.platform.geography.urls",
        ),
    ),
    path(
        "api/platform/",
        include(
            "apps.datavionos.api.urls",
        ),
    ),
    # ==========================================================================
    # Identity & Access Management
    # ==========================================================================
    path(
        "api/rbac/",
        include(
            "apps.platform.rbac.urls",
        ),
    ),
    path(
        "api/organizations/",
        include(
            "apps.platform.organizations.urls",
        ),
    ),
    # ==========================================================================
    # Document Management
    # ==========================================================================
    path(
        "api/documents/",
        include(
            "apps.documents.api.urls",
        ),
    ),
    # ==========================================================================
    # SaaS Platform Billing
    # ==========================================================================
    path(
        "api/saas-billing/",
        include(
            "apps.platform.saas_billing.urls",
        ),
    ),
    # ==========================================================================
    # Organization Operations
    # ==========================================================================
    path(
        "api/departments/",
        include(
            "apps.organization.departments.urls",
        ),
    ),
    path(
        "api/teams/",
        include(
            "apps.organization.teams.urls",
        ),
    ),
    path(
        "api/employees/",
        include(
            "apps.organization.employees.urls",
        ),
    ),
    # ==========================================================================
    # Configuration
    # ==========================================================================
    path(
        "api/configuration/",
        include(
            "apps.configuration.urls",
        ),
    ),
    # ==========================================================================
    # Patient Management
    # ==========================================================================
    path(
        "api/patient-management/",
        include(
            "apps.patient_management.urls",
        ),
    ),
    # ==========================================================================
    # Clinical APIs
    # ==========================================================================
    path(
        "api/providers/",
        include(
            (
                "apps.clinical.providers.urls",
                "providers",
            ),
        ),
    ),
    path(
        "api/appointments/",
        include(
            "apps.clinical.appointments.urls",
        ),
    ),
    path(
        "api/encounters/",
        include(
            "apps.clinical.encounters.urls",
        ),
    ),
    path(
        "api/diagnoses/",
        include(
            "apps.clinical.diagnoses.urls",
        ),
    ),
    path(
        "api/medications/",
        include(
            "apps.clinical.medications.urls",
        ),
    ),
    path(
        "api/prescriptions/",
        include(
            "apps.clinical.prescriptions.urls",
        ),
    ),
    path(
        "api/allergies/",
        include(
            "apps.clinical.allergies.urls",
        ),
    ),
    path(
        "api/vitals/",
        include(
            "apps.clinical.vitals.urls",
        ),
    ),
    path(
        "api/laboratories/",
        include(
            "apps.clinical.laboratories.urls",
        ),
    ),
    # ==========================================================================
    # Device Platform
    # ==========================================================================
    path(
        "api/device-platform/",
        include(
            "apps.device_platform.urls",
        ),
    ),
    # ==========================================================================
    # AI Platform APIs
    # ==========================================================================
    path(
        "api/ai/",
        include(
            "apps.ai.urls",
        ),
    ),
    path(
        "api/search/",
        include(
            "apps.common.search.api.urls",
        ),
    ),
    # ==========================================================================
    # Telemedicine / Imaging / Billing / Revenue Cycle
    # ==========================================================================
    path(
        "api/telemedicine/",
        include(
            "apps.telemedicine.api.urls",
        ),
    ),
    path(
        "api/imaging/",
        include(
            "apps.imaging.api.urls",
        ),
    ),
    path(
        "api/billing/",
        include(
            "apps.billing.urls",
        ),
    ),
    path(
        "api/revenue-cycle/",
        include(
            "apps.revenue_cycle.urls",
        ),
    ),
    # ==========================================================================
    # Infrastructure
    # ==========================================================================
    path(
        "",
        include(
            "apps.core.urls",
        ),
    ),
]
