"""
Permission group constants.
"""

from __future__ import annotations

from django.db import models


class PermissionGroupCode(
    models.TextChoices,
):
    """
    Built-in permission group codes.
    """

    PLATFORM = "platform", "Platform"

    ACCOUNTS = "accounts", "Accounts"

    ORGANIZATIONS = "organizations", "Organizations"

    RBAC = "rbac", "Role Based Access Control"

    PATIENTS = "patients", "Patients"

    PROVIDERS = "providers", "Providers"

    EMPLOYEES = "employees", "Employees"

    DEPARTMENTS = "departments", "Departments"

    TEAMS = "teams", "Teams"

    DOCUMENTS = "documents", "Documents"

    APPOINTMENTS = "appointments", "Appointments"

    ENCOUNTERS = "encounters", "Encounters"

    LABORATORIES = "laboratories", "Laboratories"

    MEDICATIONS = "medications", "Medications"

    PRESCRIPTIONS = "prescriptions", "Prescriptions"

    ALLERGIES = "allergies", "Allergies"

    DIAGNOSES = "diagnoses", "Diagnoses"

    VITALS = "vitals", "Vitals"

    PHARMACY = "pharmacy", "Pharmacy"

    BILLING = "billing", "Billing"

    INVENTORY = "inventory", "Inventory"

    NOTIFICATIONS = "notifications", "Notifications"

    AUDIT = "audit", "Audit"

    REPORTS = "reports", "Reports"

    DASHBOARD = "dashboard", "Dashboard"

    SETTINGS = "settings", "Settings"

    AI = "ai", "Artificial Intelligence"


__all__ = [
    "PermissionGroupCode",
]
