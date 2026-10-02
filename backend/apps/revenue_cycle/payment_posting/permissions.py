"""Canonical platform RBAC permission codes for payment posting."""

from __future__ import annotations

PAYMENT_POSTING_READ = "revenue_cycle.payment_posting.read"
PAYMENT_POSTING_WRITE = "revenue_cycle.payment_posting.write"
PAYMENT_POSTING_REVERSE = "revenue_cycle.payment_posting.reverse"
PAYMENT_POSTING_DELETE = "revenue_cycle.payment_posting.delete"
PAYMENT_POSTING_RESTORE = "revenue_cycle.payment_posting.restore"

__all__ = (
    "PAYMENT_POSTING_DELETE",
    "PAYMENT_POSTING_READ",
    "PAYMENT_POSTING_RESTORE",
    "PAYMENT_POSTING_REVERSE",
    "PAYMENT_POSTING_WRITE",
)
