from django.db import models

from apps.core.models import BaseManager, BaseModel

from .test import LaboratoryTest


class LaboratoryPanelItem(BaseModel):
    objects = BaseManager()
    panel = models.ForeignKey(
        LaboratoryTest, on_delete=models.CASCADE, related_name="panel_items"
    )
    test = models.ForeignKey(
        LaboratoryTest, on_delete=models.PROTECT, related_name="panel_memberships"
    )
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("panel", "test"), name="uq_lab_panel_test")
        ]
