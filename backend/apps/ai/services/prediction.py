"""
Prediction services.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.ai.models import Prediction
from apps.platform.accounts.models import User


class PredictionService:
    """
    Application service responsible for prediction write operations.

    This service is the single entry point for all prediction lifecycle
    operations and provides a centralized location for future business
    rules such as:

    - Validation of risk scores
    - Automatic risk level classification
    - Integration with notification systems
    - Audit logging
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> Prediction:
        """
        Create a new prediction.
        """

        prediction = Prediction(
            **validated_data,
        )

        prediction.full_clean()

        prediction.save()

        return prediction

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: Prediction,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> Prediction:
        """
        Update an existing prediction.
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
        instance: Prediction,
        performed_by: User | None = None,
    ) -> None:
        """
        Delete a prediction.
        """

        instance.hard_delete()

    @staticmethod
    @transaction.atomic
    def bulk_create(
        *,
        validated_data_list: list[Mapping[str, Any]],
        performed_by: User | None = None,
    ) -> list[Prediction]:
        """
        Create multiple predictions.
        """

        predictions: list[Prediction] = []

        for validated_data in validated_data_list:
            prediction = Prediction(
                **validated_data,
            )

            prediction.full_clean()

            prediction.save()

            predictions.append(prediction)

        return predictions


create_prediction = PredictionService.create
update_prediction = PredictionService.update
delete_prediction = PredictionService.delete


__all__ = [
    "PredictionService",
    "create_prediction",
    "delete_prediction",
    "update_prediction",
]
