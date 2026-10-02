from django.db import models


class DiagnosisType(models.TextChoices):
    PRIMARY = "primary", "Primary"
    SECONDARY = "secondary", "Secondary"
    DIFFERENTIAL = "differential", "Differential"
    HISTORICAL = "historical", "Historical"


class DiagnosisStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    RESOLVED = "resolved", "Resolved"
    INACTIVE = "inactive", "Inactive"
    RULED_OUT = "ruled_out", "Ruled Out"
