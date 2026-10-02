from django.db import models


class InsuranceType(models.TextChoices):
    GOVERNMENT = "government", "Government"
    PRIVATE = "private", "Private"
    EMPLOYER = "employer", "Employer"
    SELF_FUNDED = "self_funded", "Self Funded"
    SELF_PAY = "self_pay", "Self Pay"
    CHARITY = "charity", "Charity"


class TPAType(models.TextChoices):
    THIRD_PARTY_ADMINISTRATOR = "tpa", "Third-Party Administrator"
    BENEFITS_ADMINISTRATOR = "benefits_administrator", "Benefits Administrator"
    CLAIMS_ADMINISTRATOR = "claims_administrator", "Claims Administrator"


class RelationshipStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACTIVE = "active", "Active"
    SUSPENDED = "suspended", "Suspended"
    EXPIRED = "expired", "Expired"
    TERMINATED = "terminated", "Terminated"


class CoverageStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    EXPIRED = "expired", "Expired"
    TERMINATED = "terminated", "Terminated"


class BenefitCategory(models.TextChoices):
    MEDICAL = "medical", "Medical"
    PHARMACY = "pharmacy", "Pharmacy"
    DENTAL = "dental", "Dental"
    VISION = "vision", "Vision"
    MENTAL_HEALTH = "mental_health", "Mental Health"
    LABORATORY = "laboratory", "Laboratory"
    IMAGING = "imaging", "Imaging"
    HOSPITAL = "hospital", "Hospital"
    EMERGENCY = "emergency", "Emergency"
    OTHER = "other", "Other"


class CoordinationOrder(models.IntegerChoices):
    PRIMARY = 1, "Primary"
    SECONDARY = 2, "Secondary"
    TERTIARY = 3, "Tertiary"
