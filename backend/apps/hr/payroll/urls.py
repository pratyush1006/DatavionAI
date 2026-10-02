from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("apps.hr.payroll.api.urls"),
    ),
]
