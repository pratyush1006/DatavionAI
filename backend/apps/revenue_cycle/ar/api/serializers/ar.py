"""
Serializers for the AccountsReceivable module.
"""

from __future__ import annotations

from apps.revenue_cycle.ar.models import AccountsReceivable
from rest_framework import serializers

WRITE_FIELDS: tuple[str, ...] = (
    "patient",
    "invoice",
    "billed_amount",
    "paid_amount",
    "adjustment_amount",
    "balance",
    "status",
    "due_date",
    "last_activity_date",
    "assigned_to",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "invoice",
    "billed_amount",
    "paid_amount",
    "adjustment_amount",
    "balance",
    "status",
    "due_date",
    "last_activity_date",
    "assigned_to",
    "organization",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "invoice",
    "billed_amount",
    "paid_amount",
    "adjustment_amount",
    "balance",
    "status",
    "due_date",
    "last_activity_date",
    "assigned_to",
)

READ_ONLY_FIELDS: tuple[str, ...] = ("id", "created_at", "updated_at")


class AccountsReceivableSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountsReceivable
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class AccountsReceivableCreateSerializer(AccountsReceivableSerializer):
    class Meta(AccountsReceivableSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class AccountsReceivableUpdateSerializer(AccountsReceivableSerializer):
    class Meta(AccountsReceivableSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class AccountsReceivableListSerializer(AccountsReceivableSerializer):
    class Meta(AccountsReceivableSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


AccountsReceivableDetailSerializer = AccountsReceivableSerializer


__all__ = [
    "AccountsReceivableCreateSerializer",
    "AccountsReceivableDetailSerializer",
    "AccountsReceivableListSerializer",
    "AccountsReceivableSerializer",
    "AccountsReceivableUpdateSerializer",
]
