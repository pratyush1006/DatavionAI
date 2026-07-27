"""
Factories for Billing tests.
"""

from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal

import factory

from apps.billing.constants import (
    DEFAULT_INVOICE_STATUS,
    ClaimStatus,
    PaymentMethod,
)
from apps.billing.models import (
    InsuranceClaim,
    Invoice,
    InvoiceItem,
    Payment,
)
from apps.clinical.patients.tests.factories import PatientFactory
from apps.platform.organizations.tests.factories import OrganizationFactory


class InvoiceFactory(factory.django.DjangoModelFactory):
    """
    Factory for Invoice model.
    """

    class Meta:
        model = Invoice

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    patient = factory.SubFactory(
        PatientFactory,
    )

    invoice_number = factory.LazyFunction(
        lambda: f"INV{uuid.uuid4().hex[:8].upper()}",
    )

    invoice_date = factory.LazyFunction(
        lambda: date.today(),
    )

    due_date = factory.LazyFunction(
        lambda: date.today(),
    )

    total_amount = Decimal("1000.00")

    paid_amount = Decimal("0.00")

    balance_amount = Decimal("1000.00")

    status = DEFAULT_INVOICE_STATUS

    notes = ""


class InvoiceItemFactory(factory.django.DjangoModelFactory):
    """
    Factory for InvoiceItem model.
    """

    class Meta:
        model = InvoiceItem

    invoice = factory.SubFactory(
        InvoiceFactory,
    )

    description = "Consultation Fee"

    quantity = 1

    unit_price = Decimal("500.00")

    total_price = Decimal("500.00")

    service_code = "CPT-99213"


class PaymentFactory(factory.django.DjangoModelFactory):
    """
    Factory for Payment model.
    """

    class Meta:
        model = Payment

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    invoice = factory.SubFactory(
        InvoiceFactory,
    )

    patient = factory.SubFactory(
        PatientFactory,
    )

    payment_method = PaymentMethod.CASH

    amount = Decimal("500.00")

    payment_date = factory.LazyFunction(
        lambda: date.today(),
    )

    reference_number = ""

    notes = ""

    received_by = None


class InsuranceClaimFactory(factory.django.DjangoModelFactory):
    """
    Factory for InsuranceClaim model.
    """

    class Meta:
        model = InsuranceClaim

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    patient = factory.SubFactory(
        PatientFactory,
    )

    invoice = factory.SubFactory(
        InvoiceFactory,
    )

    insurance_provider = "Test Insurance Co."

    policy_number = factory.LazyFunction(
        lambda: f"POL{uuid.uuid4().hex[:8].upper()}",
    )

    claim_number = factory.LazyFunction(
        lambda: f"CLM{uuid.uuid4().hex[:8].upper()}",
    )

    claim_amount = Decimal("800.00")

    approved_amount = None

    status = ClaimStatus.SUBMITTED

    rejection_reason = ""


__all__ = [
    "InsuranceClaimFactory",
    "InvoiceFactory",
    "InvoiceItemFactory",
    "PaymentFactory",
]
