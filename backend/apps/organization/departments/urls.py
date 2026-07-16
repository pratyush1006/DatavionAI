from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("apps.organization.departments.api.urls"),
    ),
]
