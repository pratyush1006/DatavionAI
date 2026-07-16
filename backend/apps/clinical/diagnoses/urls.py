"""
Diagnosis URL configuration.
"""

from django.urls import include, path

app_name = "diagnoses"

urlpatterns = [
    path(
        "",
        include("apps.clinical.diagnoses.api.urls"),
    ),
]
