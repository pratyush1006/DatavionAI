from .base import DeviceIntegration


class GenericBLEIntegration(DeviceIntegration):
    name = "generic_ble"

    async def discover(self, **kwargs):
        return []

    async def sync(self, **kwargs):
        return {"status": "accepted", "mode": "gateway_managed"}
