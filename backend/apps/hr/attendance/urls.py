from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("apps.hr.attendance.api.urls"),
    ),
]
