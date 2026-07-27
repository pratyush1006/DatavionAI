"""
API views for retrieving, updating, and deleting recommendations.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.ai.api.serializers import (
    RecommendationCreateSerializer,
    RecommendationDetailSerializer,
    RecommendationListSerializer,
    RecommendationUpdateSerializer,
)
from apps.ai.models import Recommendation
from apps.ai.permissions import (
    CanCreateRecommendation,
    CanDeleteRecommendation,
    CanUpdateRecommendation,
    CanViewRecommendation,
)
from apps.ai.selectors import RecommendationSelector
from apps.ai.services import RecommendationService
from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)

RECOMMENDATION_TAG: Final[tuple[str, ...]] = ("Recommendations",)


@extend_schema(tags=RECOMMENDATION_TAG)
class RecommendationListCreateAPIView(BaseListCreateAPIView):
    """
    API view for listing existing recommendations and creating new recommendations.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewRecommendation,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateRecommendation,
        ),
    }

    serializer_classes = {
        "GET": RecommendationListSerializer,
        "POST": RecommendationCreateSerializer,
    }

    detail_serializer_class = RecommendationDetailSerializer

    create_service = RecommendationService.create

    create_success_message = "Recommendation created successfully."

    ordering = ("-created_at",)

    ordering_fields = (
        "created_at",
        "priority",
        "status",
    )

    filterset_fields = (
        "recommendation_type",
        "status",
        "priority",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Recommendation]:
        """
        Return the recommendation queryset.
        """

        return RecommendationSelector.queryset()


@extend_schema(tags=RECOMMENDATION_TAG)
class RecommendationRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a recommendation.
    """

    lookup_url_kwarg = "recommendation_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewRecommendation,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateRecommendation,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateRecommendation,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteRecommendation,
        ),
    }

    serializer_class = RecommendationDetailSerializer

    serializer_classes = {
        "GET": RecommendationDetailSerializer,
        "PUT": RecommendationUpdateSerializer,
        "PATCH": RecommendationUpdateSerializer,
    }

    update_service = RecommendationService.update

    delete_service = RecommendationService.delete

    def get_object(
        self,
    ) -> Recommendation:
        """
        Return the requested recommendation.
        """

        return RecommendationSelector.get(
            recommendation_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "RecommendationListCreateAPIView",
    "RecommendationRetrieveUpdateDestroyAPIView",
]
