from .ble import BLEAdapter, BLEDeviceAdvertisement


async def discover_devices(
    adapter: BLEAdapter, *, timeout_seconds=10
) -> list[BLEDeviceAdvertisement]:
    return await adapter.scan(timeout_seconds=timeout_seconds)
