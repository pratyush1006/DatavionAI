from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("apps.organization.employees.api.urls"),
    ),
]
