from django.db import models


class Priority(models.TextChoices):
    ROUTINE = "routine", "Routine"
    URGENT = "urgent", "Urgent"
    STAT = "stat", "STAT"


class ImagingOrderStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    ORDERED = "ordered", "Ordered"
    READY = "ready", "Ready"
    SCHEDULED = "scheduled", "Scheduled"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class ImagingStudyStatus(models.TextChoices):
    SCHEDULED = "scheduled", "Scheduled"
    ARRIVED = "arrived", "Arrived"
    READY = "ready", "Ready"
    ACQUIRING = "acquiring", "Acquiring"
    ACQUIRED = "acquired", "Acquired"
    PRELIMINARY = "preliminary", "Preliminary"
    FINAL = "final", "Final"
    AMENDED = "amended", "Amended"
    CANCELLED = "cancelled", "Cancelled"


class ImagingReportStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PRELIMINARY = "preliminary", "Preliminary"
    FINAL = "final", "Final"
    AMENDED = "amended", "Amended"


class ModalityType(models.TextChoices):
    CT = "ct", "CT"
    MRI = "mri", "MRI"
    XRAY = "xray", "X-Ray"
    ULTRASOUND = "ultrasound", "Ultrasound"
    MAMMOGRAPHY = "mammography", "Mammography"
    PET = "pet", "PET"
    SPECT = "spect", "SPECT"
    OTHER = "other", "Other"


class ProcedureType(models.TextChoices):
    DIAGNOSTIC = "diagnostic", "Diagnostic"
    SCREENING = "screening", "Screening"
    INTERVENTIONAL = "interventional", "Interventional"


class ContrastStatus(models.TextChoices):
    NOT_REQUIRED = "not_required", "Not Required"
    SCREENING = "screening", "Screening"
    CLEARED = "cleared", "Cleared"
    ADMINISTERED = "administered", "Administered"
    DECLINED = "declined", "Declined"
    CONTRAINDICATED = "contraindicated", "Contraindicated"


class AppointmentLinkStatus(models.TextChoices):
    RESERVED = "reserved", "Reserved"
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"
    COMPLETED = "completed", "Completed"


class ChargeStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUBMITTED = "submitted", "Submitted"
    FAILED = "failed", "Failed"


class DocumentLinkStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    LINKED = "linked", "Linked"
    SUPERSEDED = "superseded", "Superseded"


class IntegrationStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SENT = "sent", "Sent"
    ACKNOWLEDGED = "acknowledged", "Acknowledged"
    FAILED = "failed", "Failed"
