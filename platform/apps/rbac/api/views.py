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
    
from rest_framework.views import APIView

from apps.rbac.selectors import (
    get_user_by_id,
    get_role_by_id,
)

from apps.rbac.serializers import (
    UserRoleSerializer,
    UserRoleDetailSerializer,
)

from apps.rbac.services import (
    assign_role_to_user,
    remove_role_from_user,
)

class UserRoleAPIView(APIView):
    """
    GET  -> List roles assigned to a user
    POST -> Assign role to a user
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["RBAC"])
    def get(self, request, user_id):
        user = get_user_by_id(user_id)

        return Response(
            UserRoleDetailSerializer(user).data
        )

    @extend_schema(
        tags=["RBAC"],
        request=UserRoleSerializer,
    )
    def post(self, request, user_id):

        user = get_user_by_id(user_id)

        serializer = UserRoleSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        role = get_role_by_id(
            serializer.validated_data["role_id"]
        )

        assign_role_to_user(
            user,
            role,
        )

        return Response(
            UserRoleDetailSerializer(user).data,
            status=status.HTTP_200_OK,
        )


class UserRoleDeleteAPIView(APIView):
    """
    DELETE -> Remove role from user
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["RBAC"])
    def delete(
        self,
        request,
        user_id,
        role_id,
    ):

        user = get_user_by_id(user_id)

        role = get_role_by_id(role_id)

        remove_role_from_user(
            user,
            role,
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )