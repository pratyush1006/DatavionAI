"""
Platform Core URL configuration.
"""

from django.urls import include, path

app_name = "platform-core"

urlpatterns = [
    path(
        "",
        include("apps.datavionos.api.urls"),
    ),
]
