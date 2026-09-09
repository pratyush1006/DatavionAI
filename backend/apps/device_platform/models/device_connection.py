import uuid

from django.db import models

from apps.device_platform.constants import ConnectionState, TelemetrySource


class DeviceConnection(models.Model):
    connection_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="device_connections",
    )
    device = models.ForeignKey(
        "device_platform.Device", on_delete=models.CASCADE, related_name="connections"
    )
    source = models.CharField(max_length=30, choices=TelemetrySource.choices)
    state = models.CharField(
        max_length=24,
        choices=ConnectionState.choices,
        default=ConnectionState.DISCONNECTED,
    )
    external_connection_id = models.CharField(max_length=255, blank=True)
    connected_at = models.DateTimeField(null=True, blank=True)
    disconnected_at = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "device_platform_connections"
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "device", "source"],
                name="dp_conn_org_dev_source_uniq",
            ),
        ]
        indexes = [
            models.Index(
                fields=["organization", "device", "state"],
                name="dp_conn_org_dev_state_idx",
            ),
        ]
