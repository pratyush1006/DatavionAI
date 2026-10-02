"""
Organization catalog API views.

These endpoints expose the canonical organization classification
choices used by the organization registration flow.
"""

from __future__ import annotations

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.platform.organizations.constants import (
    OrganizationCategory,
    OrganizationSize,
    OrganizationType,
)


def _choices_response(choices) -> Response:
    """Convert Django TextChoices into the frontend catalog shape."""
    return Response(
        [
            {
                "id": value,
                "name": label,
                "code": value,
            }
            for value, label in choices.choices
        ],
    )


class OrganizationTypeCatalogAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return _choices_response(OrganizationType)


class OrganizationCategoryCatalogAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return _choices_response(OrganizationCategory)


class OrganizationSizeCatalogAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return _choices_response(OrganizationSize)


__all__ = [
    "OrganizationCategoryCatalogAPIView",
    "OrganizationSizeCatalogAPIView",
    "OrganizationTypeCatalogAPIView",
]
