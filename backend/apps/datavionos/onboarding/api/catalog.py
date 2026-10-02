from __future__ import annotations

from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.common.api.responses import success_response
from apps.platform.organizations.constants import (
    ORGANIZATION_CATEGORY_TYPES,
    OrganizationCategory,
    OrganizationSize,
    OrganizationType,
)


class OrganizationCatalogAPIView(APIView):
    """Return the canonical category, type and size catalogs for onboarding."""

    permission_classes = (AllowAny,)

    def get(self, request: Request):
        type_categories = {
            member.value: category.value
            for category, members in ORGANIZATION_CATEGORY_TYPES.items()
            for member in members
        }
        return success_response(
            data={
                "categories": [
                    {"code": choice.value, "name": str(choice.label)}
                    for choice in OrganizationCategory
                ],
                "types": [
                    {
                        "code": choice.value,
                        "name": str(choice.label),
                        "category": type_categories.get(choice.value, ""),
                    }
                    for choice in OrganizationType
                ],
                "sizes": [
                    {"code": choice.value, "name": str(choice.label)}
                    for choice in OrganizationSize
                ],
            },
            request=request,
        )


__all__ = ["OrganizationCatalogAPIView"]
