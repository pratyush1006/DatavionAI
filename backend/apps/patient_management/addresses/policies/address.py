"""Address tenant/organization policy."""

from __future__ import annotations


class AddressPolicy:
    @staticmethod
    def can_access(*, user, address):
        if not getattr(user, "is_authenticated", False):
            return False
        if getattr(user, "is_superuser", False):
            return True
        if getattr(user, "tenant_id", None) is not None and str(user.tenant_id) != str(
            address.tenant_id
        ):
            return False
        if getattr(user, "organization_id", None) is not None and str(
            user.organization_id
        ) != str(address.organization_id):
            return False
        return True
