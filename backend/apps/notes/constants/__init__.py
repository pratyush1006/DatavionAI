from django.db import models


class NoteStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    IN_REVIEW = "in_review", "In Review"
    SIGNED = "signed", "Signed"
    AMENDED = "amended", "Amended"
    CANCELLED = "cancelled", "Cancelled"


class NoteType(models.TextChoices):
    SOAP = "soap", "SOAP"
    PROGRESS = "progress", "Progress"
    CONSULTATION = "consultation", "Consultation"
    DISCHARGE = "discharge", "Discharge"
    PROCEDURE = "procedure", "Procedure"
    TELEMEDICINE = "telemedicine", "Telemedicine"
    NURSING = "nursing", "Nursing"
    OTHER = "other", "Other"


class NoteSource(models.TextChoices):
    MANUAL = "manual", "Manual"
    TRANSCRIPTION = "transcription", "Transcription"
    TELEMEDICINE = "telemedicine", "Telemedicine"
    IMPORTED = "imported", "Imported"


class AmendmentStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SUBMITTED = "submitted", "Submitted"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"
