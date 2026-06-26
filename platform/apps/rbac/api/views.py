from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.rbac.selectors import (
    get_role_by_id,
    get_roles,
)
from apps.rbac.serializers import (
    RoleCreateSerializer,
    RoleDetailSerializer,
    RoleListSerializer,
    RoleUpdateSerializer,
)
from apps.rbac.services import (
    create_role,
    delete_role,
    update_role,
)


class RoleListCreateAPIView(ListCreateAPIView):
    """
    GET  -> List Roles
    POST -> Create Role
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_roles()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return RoleCreateSerializer

        return RoleListSerializer

    @extend_schema(tags=["RBAC"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(tags=["RBAC"])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        role = create_role(
            serializer.validated_data.copy()
        )

        return Response(
            RoleDetailSerializer(role).data,
            status=status.HTTP_201_CREATED,
        )


class RoleRetrieveUpdateDestroyAPIView(
    RetrieveUpdateDestroyAPIView
):
    """
    GET
    PATCH
    PUT
    DELETE
    """

    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "role_id"

    def get_object(self):
        return get_role_by_id(
            self.kwargs["role_id"]
        )

    def get_serializer_class(self):
        if self.request.method in (
            "PUT",
            "PATCH",
        ):
            return RoleUpdateSerializer

        return RoleDetailSerializer

    @extend_schema(tags=["RBAC"])
    def get(self, request, *args, **kwargs):
        return self.retrieve(
            request,
            *args,
            **kwargs,
        )

    @extend_schema(tags=["RBAC"])
    def patch(self, request, *args, **kwargs):
        role = self.get_object()

        serializer = self.get_serializer(
            role,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        role = update_role(
            role,
            serializer.validated_data.copy(),
        )

        return Response(
            RoleDetailSerializer(role).data
        )

    @extend_schema(tags=["RBAC"])
    def put(self, request, *args, **kwargs):
        role = self.get_object()

        serializer = self.get_serializer(
            role,
            data=request.data,
            partial=False,
        )

        serializer.is_valid(
            raise_exception=True
        )

        role = update_role(
            role,
            serializer.validated_data.copy(),
        )

        return Response(
            RoleDetailSerializer(role).data
        )

    @extend_schema(tags=["RBAC"])
    def delete(self, request, *args, **kwargs):
        role = self.get_object()

        delete_role(role)

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )