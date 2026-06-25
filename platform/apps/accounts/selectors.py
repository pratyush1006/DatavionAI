from apps.accounts.models import User


def get_user_by_id(user_id: int):
    return User.objects.select_related("organization").get(id=user_id)