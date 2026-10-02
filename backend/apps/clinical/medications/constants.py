from django.db import models


class MedicationDosageForm(models.TextChoices):
    TABLET = "tablet", "Tablet"
    CAPSULE = "capsule", "Capsule"
    SYRUP = "syrup", "Syrup"
    SUSPENSION = "suspension", "Suspension"
    INJECTION = "injection", "Injection"
    CREAM = "cream", "Cream"
    OINTMENT = "ointment", "Ointment"
    DROPS = "drops", "Drops"
    INHALER = "inhaler", "Inhaler"
    PATCH = "patch", "Patch"
    POWDER = "powder", "Powder"
    SOLUTION = "solution", "Solution"
    OTHER = "other", "Other"


class MedicationRoute(models.TextChoices):
    ORAL = "oral", "Oral"
    IV = "iv", "Intravenous"
    IM = "im", "Intramuscular"
    SUBCUTANEOUS = "subcutaneous", "Subcutaneous"
    TOPICAL = "topical", "Topical"
    INHALATION = "inhalation", "Inhalation"
    NASAL = "nasal", "Nasal"
    OPHTHALMIC = "ophthalmic", "Ophthalmic"
    OTIC = "otic", "Otic"
    RECTAL = "rectal", "Rectal"
    VAGINAL = "vaginal", "Vaginal"
    OTHER = "other", "Other"
