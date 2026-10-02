"""Production HR, bootstrap and auth endpoints for the isolated browser test server."""

from django.urls import include, path

urlpatterns = [
    path("api/hr/", include("apps.hr.schema_urls")),
    path("api/employees/", include("apps.organization.employees.urls")),
    path("api/departments/", include("apps.organization.departments.urls")),
    path("api/platform/", include("apps.datavionos.api.urls")),
    path("api/auth/", include("apps.platform.accounts.urls")),
    path("api/tenancy/", include("apps.platform.tenancy.api.urls")),
]
