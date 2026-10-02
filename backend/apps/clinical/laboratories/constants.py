from django.db import models


class CollectionType(models.TextChoices):
    LABORATORY = "laboratory", "Laboratory"
    HOME = "home", "Home Collection"


class OrderStatus(models.TextChoices):
    ORDERED = "ordered", "Ordered"
    SCHEDULED = "scheduled", "Scheduled"
    COLLECTED = "collected", "Collected"
    PROCESSING = "processing", "Processing"
    VERIFIED = "verified", "Verified"
    RELEASED = "released", "Released"
    CANCELLED = "cancelled", "Cancelled"


class SpecimenStatus(models.TextChoices):
    EXPECTED = "expected", "Expected"
    COLLECTED = "collected", "Collected"
    RECEIVED = "received", "Received"
    REJECTED = "rejected", "Rejected"
    PROCESSING = "processing", "Processing"
    COMPLETED = "completed", "Completed"


class ResultStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PRELIMINARY = "preliminary", "Preliminary"
    FINAL = "final", "Final"
    CORRECTED = "corrected", "Corrected"


class AbnormalFlag(models.TextChoices):
    NORMAL = "normal", "Normal"
    LOW = "low", "Low"
    HIGH = "high", "High"
    CRITICAL_LOW = "critical_low", "Critical Low"
    CRITICAL_HIGH = "critical_high", "Critical High"
    ABNORMAL = "abnormal", "Abnormal"
