from django.urls import path

from .live import LiveTranscriptionConsumer

websocket_urlpatterns = [
    path(
        "ws/transcription/live/<uuid:session_id>/", LiveTranscriptionConsumer.as_asgi()
    )
]
