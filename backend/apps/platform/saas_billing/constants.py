"""SaaS Billing domain constants for DatavionOS.

This module contains billing-domain vocabulary only.

Plan identity, healthcare segments, pricing, entitlements and usage limits
remain owned by the canonical ``Plan`` model and SaaS Billing workflows.
Currency remains owned by ``apps.common.finance.currency``.

The module intentionally does not define:
- PLAN_* constants
- HEALTHCARE_PLANS
- healthcare-specific module maps
- currency implementations
- organization entitlement maps
"""

from __future__ import annotations

# ============================================================================
# Billing Cycles
# ============================================================================

BILLING_CYCLE_MONTHLY = "monthly"
BILLING_CYCLE_YEARLY = "yearly"

BILLING_CYCLES = (
    BILLING_CYCLE_MONTHLY,
    BILLING_CYCLE_YEARLY,
)


# ============================================================================
# Subscription Status
# ============================================================================

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


# ============================================================================
# Invoice Status
# ============================================================================

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


# ============================================================================
# Payment Status
# ============================================================================

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


# ============================================================================
# Payment Providers
# ============================================================================

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


# ============================================================================
# Usage Metrics
# ============================================================================

USAGE_USERS = "USERS"
USAGE_ACTIVE_USERS = "ACTIVE_USERS"
USAGE_BRANCHES = "BRANCHES"
USAGE_DOCTORS = "DOCTORS"
USAGE_STAFF = "STAFF"
USAGE_STORAGE = "STORAGE_GB"
USAGE_PATIENTS = "PATIENTS"
USAGE_ACTIVE_PATIENTS = "ACTIVE_PATIENTS"
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
    USAGE_ACTIVE_USERS,
    USAGE_BRANCHES,
    USAGE_DOCTORS,
    USAGE_STAFF,
    USAGE_STORAGE,
    USAGE_PATIENTS,
    USAGE_ACTIVE_PATIENTS,
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


# ============================================================================
# Subscription Events
# ============================================================================

EVENT_SUBSCRIPTION_CREATED = "subscription.created"
EVENT_SUBSCRIPTION_STARTED = "subscription.started"
EVENT_SUBSCRIPTION_TRIAL_STARTED = "subscription.trial_started"
EVENT_SUBSCRIPTION_ACTIVATED = "subscription.activated"
EVENT_SUBSCRIPTION_RENEWED = "subscription.renewed"
EVENT_SUBSCRIPTION_PAST_DUE = "subscription.past_due"
EVENT_SUBSCRIPTION_SUSPENDED = "subscription.suspended"
EVENT_SUBSCRIPTION_CANCELLED = "subscription.cancelled"
EVENT_SUBSCRIPTION_EXPIRED = "subscription.expired"
EVENT_SUBSCRIPTION_UPGRADED = "subscription.upgraded"
EVENT_SUBSCRIPTION_DOWNGRADED = "subscription.downgraded"

SUBSCRIPTION_EVENTS = (
    EVENT_SUBSCRIPTION_CREATED,
    EVENT_SUBSCRIPTION_STARTED,
    EVENT_SUBSCRIPTION_TRIAL_STARTED,
    EVENT_SUBSCRIPTION_ACTIVATED,
    EVENT_SUBSCRIPTION_RENEWED,
    EVENT_SUBSCRIPTION_PAST_DUE,
    EVENT_SUBSCRIPTION_SUSPENDED,
    EVENT_SUBSCRIPTION_CANCELLED,
    EVENT_SUBSCRIPTION_EXPIRED,
    EVENT_SUBSCRIPTION_UPGRADED,
    EVENT_SUBSCRIPTION_DOWNGRADED,
)


# ============================================================================
# Invoice Events
# ============================================================================

EVENT_INVOICE_CREATED = "invoice.created"
EVENT_INVOICE_ISSUED = "invoice.issued"
EVENT_INVOICE_SENT = "invoice.sent"
EVENT_INVOICE_OVERDUE = "invoice.overdue"
EVENT_INVOICE_PARTIALLY_PAID = "invoice.partially_paid"
EVENT_INVOICE_PAID = "invoice.paid"
EVENT_INVOICE_CANCELLED = "invoice.cancelled"
EVENT_INVOICE_REFUNDED = "invoice.refunded"

INVOICE_EVENTS = (
    EVENT_INVOICE_CREATED,
    EVENT_INVOICE_ISSUED,
    EVENT_INVOICE_SENT,
    EVENT_INVOICE_OVERDUE,
    EVENT_INVOICE_PARTIALLY_PAID,
    EVENT_INVOICE_PAID,
    EVENT_INVOICE_CANCELLED,
    EVENT_INVOICE_REFUNDED,
)


# ============================================================================
# Payment Events
# ============================================================================

EVENT_PAYMENT_CREATED = "payment.created"
EVENT_PAYMENT_PENDING = "payment.pending"
EVENT_PAYMENT_PROCESSING = "payment.processing"
EVENT_PAYMENT_SUCCESS = "payment.success"
EVENT_PAYMENT_FAILED = "payment.failed"
EVENT_PAYMENT_CANCELLED = "payment.cancelled"
EVENT_PAYMENT_REFUND_REQUESTED = "payment.refund_requested"
EVENT_PAYMENT_REFUNDED = "payment.refunded"
EVENT_PAYMENT_PARTIALLY_REFUNDED = "payment.partially_refunded"

