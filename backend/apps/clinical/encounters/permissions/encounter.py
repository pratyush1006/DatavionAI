from apps.platform.rbac.resolvers import resolve_permissions


class EncounterPermission:
    CREATE = "encounter.create"
    VIEW = "encounter.view"
    UPDATE = "encounter.update"
    DELETE = "encounter.delete"
    TRANSITION = "encounter.transition"

    @staticmethod
    def has(*, user, permission, organization):
        return permission in resolve_permissions(
            user=user,
            organization=organization,
        )
