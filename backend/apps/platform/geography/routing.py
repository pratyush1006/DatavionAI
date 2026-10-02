"""WebSocket routing for Geography live tracking."""

from __future__ import annotations

from django.urls import path

from apps.platform.geography.consumers import TrackingConsumer

websocket_urlpatterns = (
    path("ws/geography/tracking/<uuid:session_id>/", TrackingConsumer.as_asgi()),
)
__all__ = ("websocket_urlpatterns",)
