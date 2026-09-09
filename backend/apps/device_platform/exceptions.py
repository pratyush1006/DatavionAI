class DevicePlatformError(Exception):
    """Base Device Platform exception."""


class DeviceAuthorizationError(DevicePlatformError):
    pass


class DeviceStateError(DevicePlatformError):
    pass


class TelemetryValidationError(DevicePlatformError):
    pass
