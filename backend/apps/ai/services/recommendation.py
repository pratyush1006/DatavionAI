"""
Recommendation services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.ai.models import Recommendation
from apps.platform.accounts.models import User


class RecommendationService:
    """
    Application service responsible for recommendation write operations.

    This service is the single entry point for all recommendation lifecycle
    operations and provides a centralized location for future business
    rules such as:

    - Expiration handling
    - Priority escalation
    - Integration with notification systems
    - Audit logging
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> Recommendation:
        """
        Create a new recommendation.
        """

        recommendation = Recommendation(
            **validated_data,
        )

        recommendation.full_clean()

        recommendation.save()

        return recommendation

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: Recommendation,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> Recommendation:
        """
        Update an existing recommendation.
        """

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: Recommendation,
        performed_by: User | None = None,
    ) -> None:
        """
        Delete a recommendation.
        """

        instance.hard_delete()

    @staticmethod
    @transaction.atomic
    def bulk_create(
        *,
        validated_data_list: list[Mapping[str, Any]],
        performed_by: User | None = None,
    ) -> list[Recommendation]:
        """
        Create multiple recommendations.
        """

        recommendations: list[Recommendation] = []

        for validated_data in validated_data_list:
            recommendation = Recommendation(
                **validated_data,
            )

            recommendation.full_clean()

            recommendation.save()

            recommendations.append(recommendation)

        return recommendations


create_recommendation = RecommendationService.create
update_recommendation = RecommendationService.update
delete_recommendation = RecommendationService.delete


__all__ = [
    "RecommendationService",
    "create_recommendation",
    "delete_recommendation",
    "update_recommendation",
]
