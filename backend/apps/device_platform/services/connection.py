from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from apps.device_platform.constants import ConnectionState, DeviceLifecycle
from apps.device_platform.models import Device, DeviceConnection


class ConnectionService:
    @staticmethod
    @transaction.atomic
    def set_state(
        *,
        device_id,
        organization_id,
        source,
        state,
        external_connection_id="",
        last_error="",
        metadata=None,
    ):
        device = Device.objects.select_for_update().get(
            device_id=device_id, organization_id=organization_id
        )
        if device.lifecycle == DeviceLifecycle.RETIRED:
            raise ValueError("Retired devices cannot connect.")
        connection, _ = DeviceConnection.objects.select_for_update().get_or_create(
            organization_id=organization_id,
            device=device,
            source=source,
            defaults={"state": ConnectionState.DISCONNECTED},
        )
        connection.state = state
        connection.external_connection_id = external_connection_id or ""
        connection.last_error = last_error or ""
        if metadata is not None:
            connection.metadata = metadata
        now = timezone.now()
        if state == ConnectionState.CONNECTED:
            connection.connected_at = now
            connection.disconnected_at = None
            device.last_seen_at = now
            if device.lifecycle in {DeviceLifecycle.PAIRED, DeviceLifecycle.ASSOCIATED}:
                device.lifecycle = DeviceLifecycle.ACTIVE
            device.save(update_fields=["last_seen_at", "lifecycle", "updated_at"])
        elif state in {ConnectionState.DISCONNECTED, ConnectionState.FAILED}:
            connection.disconnected_at = now
        connection.full_clean()
        connection.save()
        return connection
