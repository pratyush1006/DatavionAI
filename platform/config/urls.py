from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
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
        "api/v1/",
        include("apps.core.urls"),
    ),
]
