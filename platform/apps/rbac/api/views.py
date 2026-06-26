from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.rbac.selectors import (
    get_permission_by_id,
    get_permissions,
    get_permissions_by_ids,
    get_role_by_id,
    get_roles,
    get_user_by_id,
)
from apps.rbac.serializers import (
    PermissionListSerializer,
    RoleCreateSerializer,
    RoleDetailSerializer,
    RoleListSerializer,
    RolePermissionSerializer,
    RoleUpdateSerializer,
    UserRoleDetailSerializer,
    UserRoleSerializer,
)
from apps.rbac.services import (
    assign_permissions_to_role,
    assign_role_to_user,
    create_role,
    delete_role,
    get_role_permissions,
    remove_permission_from_role,
    remove_role_from_user,
    update_role,
)

# =====================================================
# ROLE CRUD
# =====================================================


class RoleListCreateAPIView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    search_fields = ("name",)

    ordering = ("name",)

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

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        role = create_role(serializer.validated_data.copy())

        return Response(
            RoleDetailSerializer(role).data,
            status=status.HTTP_201_CREATED,
        )


class RoleRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "role_id"

    def get_object(self):
        return get_role_by_id(self.kwargs["role_id"])

    def get_serializer_class(self):

        if self.request.method in (
            "PUT",
            "PATCH",
        ):
            return RoleUpdateSerializer

        return RoleDetailSerializer

    @extend_schema(tags=["RBAC"])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(tags=["RBAC"])
    def patch(self, request, *args, **kwargs):

        role = self.get_object()

        serializer = self.get_serializer(
            role,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        role = update_role(
            role,
            serializer.validated_data.copy(),
        )

        return Response(RoleDetailSerializer(role).data)

    @extend_schema(tags=["RBAC"])
    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

    @extend_schema(tags=["RBAC"])
    def delete(self, request, *args, **kwargs):

        role = self.get_object()

        delete_role(role)

        return Response(status=status.HTTP_204_NO_CONTENT)


# =====================================================
# USER ROLE
# =====================================================


class UserRoleAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["RBAC"])
    def get(self, request, user_id):

        user = get_user_by_id(user_id)

        return Response(UserRoleDetailSerializer(user).data)

    @extend_schema(
        tags=["RBAC"],
        request=UserRoleSerializer,
    )
    def post(self, request, user_id):

        user = get_user_by_id(user_id)

        serializer = UserRoleSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        role = get_role_by_id(serializer.validated_data["role_id"])

        assign_role_to_user(
            user,
            role,
        )

        return Response(UserRoleDetailSerializer(user).data)


class UserRoleDeleteAPIView(APIView):

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

        return Response(status=status.HTTP_204_NO_CONTENT)


# =====================================================
# PERMISSIONS
# =====================================================


class PermissionListAPIView(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PermissionListSerializer

    def get_queryset(self):
        return get_permissions()


class RolePermissionAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["RBAC"])
    def get(self, request, role_id):

        role = get_role_by_id(role_id)

        return Response(
            PermissionListSerializer(
                get_role_permissions(role),
                many=True,
            ).data
        )

    @extend_schema(
        tags=["RBAC"],
        request=RolePermissionSerializer,
    )
    def post(self, request, role_id):

        role = get_role_by_id(role_id)

        serializer = RolePermissionSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        permissions = get_permissions_by_ids(
            serializer.validated_data["permission_ids"]
        )

        assign_permissions_to_role(
            role,
            permissions,
        )

        return Response(RoleDetailSerializer(role).data)


class RolePermissionDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["RBAC"])
    def delete(
        self,
        request,
        role_id,
        permission_id,
    ):

        role = get_role_by_id(role_id)

        permission = get_permission_by_id(permission_id)

        remove_permission_from_role(
            role,
            permission,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
