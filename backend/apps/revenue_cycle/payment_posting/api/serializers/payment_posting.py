"""
Serializers for the PaymentPosting module.
"""

from __future__ import annotations

from apps.revenue_cycle.payment_posting.models import PaymentPosting
from rest_framework import serializers

WRITE_FIELDS: tuple[str, ...] = (
    "patient",
    "payment",
    "invoice",
    "amount",
    "posting_date",
    "status",
    "posted_by",
    "notes",
)

DETAIL_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "payment",
    "invoice",
    "amount",
    "posting_date",
    "status",
    "posted_by",
    "notes",
    "organization",
    "is_active",
    "created_at",
    "updated_at",
)

LIST_FIELDS: tuple[str, ...] = (
    "organization",
    "patient",
    "payment",
    "invoice",
    "amount",
    "posting_date",
    "status",
    "posted_by",
    "notes",
)

READ_ONLY_FIELDS: tuple[str, ...] = ("id", "created_at", "updated_at")


class PaymentPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPosting
        fields = DETAIL_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PaymentPostingCreateSerializer(PaymentPostingSerializer):
    class Meta(PaymentPostingSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PaymentPostingUpdateSerializer(PaymentPostingSerializer):
    class Meta(PaymentPostingSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS


class PaymentPostingListSerializer(PaymentPostingSerializer):
    class Meta(PaymentPostingSerializer.Meta):
        fields = LIST_FIELDS
        read_only_fields = READ_ONLY_FIELDS


PaymentPostingDetailSerializer = PaymentPostingSerializer


__all__ = [
    "PaymentPostingCreateSerializer",
    "PaymentPostingDetailSerializer",
    "PaymentPostingListSerializer",
    "PaymentPostingSerializer",
    "PaymentPostingUpdateSerializer",
]
