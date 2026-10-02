"""DRF Address permission."""

from __future__ import annotations

from rest_framework.permissions import BasePermission

from apps.patient_management.addresses.policies import AddressPolicy


class AddressPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return AddressPolicy.can_access(user=request.user, address=obj)
