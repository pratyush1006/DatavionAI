"""
SaaS Billing Account API serializers.

Handles:

- Billing account representation
- Billing profile updates
- Billing configuration
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.saas_billing.models import (
    BillingAccount,
)


class BillingAccountSerializer(
    serializers.ModelSerializer,
):
    """
    Billing account read serializer.
    """

    class Meta:
        model = BillingAccount

        fields = [
            "id",
            "organization",
            "legal_name",
            "billing_email",
            "billing_phone",
            "billing_contact_name",
            "gst_number",
            "vat_number",
            "tax_id",
            "billing_address",
            "tax_configuration",
            "payment_terms",
            "currency",
            "payment_provider",
            "auto_charge_enabled",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "organization",
            "currency",
            "status",
            "created_at",
            "updated_at",
        ]


class BillingAccountUpdateSerializer(
    serializers.Serializer,
):
    """
    Billing profile update serializer.

    Used with:

    BillingAccountService.update_billing_profile()
    """

    legal_name = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    billing_email = serializers.EmailField(
        required=False,
        allow_blank=True,
    )

    billing_phone = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    billing_contact_name = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    gst_number = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    vat_number = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    tax_id = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    billing_address = serializers.JSONField(
        required=False,
    )

    tax_configuration = serializers.JSONField(
        required=False,
    )

    payment_terms = serializers.JSONField(
        required=False,
    )

    class Meta:
        fields = [
            "legal_name",
            "billing_email",
            "billing_phone",
            "billing_contact_name",
            "gst_number",
            "vat_number",
            "tax_id",
            "billing_address",
            "tax_configuration",
            "payment_terms",
        ]


__all__ = [
    "BillingAccountSerializer",
    "BillingAccountUpdateSerializer",
]
