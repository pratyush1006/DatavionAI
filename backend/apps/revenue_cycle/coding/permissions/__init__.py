from __future__ import annotations

"""Canonical RBAC permission codes for Revenue Cycle Coding."""


class CodingPermissions:
    """Permission constants consumed by Coding policies."""

    LIST = "revenue_cycle.coding.list"
    VIEW = "revenue_cycle.coding.view"
    CREATE = "revenue_cycle.coding.create"
    UPDATE = "revenue_cycle.coding.update"
    DELETE = "revenue_cycle.coding.delete"
    RESTORE = "revenue_cycle.coding.restore"
    ASSIGN = "revenue_cycle.coding.assign"
    REVIEW = "revenue_cycle.coding.review"
    CODE = "revenue_cycle.coding.code"
    VALIDATE = "revenue_cycle.coding.validate"
    RELEASE = "revenue_cycle.coding.release"
    VOID = "revenue_cycle.coding.void"


__all__ = ("CodingPermissions",)
