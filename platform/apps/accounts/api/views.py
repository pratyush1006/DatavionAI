from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from apps.accounts.serializers import (
    LoginSerializer,
    MeSerializer,
    UserListSerializer,
    UserDetailSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
)

from apps.accounts.services import (
    generate_tokens,
    create_user,
    update_user,
)

from apps.accounts.selectors import (
    get_users,
    get_user_by_id,
)


class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
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

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)


class UserListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_users()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        return UserListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # IMPORTANT: pass a copy so validated_data is not mutated
        validated_data = serializer.validated_data.copy()

        user = create_user(validated_data)

        return Response(
            UserDetailSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class UserRetrieveUpdateDestroyAPIView(
    RetrieveUpdateDestroyAPIView
):
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "user_id"

    def get_object(self):
        return get_user_by_id(
            self.kwargs["user_id"]
        )

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UserUpdateSerializer
        return UserDetailSerializer

    def update(self, request, *args, **kwargs):
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

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )