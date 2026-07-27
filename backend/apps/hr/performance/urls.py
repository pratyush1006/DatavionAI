from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("apps.hr.performance.api.urls"),
    ),
]
