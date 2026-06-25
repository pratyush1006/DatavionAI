from django.db import models
from apps.core.models import TimeStampedModel

class Organization(TimeStampedModel):
    name = models.CharField(
        max_length=255,
        unique=True
    )

    code = models.CharField(
        max_length=20,
        unique=True
    )

    organization_type = models.CharField(
        max_length=100,
        default="Hospital"
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    country = models.CharField(
        max_length=100,
        default="USA"
    )

    is_active = models.BooleanField(
        default=True
    
    )

    def __str__(self):
        return self.name