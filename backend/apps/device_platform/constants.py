from django.db import models


class DeviceLifecycle(models.TextChoices):
    DISCOVERED = "DISCOVERED", "Discovered"
    PAIRING = "PAIRING", "Pairing"
    PAIRED = "PAIRED", "Paired"
    ASSOCIATED = "ASSOCIATED", "Associated"
    ACTIVE = "ACTIVE", "Active"
    SUSPENDED = "SUSPENDED", "Suspended"
    RETIRED = "RETIRED", "Retired"


class ConnectionState(models.TextChoices):
    DISCONNECTED = "DISCONNECTED", "Disconnected"
    CONNECTING = "CONNECTING", "Connecting"
    CONNECTED = "CONNECTED", "Connected"
    RECONNECTING = "RECONNECTING", "Reconnecting"
    FAILED = "FAILED", "Failed"


class PairingState(models.TextChoices):
    NOT_PAIRED = "NOT_PAIRED", "Not paired"
    PENDING = "PENDING", "Pending"
    PAIRED = "PAIRED", "Paired"
    REVOKED = "REVOKED", "Revoked"


class TrustState(models.TextChoices):
    UNKNOWN = "UNKNOWN", "Unknown"
    TRUSTED = "TRUSTED", "Trusted"
    UNTRUSTED = "UNTRUSTED", "Untrusted"
    REVOKED = "REVOKED", "Revoked"


class DeviceCapabilityType(models.TextChoices):
    HEART_RATE = "HEART_RATE", "Heart rate"
    SPO2 = "SPO2", "SpO2"
    BLOOD_PRESSURE = "BLOOD_PRESSURE", "Blood pressure"
    GLUCOSE = "GLUCOSE", "Glucose"
    TEMPERATURE = "TEMPERATURE", "Temperature"
    ECG = "ECG", "ECG"
    RESPIRATORY_RATE = "RESPIRATORY_RATE", "Respiratory rate"
    WEIGHT = "WEIGHT", "Weight"
    STEPS = "STEPS", "Steps"
    DISTANCE = "DISTANCE", "Distance"
    CALORIES = "CALORIES", "Calories"
    SLEEP = "SLEEP", "Sleep"
    ACTIVITY = "ACTIVITY", "Activity"
    BATTERY = "BATTERY", "Battery"
    GENERIC = "GENERIC", "Generic"


class TelemetrySource(models.TextChoices):
    BLE = "BLE", "Bluetooth Low Energy"
    WIFI = "WIFI", "Wi-Fi"
    MOBILE = "MOBILE", "Mobile"
    HEALTH_PLATFORM = "HEALTH_PLATFORM", "Health platform"
    GATEWAY = "GATEWAY", "Gateway"
    API = "API", "API"


class MeasurementQuality(models.TextChoices):
    UNKNOWN = "UNKNOWN", "Unknown"
    VALID = "VALID", "Valid"
    SUSPECT = "SUSPECT", "Suspect"
    INVALID = "INVALID", "Invalid"


WORKFLOW_DEVICE_REGISTER = "device.register"
WORKFLOW_DEVICE_UPDATE = "device.update"
WORKFLOW_DEVICE_PAIR = "device.pair"
WORKFLOW_DEVICE_UNPAIR = "device.unpair"
WORKFLOW_DEVICE_CONNECT = "device.connect"
WORKFLOW_DEVICE_DISCONNECT = "device.disconnect"
WORKFLOW_DEVICE_ASSOCIATE = "device.associate_patient"
WORKFLOW_DEVICE_DISSOCIATE = "device.dissociate_patient"
WORKFLOW_DEVICE_INGEST = "device.ingest_telemetry"
WORKFLOW_DEVICE_SYNC = "device.sync"
WORKFLOW_DEVICE_RETIRE = "device.retire"
