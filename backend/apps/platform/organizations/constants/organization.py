"""
Organization-specific constants.
"""

from __future__ import annotations

from typing import Final

from django.db import models


class OrganizationCategory(
    models.TextChoices,
):
    """
    High-level organization categories.
    """

    HEALTHCARE_PROVIDER = (
        "healthcare_provider",
        "Healthcare Provider",
    )

    DIAGNOSTICS = (
        "diagnostics",
        "Diagnostics",
    )

    PHARMACY = (
        "pharmacy",
        "Pharmacy",
    )

    EMERGENCY = (
        "emergency",
        "Emergency Services",
    )

    INSURANCE = (
        "insurance",
        "Insurance",
    )

    RESEARCH = (
        "research",
        "Research & Education",
    )

    PUBLIC_HEALTH = (
        "public_health",
        "Public Health",
    )

    ENTERPRISE = (
        "enterprise",
        "Enterprise",
    )


class OrganizationType(
    models.TextChoices,
):
    """
    Supported organization types.
    """

    # ======================================================================
    # Healthcare Providers
    # ======================================================================

    HOSPITAL = (
        "hospital",
        "Hospital",
    )

    CLINIC = (
        "clinic",
        "Clinic",
    )

    DENTAL_CLINIC = (
        "dental_clinic",
        "Dental Clinic",
    )

    EYE_CLINIC = (
        "eye_clinic",
        "Eye Clinic",
    )

    ENT_CLINIC = (
        "ent_clinic",
        "ENT Clinic",
    )

    CARDIOLOGY_CLINIC = (
        "cardiology_clinic",
        "Cardiology Clinic",
    )

    NEUROLOGY_CLINIC = (
        "neurology_clinic",
        "Neurology Clinic",
    )

    ORTHOPEDIC_CLINIC = (
        "orthopedic_clinic",
        "Orthopedic Clinic",
    )

    PEDIATRIC_CLINIC = (
        "pediatric_clinic",
        "Pediatric Clinic",
    )

    GYNECOLOGY_CLINIC = (
        "gynecology_clinic",
        "Gynecology Clinic",
    )

    DERMATOLOGY_CLINIC = (
        "dermatology_clinic",
        "Dermatology Clinic",
    )

    PSYCHIATRY_CLINIC = (
        "psychiatry_clinic",
        "Psychiatry Clinic",
    )

    ONCOLOGY_CENTER = (
        "oncology_center",
        "Oncology Center",
    )

    PHYSIOTHERAPY_CENTER = (
        "physiotherapy_center",
        "Physiotherapy Center",
    )

    REHABILITATION_CENTER = (
        "rehabilitation_center",
        "Rehabilitation Center",
    )

    DIALYSIS_CENTER = (
        "dialysis_center",
        "Dialysis Center",
    )

    FERTILITY_CENTER = (
        "fertility_center",
        "Fertility Center",
    )

    HOME_HEALTHCARE = (
        "home_healthcare",
        "Home Healthcare",
    )

    TELEMEDICINE = (
        "telemedicine",
        "Telemedicine Provider",
    )

    NURSING_HOME = (
        "nursing_home",
        "Nursing Home",
    )

    HOSPICE = (
        "hospice",
        "Hospice",
    )

    ASSISTED_LIVING = (
        "assisted_living",
        "Assisted Living Facility",
    )

    WELLNESS_CENTER = (
        "wellness_center",
        "Wellness Center",
    )

    # ======================================================================
    # Diagnostics
    # ======================================================================

    LABORATORY = (
        "laboratory",
        "Laboratory",
    )

    DIAGNOSTIC_CENTER = (
        "diagnostic_center",
        "Diagnostic Center",
    )

    RADIOLOGY_CENTER = (
        "radiology_center",
        "Radiology Center",
    )

    IMAGING_CENTER = (
        "imaging_center",
        "Imaging Center",
    )

    PATHOLOGY_LAB = (
        "pathology_lab",
        "Pathology Laboratory",
    )

    BLOOD_BANK = (
        "blood_bank",
        "Blood Bank",
    )

    # ======================================================================
    # Pharmacy
    # ======================================================================

    RETAIL_PHARMACY = (
        "retail_pharmacy",
        "Retail Pharmacy",
    )

    HOSPITAL_PHARMACY = (
        "hospital_pharmacy",
        "Hospital Pharmacy",
    )

    ONLINE_PHARMACY = (
        "online_pharmacy",
        "Online Pharmacy",
    )

    WHOLESALE_PHARMACY = (
        "wholesale_pharmacy",
        "Wholesale Pharmacy",
    )

    # ======================================================================
    # Emergency
    # ======================================================================

    AMBULANCE_SERVICE = (
        "ambulance_service",
        "Ambulance Service",
    )

    TRAUMA_CENTER = (
        "trauma_center",
        "Trauma Center",
    )

    EMERGENCY_CENTER = (
        "emergency_center",
        "Emergency Center",
    )

    # ======================================================================
    # Insurance
    # ======================================================================

    INSURANCE_COMPANY = (
        "insurance_company",
        "Insurance Company",
    )

    TPA = (
        "tpa",
        "Third Party Administrator",
    )

    # ======================================================================
    # Research & Education
    # ======================================================================

    MEDICAL_COLLEGE = (
        "medical_college",
        "Medical College",
    )

    MEDICAL_UNIVERSITY = (
        "medical_university",
        "Medical University",
    )

    RESEARCH_INSTITUTE = (
        "research_institute",
        "Research Institute",
    )

    CLINICAL_TRIAL_CENTER = (
        "clinical_trial_center",
        "Clinical Trial Center",
    )

    # ======================================================================
    # Public Health
    # ======================================================================

    GOVERNMENT_HOSPITAL = (
        "government_hospital",
        "Government Hospital",
    )

    PUBLIC_HEALTH_CENTER = (
        "public_health_center",
        "Public Health Center",
    )

    NGO = (
        "ngo",
        "NGO",
    )

    # ======================================================================
    # Enterprise
    # ======================================================================

    CORPORATE = (
        "corporate",
        "Corporate",
    )

    OCCUPATIONAL_HEALTH = (
        "occupational_health",
        "Occupational Health",
    )

    HEALTHCARE_NETWORK = (
        "healthcare_network",
        "Healthcare Network",
    )


