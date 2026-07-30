"""
SaaS Billing RBAC permissions.

SaaS Billing bounded context permission adapters.

Uses the DatavionOS centralized RBAC engine.

Architecture:

User
 |
Organization
 |
RBAC Permission Engine
 |
SaaS Billing API
 |
Workflow
 |
Service
 |
Domain Event
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import (
    RBACPermissionBase,
)

# =============================================================================
# Billing Account Permissions
# =============================================================================


class CanViewBilling(
    RBACPermissionBase,
):
    """
    Allows viewing billing accounts.
    """

    message = "You do not have permission to view billing accounts."

    permission_code = "billing.view"


class CanManageBilling(
    RBACPermissionBase,
):
    """
    Allows managing billing accounts.

    Covers:

    - Billing profile updates
    - Payment provider configuration
    - Billing lifecycle operations
    """

    message = "You do not have permission to manage billing accounts."

    permission_code = "billing.manage"


# =============================================================================
# Subscription Permissions
# =============================================================================


class CanViewSubscription(
    RBACPermissionBase,
):
    """
    Allows viewing subscriptions.
    """

    message = "You do not have permission to view subscriptions."

    permission_code = "subscriptions.view"


class CanManageSubscription(
    RBACPermissionBase,
):
    """
    Allows managing subscriptions.

    Covers:

    - Create
    - Activate
    - Renew
    - Upgrade
    - Downgrade
    - Cancel
    """

    message = "You do not have permission to manage subscriptions."

    permission_code = "subscriptions.manage"


# =============================================================================
# Invoice Permissions
# =============================================================================


class CanViewInvoice(
    RBACPermissionBase,
):
    """
    Allows viewing invoices.
    """

    message = "You do not have permission to view invoices."

    permission_code = "invoices.view"


class CanManageInvoice(
    RBACPermissionBase,
):
    """
    Allows managing invoices.

    Covers:

    - Generate
    - Issue
    - Finalize
    - Cancel
    - Refund
    """

    message = "You do not have permission to manage invoices."

    permission_code = "invoices.manage"


# =============================================================================
# Payment Permissions
# =============================================================================


class CanViewPayment(
    RBACPermissionBase,
):
    """
    Allows viewing payments.
    """

    message = "You do not have permission to view payments."

    permission_code = "payments.view"


class CanManagePayment(
    RBACPermissionBase,
):
    """
    Allows managing payments.

    Covers:

    - Payment processing
    - Gateway reconciliation
    - Refunds
    """

    message = "You do not have permission to manage payments."

    permission_code = "payments.manage"


# =============================================================================
# Usage Permissions
# =============================================================================


class CanViewUsage(
    RBACPermissionBase,
):
    """
    Allows viewing usage metrics.
    """

    message = "You do not have permission to view usage metrics."

    permission_code = "usage.view"


class CanManageUsage(
    RBACPermissionBase,
):
    """
    Allows managing usage metering.

    Covers:

    - Usage collection
    - Usage evaluation
    - Usage charging
    """

    message = "You do not have permission to manage usage."

    permission_code = "usage.manage"


__all__ = (
    # Billing
    "CanViewBilling",
    "CanManageBilling",
    # Subscription
    "CanViewSubscription",
    "CanManageSubscription",
    # Invoice
    "CanViewInvoice",
    "CanManageInvoice",
    # Payment
    "CanViewPayment",
    "CanManagePayment",
    # Usage
    "CanViewUsage",
    "CanManageUsage",
)
