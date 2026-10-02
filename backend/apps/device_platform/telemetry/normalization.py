NORMALIZED_TYPES = {
    "hr": ("HEART_RATE", "bpm"),
    "heart_rate": ("HEART_RATE", "bpm"),
    "spo2": ("SPO2", "%"),
    "oxygen_saturation": ("SPO2", "%"),
    "temperature": ("TEMPERATURE", "C"),
    "weight": ("WEIGHT", "kg"),
    "steps": ("STEPS", "count"),
}


def normalize_measurement(
    measurement_type: str, value, unit: str | None = None
) -> tuple[str, object, str]:
    key = measurement_type.strip().lower()
    normalized_type, default_unit = NORMALIZED_TYPES.get(
        key, (measurement_type.upper(), unit or "")
    )
    return normalized_type, value, unit or default_unit
