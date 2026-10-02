from apps.platform.rbac.resolvers import resolve_permissions


class PharmacyPolicy:
    @staticmethod
    def allowed(*, user, permission, organization):
        return permission in resolve_permissions(user=user, organization=organization)

    @classmethod
    def can_view(cls, *, user, organization):
        return cls.allowed(
            user=user, permission="pharmacy.view", organization=organization
        )

    @classmethod
    def can_inventory(cls, *, user, organization):
        return cls.allowed(
            user=user, permission="pharmacy.inventory", organization=organization
        )

    @classmethod
    def can_purchasing(cls, *, user, organization):
        return cls.allowed(
            user=user, permission="pharmacy.purchasing", organization=organization
        )

    @classmethod
    def can_dispense(cls, *, user, organization):
        return cls.allowed(
            user=user, permission="pharmacy.dispense", organization=organization
        )

    @classmethod
    def can_manage_controlled(cls, *, user, organization):
        return cls.allowed(
            user=user, permission="pharmacy.controlled", organization=organization
        )

    @classmethod
    def can_manage_recalls(cls, *, user, organization):
        return cls.allowed(
            user=user, permission="pharmacy.recall", organization=organization
        )

    @classmethod
    def can_approve_purchasing(cls, *, user, organization):
        return cls.allowed(
            user=user,
            permission="pharmacy.purchasing.approve",
            organization=organization,
        )
