from __future__ import annotations

import uuid

from django.db import models
from django.utils import timezone

from apps.device_platform.constants import PairingState


class DevicePairing(models.Model):
    pairing_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="device_pairings",
    )
    device = models.ForeignKey(
        "device_platform.Device", on_delete=models.CASCADE, related_name="pairings"
    )
    initiated_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="device_pairings_initiated",
    )
    state = models.CharField(
        max_length=24, choices=PairingState.choices, default=PairingState.PENDING
    )
    pairing_method = models.CharField(max_length=40, default="BLE")
    external_pairing_id = models.CharField(max_length=255, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "device_platform_pairings"
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "device"],
                condition=models.Q(state=PairingState.PAIRED),
                name="dp_pair_active_uniq",
            ),
        ]
        indexes = [
            models.Index(
                fields=["organization", "device", "state"],
                name="dp_pair_org_dev_state_idx",
            ),
        ]

    def revoke(self) -> None:
        self.state = PairingState.REVOKED
        self.revoked_at = timezone.now()
        self.save(update_fields=["state", "revoked_at"])
