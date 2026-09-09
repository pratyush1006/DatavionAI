from datetime import datetime


def build_provenance(
    *, source: str, source_device_id: str, source_timestamp: datetime | None = None
) -> dict:
    return {
        "source": source,
        "source_device_id": source_device_id,
        "source_timestamp": source_timestamp.isoformat() if source_timestamp else None,
        "received_by": "datavion-device-platform",
        "schema_version": 1,
    }
