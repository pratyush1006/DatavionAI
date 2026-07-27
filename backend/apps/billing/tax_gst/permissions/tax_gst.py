"""
Tax and GST permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class TaxGstPermission:
    """
    Tax and GST permission codes.
    """

    VIEW = "tax_gst.view"
    CREATE = "tax_gst.create"
    UPDATE = "tax_gst.update"
    DELETE = "tax_gst.delete"


class CanViewTaxGst(BasePermission):
    """
    Permission required to view tax gst.
    """

    permission_code = TaxGstPermission.VIEW


class CanCreateTaxGst(BasePermission):
    """
    Permission required to create tax gst.
    """

    permission_code = TaxGstPermission.CREATE


class CanUpdateTaxGst(BasePermission):
    """
    Permission required to update tax gst.
    """

    permission_code = TaxGstPermission.UPDATE


class CanDeleteTaxGst(BasePermission):
    """
    Permission required to delete tax gst.
    """

    permission_code = TaxGstPermission.DELETE


__all__ = [
    "TaxGstPermission",
    "CanViewTaxGst",
    "CanCreateTaxGst",
    "CanUpdateTaxGst",
    "CanDeleteTaxGst",
]
