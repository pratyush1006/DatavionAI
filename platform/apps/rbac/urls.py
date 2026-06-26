from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("apps.rbac.api.urls"),
    ),
]