PAYMENT_EVENTS = (
    EVENT_PAYMENT_CREATED,
    EVENT_PAYMENT_PENDING,
    EVENT_PAYMENT_PROCESSING,
    EVENT_PAYMENT_SUCCESS,
    EVENT_PAYMENT_FAILED,
    EVENT_PAYMENT_CANCELLED,
    EVENT_PAYMENT_REFUND_REQUESTED,
    EVENT_PAYMENT_REFUNDED,
    EVENT_PAYMENT_PARTIALLY_REFUNDED,
)


# ============================================================================
# Usage / Metering Events
# ============================================================================

EVENT_USAGE_RECORDED = "usage.recorded"
EVENT_USAGE_AGGREGATED = "usage.aggregated"
EVENT_USAGE_LIMIT_REACHED = "usage.limit_reached"
EVENT_USAGE_LIMIT_EXCEEDED = "usage.limit_exceeded"
EVENT_USAGE_CHARGE_CREATED = "usage.charge_created"

USAGE_EVENTS = (
    EVENT_USAGE_RECORDED,
    EVENT_USAGE_AGGREGATED,
    EVENT_USAGE_LIMIT_REACHED,
    EVENT_USAGE_LIMIT_EXCEEDED,
    EVENT_USAGE_CHARGE_CREATED,
)


# ============================================================================
# Public API
# ============================================================================

__all__ = [
    "BILLING_CYCLE_MONTHLY",
    "BILLING_CYCLE_YEARLY",
    "BILLING_CYCLES",
    "SUBSCRIPTION_TRIAL",
    "SUBSCRIPTION_ACTIVE",
    "SUBSCRIPTION_PAST_DUE",
    "SUBSCRIPTION_SUSPENDED",
    "SUBSCRIPTION_CANCELLED",
    "SUBSCRIPTION_EXPIRED",
    "SUBSCRIPTION_STATUSES",
    "INVOICE_DRAFT",
    "INVOICE_ISSUED",
    "INVOICE_SENT",
    "INVOICE_PARTIALLY_PAID",
    "INVOICE_PAID",
    "INVOICE_OVERDUE",
    "INVOICE_FAILED",
    "INVOICE_CANCELLED",
    "INVOICE_REFUNDED",
    "INVOICE_STATUSES",
    "PAYMENT_PENDING",
    "PAYMENT_PROCESSING",
    "PAYMENT_SUCCESS",
    "PAYMENT_FAILED",
    "PAYMENT_CANCELLED",
    "PAYMENT_REFUNDED",
    "PAYMENT_PARTIALLY_REFUNDED",
    "PAYMENT_STATUSES",
    "PROVIDER_STRIPE",
    "PROVIDER_RAZORPAY",
    "PROVIDER_PAYPAL",
    "PROVIDER_BANK",
    "PROVIDER_MANUAL",
    "PAYMENT_PROVIDERS",
    "USAGE_USERS",
    "USAGE_ACTIVE_USERS",
    "USAGE_BRANCHES",
    "USAGE_DOCTORS",
    "USAGE_STAFF",
    "USAGE_STORAGE",
    "USAGE_PATIENTS",
    "USAGE_ACTIVE_PATIENTS",
    "USAGE_APPOINTMENTS",
    "USAGE_ENCOUNTERS",
    "USAGE_PRESCRIPTIONS",
    "USAGE_LAB_ORDERS",
    "USAGE_IMAGING",
    "USAGE_TELEMEDICINE",
    "USAGE_PHARMACY_ORDERS",
    "USAGE_INVENTORY",
    "USAGE_AI_REQUESTS",
    "USAGE_AI_TOKENS",
    "USAGE_AI_DOCUMENTS",
    "USAGE_API_CALLS",
    "USAGE_METRICS",
    "EVENT_SUBSCRIPTION_CREATED",
    "EVENT_SUBSCRIPTION_STARTED",
    "EVENT_SUBSCRIPTION_TRIAL_STARTED",
    "EVENT_SUBSCRIPTION_ACTIVATED",
    "EVENT_SUBSCRIPTION_RENEWED",
    "EVENT_SUBSCRIPTION_PAST_DUE",
    "EVENT_SUBSCRIPTION_SUSPENDED",
    "EVENT_SUBSCRIPTION_CANCELLED",
    "EVENT_SUBSCRIPTION_EXPIRED",
    "EVENT_SUBSCRIPTION_UPGRADED",
    "EVENT_SUBSCRIPTION_DOWNGRADED",
    "SUBSCRIPTION_EVENTS",
    "EVENT_INVOICE_CREATED",
    "EVENT_INVOICE_ISSUED",
    "EVENT_INVOICE_SENT",
    "EVENT_INVOICE_OVERDUE",
    "EVENT_INVOICE_PARTIALLY_PAID",
    "EVENT_INVOICE_PAID",
    "EVENT_INVOICE_CANCELLED",
    "EVENT_INVOICE_REFUNDED",
    "INVOICE_EVENTS",
    "EVENT_PAYMENT_CREATED",
    "EVENT_PAYMENT_PENDING",
    "EVENT_PAYMENT_PROCESSING",
    "EVENT_PAYMENT_SUCCESS",
    "EVENT_PAYMENT_FAILED",
    "EVENT_PAYMENT_CANCELLED",
    "EVENT_PAYMENT_REFUND_REQUESTED",
    "EVENT_PAYMENT_REFUNDED",
    "EVENT_PAYMENT_PARTIALLY_REFUNDED",
    "PAYMENT_EVENTS",
    "EVENT_USAGE_RECORDED",
    "EVENT_USAGE_AGGREGATED",
    "EVENT_USAGE_LIMIT_REACHED",
    "EVENT_USAGE_LIMIT_EXCEEDED",
    "EVENT_USAGE_CHARGE_CREATED",
    "USAGE_EVENTS",
]
