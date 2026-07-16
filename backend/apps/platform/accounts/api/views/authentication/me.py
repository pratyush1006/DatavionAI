"""
Current user API view.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.responses import success_response
from apps.platform.accounts.api.serializers.authentication import (
    MeSerializer,
)

AUTH_TAG: Final = ("Authentication",)


@extend_schema(
    tags=AUTH_TAG,
    summary="Current User",
    description="Return the currently authenticated user.",
    responses={
        200: MeSerializer,
    },
)
class MeAPIView(APIView):
    """
    Retrieve the authenticated user.
    """

    permission_classes = (IsAuthenticated,)

    serializer_class = MeSerializer

    def get(
        self,
        request: Request,
    ) -> Response:
        """
        Return the authenticated user.
        """

        serializer = self.serializer_class(
            instance=request.user,
        )

        return success_response(
            data=serializer.data,
        )


__all__ = [
    "MeAPIView",
]
