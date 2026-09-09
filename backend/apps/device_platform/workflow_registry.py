"""Device Platform workflow registration against the canonical workflow kernel."""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.device_platform.workflows import (
    DeviceAssociateWorkflow,
    DeviceConnectWorkflow,
    DeviceDisconnectWorkflow,
    DeviceDissociateWorkflow,
    DevicePairWorkflow,
    DeviceRegisterWorkflow,
    DeviceRetireWorkflow,
    DeviceSyncWorkflow,
    DeviceTelemetryIngestWorkflow,
    DeviceUnpairWorkflow,
    DeviceUpdateWorkflow,
)


def register_device_workflows() -> None:
    workflows = {
        cls.workflow_name: cls
        for cls in (
            DeviceRegisterWorkflow,
            DeviceUpdateWorkflow,
            DevicePairWorkflow,
            DeviceUnpairWorkflow,
            DeviceConnectWorkflow,
            DeviceDisconnectWorkflow,
            DeviceAssociateWorkflow,
            DeviceDissociateWorkflow,
            DeviceTelemetryIngestWorkflow,
            DeviceSyncWorkflow,
            DeviceRetireWorkflow,
        )
    }
    for name, workflow in workflows.items():
        if not workflow_registry.is_registered(name):
            workflow_registry.register(name=name, workflow=workflow)


__all__ = ["register_device_workflows"]
