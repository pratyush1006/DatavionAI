"""
Recommendation permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


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
    "CanArchiveRecommendation",
    "CanCreateRecommendation",
    "CanDeleteRecommendation",
    "CanRestoreRecommendation",
    "CanUpdateRecommendation",
    "CanViewRecommendation",
    "RecommendationPermission",
]
