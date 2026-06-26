from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("apps.employees.api.urls"),
    ),
]
