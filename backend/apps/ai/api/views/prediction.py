"""
API views for listing and creating predictions.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.ai.api.serializers import (
    PredictionCreateSerializer,
    PredictionDetailSerializer,
    PredictionListSerializer,
    PredictionUpdateSerializer,
)
from apps.ai.models import Prediction
from apps.ai.permissions import (
    CanCreatePrediction,
    CanDeletePrediction,
    CanUpdatePrediction,
    CanViewPrediction,
)
from apps.ai.selectors import PredictionSelector
from apps.ai.services import PredictionService
from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)

PREDICTION_TAG: Final[tuple[str, ...]] = ("Predictions",)


@extend_schema(tags=PREDICTION_TAG)
class PredictionListCreateAPIView(BaseListCreateAPIView):
    """
    API view for listing existing predictions and creating new predictions.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewPrediction,
        ),
        "POST": (
            IsAuthenticated,
            CanCreatePrediction,
        ),
    }

    serializer_classes = {
        "GET": PredictionListSerializer,
        "POST": PredictionCreateSerializer,
    }

    detail_serializer_class = PredictionDetailSerializer

    create_service = PredictionService.create

    create_success_message = "Prediction created successfully."

    ordering = ("-predicted_at",)

    ordering_fields = (
        "predicted_at",
        "risk_score",
        "prediction_type",
        "risk_level",
    )

    filterset_fields = (
        "prediction_type",
        "risk_level",
        "is_reviewed",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Prediction]:
        """
        Return the prediction queryset.
        """

        return PredictionSelector.queryset()


@extend_schema(tags=PREDICTION_TAG)
class PredictionRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a prediction.
    """

    lookup_url_kwarg = "prediction_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewPrediction,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdatePrediction,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdatePrediction,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeletePrediction,
        ),
    }

    serializer_class = PredictionDetailSerializer

    serializer_classes = {
        "GET": PredictionDetailSerializer,
        "PUT": PredictionUpdateSerializer,
        "PATCH": PredictionUpdateSerializer,
    }

    update_service = PredictionService.update

    delete_service = PredictionService.delete

    def get_object(
        self,
    ) -> Prediction:
        """
        Return the requested prediction.
        """

        return PredictionSelector.get(
            prediction_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "PredictionListCreateAPIView",
    "PredictionRetrieveUpdateDestroyAPIView",
]
