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
from rest_framework.views import APIView

from apps.accounts.selectors import (
    get_user_by_id,
    get_users,
)
from apps.accounts.serializers import (
    LoginSerializer,
    MeSerializer,
    UserCreateSerializer,
    UserDetailSerializer,
    UserListSerializer,
    UserUpdateSerializer,
)
from apps.accounts.services import (
    create_user,
    generate_tokens,
    update_user,
)


class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["Authentication"],
        request=LoginSerializer,
        responses=200,
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        tokens = generate_tokens(user)

        return Response(
            {
                "access": tokens["access"],
                "refresh": tokens["refresh"],
                "user": MeSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Authentication"])
    def get(self, request):
        return Response(
            MeSerializer(request.user).data
        )


class UserListCreateAPIView(ListCreateAPIView):
    """
    GET  -> List Users
    POST -> Create User
    """

    permission_classes = [IsAuthenticated]

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )

    ordering = (
        "username",
    )

    ordering_fields = (
        "username",
        "email",
        "created_at",
    )

    filterset_fields = (
        "organization",
    )

    @extend_schema(tags=["Users"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(tags=["Users"])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = create_user(
            serializer.validated_data.copy()
        )

        return Response(
            UserDetailSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self):
        return get_users(self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer

        return UserListSerializer


class UserRetrieveUpdateDestroyAPIView(
    RetrieveUpdateDestroyAPIView
):
    """
    GET
    PUT
    PATCH
    DELETE
    """

    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "user_id"

    def get_object(self):
        return get_user_by_id(
            self.kwargs["user_id"],
            self.request.user,
        )

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return UserUpdateSerializer

        return UserDetailSerializer

    @extend_schema(tags=["Users"])
    def get(self, request, *args, **kwargs):
        return self.retrieve(
            request,
            *args,
            **kwargs,
        )

    @extend_schema(tags=["Users"])
    def patch(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        user = update_user(
            user,
            serializer.validated_data.copy(),
        )

        return Response(
            UserDetailSerializer(user).data
        )

    @extend_schema(tags=["Users"])
    def put(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=False,
        )

        serializer.is_valid(raise_exception=True)

        user = update_user(
            user,
            serializer.validated_data.copy(),
        )

        return Response(
            UserDetailSerializer(user).data
        )

    @extend_schema(tags=["Users"])
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )