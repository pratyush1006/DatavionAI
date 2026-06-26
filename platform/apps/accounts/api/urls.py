from django.urls import path

from .views import (
    LoginAPIView,
    MeAPIView,
    UserListCreateAPIView,
    UserRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("me/", MeAPIView.as_view(), name="me"),
    path("users/", UserListCreateAPIView.as_view(), name="user-list-create"),
    path(
        "users/<int:user_id>/",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="user-detail",
    ),
]
