from django.urls import path

from apps.accounts.api.views import (
    UserListCreateAPIView,
    UserRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "",
        UserListCreateAPIView.as_view(),
        name="user-list-create",
    ),
    path(
        "<int:user_id>/",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="user-detail",
    ),
]
