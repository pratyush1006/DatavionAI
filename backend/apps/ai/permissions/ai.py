"""
AI permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class AIPermission:
    """
    AI module permission codes.
    """

    VIEW = "ai.view"
    CREATE = "ai.create"
    UPDATE = "ai.update"
    DELETE = "ai.delete"
    ARCHIVE = "ai.archive"
    RESTORE = "ai.restore"


class CanViewAI(BasePermission):
    """
    Permission required to view AI resources.
    """

    permission_code = AIPermission.VIEW


class CanCreateAI(BasePermission):
    """
    Permission required to create AI resources.
    """

    permission_code = AIPermission.CREATE


class CanUpdateAI(BasePermission):
    """
    Permission required to update AI resources.
    """

    permission_code = AIPermission.UPDATE


class CanDeleteAI(BasePermission):
    """
    Permission required to delete AI resources.
    """

    permission_code = AIPermission.DELETE


class CanArchiveAI(BasePermission):
    """
    Permission required to archive AI resources.
    """

    permission_code = AIPermission.ARCHIVE


class CanRestoreAI(BasePermission):
    """
    Permission required to restore AI resources.
    """

    permission_code = AIPermission.RESTORE


class PredictionPermission:
    """
    Prediction permission codes.
    """

    VIEW = "prediction.view"
    CREATE = "prediction.create"
    UPDATE = "prediction.update"
    DELETE = "prediction.delete"
    ARCHIVE = "prediction.archive"
    RESTORE = "prediction.restore"


class CanViewPrediction(BasePermission):
    """
    Permission required to view predictions.
    """

    permission_code = PredictionPermission.VIEW


class CanCreatePrediction(BasePermission):
    """
    Permission required to create predictions.
    """

    permission_code = PredictionPermission.CREATE


class CanUpdatePrediction(BasePermission):
    """
    Permission required to update predictions.
    """

    permission_code = PredictionPermission.UPDATE


class CanDeletePrediction(BasePermission):
    """
    Permission required to delete predictions.
    """

    permission_code = PredictionPermission.DELETE


class CanArchivePrediction(BasePermission):
    """
    Permission required to archive predictions.
    """

    permission_code = PredictionPermission.ARCHIVE


class CanRestorePrediction(BasePermission):
    """
    Permission required to restore predictions.
    """

    permission_code = PredictionPermission.RESTORE


class RecommendationPermission:
    """
    Recommendation permission codes.
    """

    VIEW = "recommendation.view"
    CREATE = "recommendation.create"
    UPDATE = "recommendation.update"
    DELETE = "recommendation.delete"
    ARCHIVE = "recommendation.archive"
    RESTORE = "recommendation.restore"


class CanViewRecommendation(BasePermission):
    """
    Permission required to view recommendations.
    """

    permission_code = RecommendationPermission.VIEW


class CanCreateRecommendation(BasePermission):
    """
    Permission required to create recommendations.
    """

    permission_code = RecommendationPermission.CREATE


class CanUpdateRecommendation(BasePermission):
    """
    Permission required to update recommendations.
    """

    permission_code = RecommendationPermission.UPDATE


class CanDeleteRecommendation(BasePermission):
    """
    Permission required to delete recommendations.
    """

    permission_code = RecommendationPermission.DELETE


class CanArchiveRecommendation(BasePermission):
    """
    Permission required to archive recommendations.
    """

    permission_code = RecommendationPermission.ARCHIVE


class CanRestoreRecommendation(BasePermission):
    """
    Permission required to restore recommendations.
    """

    permission_code = RecommendationPermission.RESTORE


__all__ = [
    "AIPermission",
    "CanArchiveAI",
    "CanArchivePrediction",
    "CanArchiveRecommendation",
    "CanCreateAI",
    "CanCreatePrediction",
    "CanCreateRecommendation",
    "CanDeleteAI",
    "CanDeletePrediction",
    "CanDeleteRecommendation",
    "CanRestoreAI",
    "CanRestorePrediction",
    "CanRestoreRecommendation",
    "CanUpdateAI",
    "CanUpdatePrediction",
    "CanUpdateRecommendation",
    "CanViewAI",
    "CanViewPrediction",
    "CanViewRecommendation",
    "PredictionPermission",
    "RecommendationPermission",
]
