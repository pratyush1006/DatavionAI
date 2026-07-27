from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("apps.hr.holidays.api.urls"),
    ),
]
