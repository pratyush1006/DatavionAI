from apps.platform.rbac.resolvers import resolve_permissions


class DiagnosisPermission:
    CREATE = "diagnosis.create"
    VIEW = "diagnosis.view"
    UPDATE = "diagnosis.update"
    DELETE = "diagnosis.delete"

    @staticmethod
    def has(*, user, permission, organization):
        return permission in resolve_permissions(user=user, organization=organization)
