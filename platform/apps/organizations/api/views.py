from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.organizations.selectors import (
    get_organization_by_id,
    get_organizations,
)
from apps.organizations.serializers import (
    OrganizationCreateSerializer,
    OrganizationDetailSerializer,
    OrganizationListSerializer,
    OrganizationUpdateSerializer,
)
from apps.organizations.services import (
    create_organization,
    delete_organization,
    update_organization,
)
from apps.rbac.permissions import (
    CanAddOrganizations,
    CanChangeOrganizations,
    CanDeleteOrganizations,
    CanViewOrganizations,
)


class OrganizationListCreateAPIView(ListCreateAPIView):
    """
    GET  -> List Organizations
    POST -> Create Organization
    """

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    search_fields = (
        "name",
        "code",
        "city",
        "state",
        "country",
    )

    ordering = (
        "name",
    )

    ordering_fields = (
        "name",
        "code",
        "city",
        "created_at",
    )

    filterset_fields = (
        "organization_type",
        "country",
        "is_active",
    )

    def get_permissions(self):

        if self.request.method == "GET":
            permission_classes = [
                IsAuthenticated,
                CanViewOrganizations,
            ]
        else:
            permission_classes = [
                IsAuthenticated,
                CanAddOrganizations,
            ]

        return [
            permission()
            for permission in permission_classes
        ]

    def get_queryset(self):
        return get_organizations()

    def get_serializer_class(self):

        if self.request.method == "POST":
            return OrganizationCreateSerializer

        return OrganizationListSerializer

    @extend_schema(tags=["Organizations"])
    def get(self, request, *args, **kwargs):
        return self.list(
            request,
            *args,
            **kwargs,
        )

    @extend_schema(tags=["Organizations"])
    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        organization = create_organization(
            serializer.validated_data.copy()
        )

        return Response(
            OrganizationDetailSerializer(
                organization
            ).data,
            status=status.HTTP_201_CREATED,
        )


class OrganizationRetrieveUpdateDestroyAPIView(
    RetrieveUpdateDestroyAPIView
):
    """
    GET
    PUT
    PATCH
    DELETE
    """

    lookup_url_kwarg = "organization_id"

    def get_permissions(self):

        if self.request.method == "GET":
            permission_classes = [
                IsAuthenticated,
                CanViewOrganizations,
            ]

        elif self.request.method in (
            "PUT",
            "PATCH",
        ):
            permission_classes = [
                IsAuthenticated,
                CanChangeOrganizations,
            ]

        else:
            permission_classes = [
                IsAuthenticated,
                CanDeleteOrganizations,
            ]

        return [
            permission()
            for permission in permission_classes
        ]

    def get_object(self):
        return get_organization_by_id(
            self.kwargs["organization_id"]
        )

    def get_serializer_class(self):

        if self.request.method in (
            "PUT",
            "PATCH",
        ):
            return OrganizationUpdateSerializer

        return OrganizationDetailSerializer

    @extend_schema(tags=["Organizations"])
    def get(self, request, *args, **kwargs):
        return self.retrieve(
            request,
            *args,
            **kwargs,
        )

    @extend_schema(tags=["Organizations"])
    def patch(self, request, *args, **kwargs):

        organization = self.get_object()

        serializer = self.get_serializer(
            organization,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        organization = update_organization(
            organization,
            serializer.validated_data.copy(),
        )

        return Response(
            OrganizationDetailSerializer(
                organization
            ).data
        )

    @extend_schema(tags=["Organizations"])
    def put(self, request, *args, **kwargs):

        organization = self.get_object()

        serializer = self.get_serializer(
            organization,
            data=request.data,
            partial=False,
        )

        serializer.is_valid(
            raise_exception=True
        )

        organization = update_organization(
            organization,
            serializer.validated_data.copy(),
        )

        return Response(
            OrganizationDetailSerializer(
                organization
            ).data
        )

    @extend_schema(tags=["Organizations"])
    def delete(self, request, *args, **kwargs):

        organization = self.get_object()

        delete_organization(
            organization
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )