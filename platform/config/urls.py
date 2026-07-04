from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Django Admin
    path(
        "admin/",
        admin.site.urls,
    ),
    # API Documentation
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
    # Business APIs
    path(
        "api/auth/",
        include("apps.accounts.urls"),
    ),
    path(
        "api/rbac/",
        include("apps.rbac.urls"),
    ),
    path(
        "api/organizations/",
        include("apps.organizations.urls"),
    ),
    path(
        "api/departments/",
        include("apps.departments.urls"),
    ),
    path(
        "api/teams/",
        include("apps.teams.urls"),
    ),
    path(
        "api/employees/",
        include("apps.employees.urls"),
    ),
    path(
        "api/configuration/",
        include("apps.configuration.urls"),
    ),
    path(
        "api/storage/",
        include("apps.storage.urls"),
    ),
    path(
        "api/patients/",
        include("apps.patients.urls"),
    ),
    path(
        "api/providers/",
        include("apps.providers.urls"),
    ),
    path(
        "api/appointments/",
        include("apps.appointments.urls"),
    ),
    # Infrastructure Endpoints
    path(
        "",
        include("apps.core.urls"),
    ),
]
