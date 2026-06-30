"""
API views for retrieving, updating, and deleting organizations.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.common.api.responses import (
    no_content_response,
    success_response,
)
from apps.organizations.api.serializers import (
    OrganizationDetailSerializer,
    OrganizationUpdateSerializer,
)
from apps.organizations.models import Organization
from apps.organizations.selectors import (
    get_organization_by_id,
)
from apps.organizations.services import (
    delete_organization,
    update_organization,
)
from apps.rbac.permissions import (
    CanChangeOrganizations,
    CanDeleteOrganizations,
    CanViewOrganizations,
)

ORGANIZATION_TAG: Final = ("Organizations",)


class OrganizationRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete an organization.
    """

    lookup_url_kwarg = "organization_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewOrganizations,
        ),
        "PUT": (
            IsAuthenticated,
            CanChangeOrganizations,
        ),
        "PATCH": (
            IsAuthenticated,
            CanChangeOrganizations,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteOrganizations,
        ),
    }

    def get_permissions(self) -> list[BasePermission]:
        """
        Return permissions based on request method.
        """
        permission_classes = self.permission_classes_map[self.request.method]
        return [permission() for permission in permission_classes]

    def get_object(self) -> Organization:
        """
        Return the requested organization.
        """
        return get_organization_by_id(
            organization_id=self.kwargs[self.lookup_url_kwarg],
        )

    def get_serializer_class(self) -> type[BaseSerializer]:
        """
        Return serializer for current request.
        """
        if self.request.method in ("PUT", "PATCH"):
            return OrganizationUpdateSerializer

        return OrganizationDetailSerializer

    def _update(
        self,
        request: Request,
        *,
        partial: bool = False,
    ) -> Response:
        """
        Shared implementation for PUT and PATCH.
        """

        organization = self.get_object()

        serializer = self.get_serializer(
            organization,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        organization = update_organization(
            organization=organization,
            validated_data=serializer.validated_data,
        )

        return success_response(
            data=OrganizationDetailSerializer(
                organization,
            ).data,
            message="Organization updated successfully.",
        )

    @extend_schema(tags=ORGANIZATION_TAG)
    def get(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Retrieve organization.
        """
        return self.retrieve(
            request,
            *args,
            **kwargs,
        )

    @extend_schema(tags=ORGANIZATION_TAG)
    def put(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Replace organization.
        """
        return self._update(
            request,
            partial=False,
        )

    @extend_schema(tags=ORGANIZATION_TAG)
    def patch(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Partially update organization.
        """
        return self._update(
            request,
            partial=True,
        )

    @extend_schema(tags=ORGANIZATION_TAG)
    def delete(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Delete organization.
        """
        delete_organization(
            organization=self.get_object(),
        )

        return no_content_response()