class OrganizationStatus(
    models.TextChoices,
):
    """
    Organization lifecycle status.
    """

    DRAFT = (
        "draft",
        "Draft",
    )

    PENDING_VERIFICATION = (
        "pending_verification",
        "Pending Verification",
    )

    ACTIVE = (
        "active",
        "Active",
    )

    INACTIVE = (
        "inactive",
        "Inactive",
    )

    SUSPENDED = (
        "suspended",
        "Suspended",
    )

    ARCHIVED = (
        "archived",
        "Archived",
    )


class OrganizationSize(
    models.TextChoices,
):
    """
    Organization size.
    """

    SOLO = (
        "solo",
        "Solo Practice",
    )

    SMALL = (
        "small",
        "Small",
    )

    MEDIUM = (
        "medium",
        "Medium",
    )

    LARGE = (
        "large",
        "Large",
    )

    ENTERPRISE = (
        "enterprise",
        "Enterprise",
    )


class VerificationStatus(
    models.TextChoices,
):
    """
    Organization verification status.
    """

    PENDING = (
        "pending",
        "Pending",
    )

    VERIFIED = (
        "verified",
        "Verified",
    )

    REJECTED = (
        "rejected",
        "Rejected",
    )


class SubscriptionStatus(
    models.TextChoices,
):
    """
    Organization subscription status.
    """

    TRIAL = (
        "trial",
        "Trial",
    )

    ACTIVE = (
        "active",
        "Active",
    )

    GRACE_PERIOD = (
        "grace_period",
        "Grace Period",
    )

    EXPIRED = (
        "expired",
        "Expired",
    )

    CANCELLED = (
        "cancelled",
        "Cancelled",
    )


# ============================================================================
# Default Values
# ============================================================================

DEFAULT_ORGANIZATION_CATEGORY: Final[str] = OrganizationCategory.HEALTHCARE_PROVIDER

DEFAULT_ORGANIZATION_TYPE: Final[str] = OrganizationType.HOSPITAL

DEFAULT_ORGANIZATION_STATUS: Final[str] = OrganizationStatus.ACTIVE

DEFAULT_ORGANIZATION_SIZE: Final[str] = OrganizationSize.SMALL

