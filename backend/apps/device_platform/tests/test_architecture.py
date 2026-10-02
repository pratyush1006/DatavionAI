from pathlib import Path


def test_device_platform_does_not_import_legacy_patient_domain():
    root = Path(__file__).resolve().parents[1]
    for path in root.rglob("*.py"):
        assert "apps.clinical.patients" not in path.read_text(encoding="utf-8")


def test_all_device_workflows_are_registered():
    from apps.core.workflows import workflow_registry

    expected = {
        "device.register",
        "device.update",
        "device.pair",
        "device.unpair",
        "device.connect",
        "device.disconnect",
        "device.associate_patient",
        "device.dissociate_patient",
        "device.ingest_telemetry",
        "device.sync",
        "device.retire",
    }
    assert all(workflow_registry.is_registered(name) for name in expected)
