"""
Selectors for the Patient Registration module.
"""

from apps.patient_management.registration.selectors.registration import (
    get_completed_registrations,
    get_pending_verification_registrations,
    get_ready_for_checkin_registrations,
    get_ready_for_completion_registrations,
    get_registration_by_number,
    get_registration_by_uuid,
    get_today_registrations,
    list_organization_registrations,
    list_patient_registrations,
    list_registrations,
    search_registrations,
)

__all__ = [
    "get_completed_registrations",
    "get_pending_verification_registrations",
    "get_ready_for_checkin_registrations",
    "get_ready_for_completion_registrations",
    "get_registration_by_number",
    "get_registration_by_uuid",
    "get_today_registrations",
    "list_organization_registrations",
    "list_patient_registrations",
    "list_registrations",
    "search_registrations",
]
