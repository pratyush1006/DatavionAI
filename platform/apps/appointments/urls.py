"""
Appointment URL configuration.
"""

from django.urls import include, path

app_name = "appointments"

urlpatterns = [
    path(
        "",
        include("apps.appointments.api.urls"),
    ),
]
