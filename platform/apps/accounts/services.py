from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User


def generate_tokens(user):
    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def create_user(validated_data):
    password = validated_data.pop("password", None)

    if password is None:
        raise ValueError("Password is required.")

    user = User.objects.create(
        password=make_password(password),
        **validated_data,
    )

    return user


def update_user(user, validated_data):
    password = validated_data.pop("password", None)

    for field, value in validated_data.items():
        setattr(user, field, value)

    if password:
        user.set_password(password)

    user.save()

    return user