from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("apps.hr.shifts.api.urls"),
    ),
]
