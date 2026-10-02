"""
Root URL configuration for DatavionAI.

DatavionOS API Gateway routing layer.

Responsibilities
----------------
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
- Revenue Cycle
- Enterprise Finance
- Infrastructure
"""

from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("api/ai-control/", include("apps.datavionos.ai_control.api.urls")),
    path(
        "api/organization-access/", include("apps.datavionos.access_control.api.urls")
    ),
    path(
        "api/organization-control/", include("apps.datavionos.control_plane.api.urls")
    ),
    path("api/hospital-operations/", include("apps.hospital_operations.api.urls")),
    path("api/ai/", include("apps.ai.api.urls")),
    path("api/transcription/", include("apps.transcription.api.urls")),
    # ==========================================================================
    # Notes
    # ==========================================================================
    path(
        "api/notes/",
        include("apps.notes.urls"),
    ),
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
    path(
        "api/onboarding/",
        include(
            "apps.datavionos.onboarding.api.urls",
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
    path(
        "api/nursing/",
        include("apps.clinical.nursing.urls"),
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
        "api/search/",
        include(
            "apps.common.search.api.urls",
        ),
    ),
    # ==========================================================================
    # Telemedicine
    # ==========================================================================
    path(
        "api/telemedicine/",
        include(
            "apps.telemedicine.api.urls",
        ),
    ),
    # ==========================================================================
    # Imaging
    # ==========================================================================
    path(
        "api/imaging/",
        include(
            "apps.imaging.api.urls",
        ),
    ),
    # ==========================================================================
    # Enterprise Finance
    #
    # Canonical owner:
    #     apps.billing.finance
    #
    # Both routes intentionally point to the same canonical Finance API.
    # /api/billing/ is the primary bounded-context route.
    # /api/finance/ is retained as a stable public API route and is required
    # by the Finance production-hardening contract.
    # ==========================================================================
    path(
        "api/billing/",
        include("apps.billing.finance.api.urls"),
    ),
    path(
        "api/finance/",
        include("apps.billing.finance.api.urls"),
    ),
    # ==========================================================================
    # Insurance
    # ==========================================================================
    path(
        "api/insurance/",
        include(
            "apps.insurance.urls",
        ),
    ),
    # ==========================================================================
    # Revenue Cycle
    #
    # Healthcare billing is owned exclusively by Revenue Cycle.
    # ==========================================================================
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
    # ==========================================================================
    # Pharmacy
    # ==========================================================================
    path(
        "api/pharmacy/",
        include(
            "apps.pharmacy.api.urls",
        ),
    ),
    # ==========================================================================
    # Human Resources
    # ==========================================================================
    path("api/hr/recruitment/", include("apps.hr.recruitment.urls")),
    path(
        "api/hr/attendance/",
        include("apps.hr.attendance.urls"),
    ),
    path(
        "api/hr/holidays/",
        include("apps.hr.holidays.urls"),
    ),
    path(
        "api/hr/leave/",
        include("apps.hr.leave.urls"),
    ),
    path(
        "api/hr/onboarding/",
        include("apps.hr.onboarding.urls"),
    ),
    path(
        "api/hr/payroll/",
        include("apps.hr.payroll.urls"),
    ),
    path(
        "api/hr/performance/",
        include("apps.hr.performance.urls"),
    ),
    path(
        "api/hr/shifts/",
        include("apps.hr.shifts.urls"),
    ),
    # ==========================================================================
    # Compliance and Interoperability
    # ==========================================================================
    path(
        "api/compliance/",
        include("apps.compliance.api.urls"),
    ),
    path(
        "api/interoperability/",
        include("apps.interoperability.api.urls"),
    ),
]
