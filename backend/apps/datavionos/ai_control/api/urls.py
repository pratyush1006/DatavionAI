from django.urls import path

from apps.datavionos.ai_control.api.views import (
    AIControlPlaneAPIView,
    AIControlToggleAPIView,
)

app_name = "datavionos-ai-control"


urlpatterns = [
    path(
        "",
        AIControlPlaneAPIView.as_view(),
        name="control-plane",
    ),
    path(
        "<uuid:application_id>/toggle/",
        AIControlToggleAPIView.as_view(),
        name="toggle",
    ),
]
