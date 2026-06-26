from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("apps.departments.api.urls"),
    ),
]