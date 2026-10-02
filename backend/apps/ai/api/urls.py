from __future__ import annotations

from django.http import JsonResponse

from apps.ai.services.health import liveness, readiness

"""AI API routes."""

from django.urls import path

from .clinical import (
    ClinicalArtifactCreateAPIView,
    ClinicalArtifactReviewAPIView,
    ClinicalNoteCleanAPIView,
    LaboratoryOrderStatusAPIView,
    PrescriptionDraftAPIView,
)
from .views import (
    AIApplicationsAPIView,
    AIChatAPIView,
    AIChatStreamAPIView,
    AIHealthAPIView,
    AIRAGIndexAPIView,
    AIRAGSearchAPIView,
)

app_name = "ai-api"

urlpatterns = [
    path("health/live/", lambda request: JsonResponse(liveness()), name="ai-liveness"),
    path(
        "health/ready/", lambda request: JsonResponse(readiness()), name="ai-readiness"
    ),
    path("health/", AIHealthAPIView.as_view(), name="ai-health"),
    path("applications/", AIApplicationsAPIView.as_view(), name="ai-applications"),
    path("chat/", AIChatAPIView.as_view(), name="ai-chat"),
    path("chat/stream/", AIChatStreamAPIView.as_view(), name="ai-chat-stream"),
    path("rag/index/", AIRAGIndexAPIView.as_view(), name="ai-rag-index"),
    path("rag/search/", AIRAGSearchAPIView.as_view(), name="ai-rag-search"),
    path(
        "clinical/artifacts/",
        ClinicalArtifactCreateAPIView.as_view(),
        name="ai-clinical-artifact-create",
    ),
    path(
        "clinical/artifacts/versions/<uuid:version_id>/review/",
        ClinicalArtifactReviewAPIView.as_view(),
        name="ai-clinical-artifact-review",
    ),
    path(
        "clinical/lab-orders/status/",
        LaboratoryOrderStatusAPIView.as_view(),
        name="ai-lab-order-status",
    ),
    path(
        "clinical/notes/clean/",
        ClinicalNoteCleanAPIView.as_view(),
        name="ai-clinical-note-clean",
    ),
    path(
        "clinical/prescriptions/draft/",
        PrescriptionDraftAPIView.as_view(),
        name="ai-prescription-draft",
    ),
]
