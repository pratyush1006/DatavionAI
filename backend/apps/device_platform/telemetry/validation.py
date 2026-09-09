from decimal import Decimal


def validate_measurement(*, measurement_type: str, value, unit: str) -> None:
    if not measurement_type or len(measurement_type) > 60:
        raise ValueError("measurement_type is required and must be <= 60 characters.")
    if value is not None:
        Decimal(str(value))
    if unit and len(unit) > 40:
        raise ValueError("unit must be <= 40 characters.")
