"""
SaaS Billing constants.

Centralized billing domain constants
for DatavionOS.

Contains:

- Subscription states
- Invoice states
- Payment states
- Providers
- Billing cycles
- Healthcare SaaS plans
- Usage metrics
- Billing events
"""

from __future__ import annotations

# ==========================================================================
# Billing Cycles
# ==========================================================================

BILLING_CYCLE_MONTHLY = "monthly"

BILLING_CYCLE_YEARLY = "yearly"


BILLING_CYCLES = (
    BILLING_CYCLE_MONTHLY,
    BILLING_CYCLE_YEARLY,
)


# ==========================================================================
# Subscription Status
# ==========================================================================

SUBSCRIPTION_TRIAL = "TRIAL"

SUBSCRIPTION_ACTIVE = "ACTIVE"

SUBSCRIPTION_PAST_DUE = "PAST_DUE"

SUBSCRIPTION_SUSPENDED = "SUSPENDED"

SUBSCRIPTION_CANCELLED = "CANCELLED"

SUBSCRIPTION_EXPIRED = "EXPIRED"


SUBSCRIPTION_STATUSES = (
    SUBSCRIPTION_TRIAL,
    SUBSCRIPTION_ACTIVE,
    SUBSCRIPTION_PAST_DUE,
    SUBSCRIPTION_SUSPENDED,
    SUBSCRIPTION_CANCELLED,
    SUBSCRIPTION_EXPIRED,
)


# ==========================================================================
# Invoice Status
# ==========================================================================

INVOICE_DRAFT = "DRAFT"

INVOICE_ISSUED = "ISSUED"

INVOICE_SENT = "SENT"

INVOICE_PARTIALLY_PAID = "PARTIALLY_PAID"

INVOICE_PAID = "PAID"

INVOICE_OVERDUE = "OVERDUE"

INVOICE_FAILED = "FAILED"

INVOICE_CANCELLED = "CANCELLED"

INVOICE_REFUNDED = "REFUNDED"


INVOICE_STATUSES = (
    INVOICE_DRAFT,
    INVOICE_ISSUED,
    INVOICE_SENT,
    INVOICE_PARTIALLY_PAID,
    INVOICE_PAID,
    INVOICE_OVERDUE,
    INVOICE_FAILED,
    INVOICE_CANCELLED,
    INVOICE_REFUNDED,
)


# ==========================================================================
# Payment Status
# ==========================================================================

PAYMENT_PENDING = "PENDING"

PAYMENT_PROCESSING = "PROCESSING"

PAYMENT_SUCCESS = "SUCCESS"

PAYMENT_FAILED = "FAILED"

PAYMENT_CANCELLED = "CANCELLED"

PAYMENT_REFUNDED = "REFUNDED"

PAYMENT_PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"


PAYMENT_STATUSES = (
    PAYMENT_PENDING,
    PAYMENT_PROCESSING,
    PAYMENT_SUCCESS,
    PAYMENT_FAILED,
    PAYMENT_CANCELLED,
    PAYMENT_REFUNDED,
    PAYMENT_PARTIALLY_REFUNDED,
)


# ==========================================================================
# Payment Providers
# ==========================================================================

PROVIDER_STRIPE = "STRIPE"

PROVIDER_RAZORPAY = "RAZORPAY"

PROVIDER_PAYPAL = "PAYPAL"

PROVIDER_BANK = "BANK"

PROVIDER_MANUAL = "MANUAL"


PAYMENT_PROVIDERS = (
    PROVIDER_STRIPE,
    PROVIDER_RAZORPAY,
    PROVIDER_PAYPAL,
    PROVIDER_BANK,
    PROVIDER_MANUAL,
)


# ==========================================================================
# Healthcare SaaS Plans
# ==========================================================================

PLAN_FREE = "FREE"

PLAN_CLINIC = "CLINIC"

PLAN_HOSPITAL = "HOSPITAL"

PLAN_PHARMACY = "PHARMACY"

PLAN_MEDICAL_STORE = "MEDICAL_STORE"

PLAN_LABORATORY = "LABORATORY"

PLAN_ENTERPRISE = "ENTERPRISE"


HEALTHCARE_PLANS = (
    PLAN_FREE,
    PLAN_CLINIC,
    PLAN_HOSPITAL,
    PLAN_PHARMACY,
    PLAN_MEDICAL_STORE,
    PLAN_LABORATORY,
    PLAN_ENTERPRISE,
)


# ==========================================================================
# Usage Metrics
# ==========================================================================

USAGE_USERS = "USERS"

USAGE_STORAGE = "STORAGE_GB"

USAGE_PATIENTS = "PATIENTS"

USAGE_APPOINTMENTS = "APPOINTMENTS"

USAGE_ENCOUNTERS = "ENCOUNTERS"

USAGE_PRESCRIPTIONS = "PRESCRIPTIONS"

USAGE_LAB_ORDERS = "LAB_ORDERS"

USAGE_IMAGING = "IMAGING_STUDIES"

USAGE_TELEMEDICINE = "TELEMEDICINE_MINUTES"

USAGE_PHARMACY_ORDERS = "PHARMACY_ORDERS"

USAGE_INVENTORY = "INVENTORY_TRANSACTIONS"

USAGE_AI_REQUESTS = "AI_REQUESTS"

USAGE_AI_TOKENS = "AI_TOKENS"

USAGE_AI_DOCUMENTS = "AI_DOCUMENTS"

USAGE_API_CALLS = "API_CALLS"


USAGE_METRICS = (
    USAGE_USERS,
    USAGE_STORAGE,
    USAGE_PATIENTS,
    USAGE_APPOINTMENTS,
    USAGE_ENCOUNTERS,
    USAGE_PRESCRIPTIONS,
    USAGE_LAB_ORDERS,
    USAGE_IMAGING,
    USAGE_TELEMEDICINE,
    USAGE_PHARMACY_ORDERS,
    USAGE_INVENTORY,
    USAGE_AI_REQUESTS,
    USAGE_AI_TOKENS,
    USAGE_AI_DOCUMENTS,
    USAGE_API_CALLS,
)


# ==========================================================================
# Billing Events
# ==========================================================================

EVENT_SUBSCRIPTION_CREATED = "subscription.created"

EVENT_SUBSCRIPTION_ACTIVATED = "subscription.activated"

EVENT_SUBSCRIPTION_CANCELLED = "subscription.cancelled"

EVENT_INVOICE_CREATED = "invoice.created"

EVENT_INVOICE_PAID = "invoice.paid"

EVENT_PAYMENT_SUCCESS = "payment.success"

EVENT_PAYMENT_FAILED = "payment.failed"

EVENT_USAGE_RECORDED = "usage.recorded"


# ==========================================================================
# Currency
# ==========================================================================

CURRENCY_USD = "USD"

CURRENCY_INR = "INR"

CURRENCY_EUR = "EUR"

CURRENCY_GBP = "GBP"


SUPPORTED_CURRENCIES = (
    CURRENCY_USD,
    CURRENCY_INR,
    CURRENCY_EUR,
    CURRENCY_GBP,
)


__all__ = [
    "BILLING_CYCLES",
    "SUBSCRIPTION_STATUSES",
    "INVOICE_STATUSES",
    "PAYMENT_STATUSES",
    "PAYMENT_PROVIDERS",
    "HEALTHCARE_PLANS",
    "USAGE_METRICS",
    "SUPPORTED_CURRENCIES",
]
