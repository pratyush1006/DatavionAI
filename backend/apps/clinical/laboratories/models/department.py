from django.db import models

from apps.core.models import BaseManager, BaseModel

from .laboratory import Laboratory


class LaboratoryDepartment(BaseModel):
    objects = BaseManager()
    laboratory = models.ForeignKey(
        Laboratory, on_delete=models.CASCADE, related_name="departments"
    )
    code = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default="active")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("laboratory", "code"), name="uq_lab_department_code"
            )
        ]