DEFAULT_VERIFICATION_STATUS: Final[str] = VerificationStatus.PENDING

DEFAULT_SUBSCRIPTION_STATUS: Final[str] = SubscriptionStatus.TRIAL


# ============================================================================
# Category → Supported Organization Types
# ============================================================================

ORGANIZATION_CATEGORY_TYPES: Final[
    dict[
        OrganizationCategory,
        set[OrganizationType],
    ]
] = {
    OrganizationCategory.HEALTHCARE_PROVIDER: {
        OrganizationType.HOSPITAL,
        OrganizationType.CLINIC,
        OrganizationType.DENTAL_CLINIC,
        OrganizationType.EYE_CLINIC,
        OrganizationType.ENT_CLINIC,
        OrganizationType.CARDIOLOGY_CLINIC,
        OrganizationType.NEUROLOGY_CLINIC,
        OrganizationType.ORTHOPEDIC_CLINIC,
        OrganizationType.PEDIATRIC_CLINIC,
        OrganizationType.GYNECOLOGY_CLINIC,
        OrganizationType.DERMATOLOGY_CLINIC,
        OrganizationType.PSYCHIATRY_CLINIC,
        OrganizationType.ONCOLOGY_CENTER,
        OrganizationType.PHYSIOTHERAPY_CENTER,
        OrganizationType.REHABILITATION_CENTER,
        OrganizationType.DIALYSIS_CENTER,
        OrganizationType.FERTILITY_CENTER,
        OrganizationType.HOME_HEALTHCARE,
        OrganizationType.TELEMEDICINE,
        OrganizationType.NURSING_HOME,
        OrganizationType.HOSPICE,
        OrganizationType.ASSISTED_LIVING,
        OrganizationType.WELLNESS_CENTER,
    },
    OrganizationCategory.DIAGNOSTICS: {
        OrganizationType.LABORATORY,
        OrganizationType.DIAGNOSTIC_CENTER,
        OrganizationType.RADIOLOGY_CENTER,
        OrganizationType.IMAGING_CENTER,
        OrganizationType.PATHOLOGY_LAB,
        OrganizationType.BLOOD_BANK,
    },
    OrganizationCategory.PHARMACY: {
        OrganizationType.RETAIL_PHARMACY,
        OrganizationType.HOSPITAL_PHARMACY,
        OrganizationType.ONLINE_PHARMACY,
        OrganizationType.WHOLESALE_PHARMACY,
    },
    OrganizationCategory.EMERGENCY: {
        OrganizationType.AMBULANCE_SERVICE,
        OrganizationType.TRAUMA_CENTER,
        OrganizationType.EMERGENCY_CENTER,
    },
    OrganizationCategory.INSURANCE: {
        OrganizationType.INSURANCE_COMPANY,
        OrganizationType.TPA,
    },
    OrganizationCategory.RESEARCH: {
        OrganizationType.MEDICAL_COLLEGE,
        OrganizationType.MEDICAL_UNIVERSITY,
        OrganizationType.RESEARCH_INSTITUTE,
        OrganizationType.CLINICAL_TRIAL_CENTER,
    },
    OrganizationCategory.PUBLIC_HEALTH: {
        OrganizationType.GOVERNMENT_HOSPITAL,
        OrganizationType.PUBLIC_HEALTH_CENTER,
        OrganizationType.NGO,
    },
    OrganizationCategory.ENTERPRISE: {
        OrganizationType.CORPORATE,
        OrganizationType.OCCUPATIONAL_HEALTH,
        OrganizationType.HEALTHCARE_NETWORK,
    },
}


# ============================================================================
# Public Exports
# ============================================================================

__all__ = [
    "OrganizationCategory",
    "OrganizationType",
    "OrganizationStatus",
    "OrganizationSize",
    "VerificationStatus",
    "SubscriptionStatus",
    "ORGANIZATION_CATEGORY_TYPES",
    "DEFAULT_ORGANIZATION_CATEGORY",
    "DEFAULT_ORGANIZATION_TYPE",
    "DEFAULT_ORGANIZATION_STATUS",
    "DEFAULT_ORGANIZATION_SIZE",
    "DEFAULT_VERIFICATION_STATUS",
    "DEFAULT_SUBSCRIPTION_STATUS",
]
