from dataclasses import dataclass
from importlib import import_module

from django.apps import apps


@dataclass(frozen=True)
class IntegrationSpec:
    key: str
    package: str
    app_labels: tuple[str, ...]
    purpose: str


INTEGRATIONS = (
    IntegrationSpec(
        "patient",
        "apps.patient_management.patients.models",
        (),
        "Canonical patient identity.",
    ),
    IntegrationSpec(
        "encounters",
        "apps.encounters",
        ("encounters",),
        "Clinical encounter lifecycle.",
    ),
    IntegrationSpec(
        "laboratory",
        "apps.laboratories",
        ("laboratories",),
        "Laboratory workflow boundary.",
    ),
    IntegrationSpec(
        "pharmacy", "apps.pharmacy", ("pharmacy",), "Pharmacy workflow boundary."
    ),
    IntegrationSpec(
        "imaging", "apps.imaging", ("imaging",), "Diagnostic imaging boundary."
    ),
    IntegrationSpec(
        "rcm",
        "apps.revenue_cycle.billing",
        ("revenue_cycle_billing", "revenue_cycle"),
        "Canonical healthcare RCM billing boundary.",
    ),
    IntegrationSpec(
        "notifications",
        "apps.notifications",
        ("notifications",),
        "Operational notification boundary.",
    ),
    IntegrationSpec("audit", "apps.audit", ("audit",), "Operational audit boundary."),
    IntegrationSpec("ai", "apps.ai", ("ai",), "Canonical advisory AI boundary."),
)


def _importable(package: str) -> bool:
    try:
        import_module(package)
        return True
    except (ImportError, ModuleNotFoundError):
        return False


def _installed_config_for(spec: IntegrationSpec):
    for label in spec.app_labels:
        try:
            return apps.get_app_config(label)
        except LookupError:
            continue

    package_tail = spec.package.rsplit(".", 1)[-1]
    for config in apps.get_app_configs():
        config_name = getattr(config, "name", "")
        config_label = getattr(config, "label", "")
        if config_name == spec.package or config_name.endswith("." + package_tail):
            return config
        if config_label == package_tail:
            return config
    return None


def _patient_integration() -> dict[str, object]:
    try:
        patient = apps.get_model("patient_core", "Patient")
    except LookupError:
        return {
            "package": "apps.patient_management.patients.models",
            "purpose": "Canonical patient identity.",
            "app_labels": ("patient_core",),
            "installed": False,
            "importable": False,
            "resolved_app": None,
        }

    return {
        "package": "apps.patient_management.patients.models",
        "purpose": "Canonical patient identity.",
        "app_labels": ("patient_core",),
        "installed": True,
        "importable": patient.__module__
        == "apps.patient_management.patients.models.patient",
        "resolved_app": "patient_core",
    }


def discover_integrations() -> dict[str, dict[str, object]]:
    result = {"patient": _patient_integration()}

    for spec in INTEGRATIONS:
        if spec.key == "patient":
            continue
        config = _installed_config_for(spec)
        importable = _importable(spec.package)
        runtime_importable = importable or config is not None
        result[spec.key] = {
            "package": spec.package,
            "purpose": spec.purpose,
            "app_labels": () if config is None else (config.label,),
            "installed": config is not None,
            "importable": runtime_importable,
            "resolved_app": None if config is None else config.name,
        }
    return result


def require_integration(key: str) -> dict[str, object]:
    result = discover_integrations().get(key)
    if result is None:
        raise LookupError(f"Unknown Hospital Operations integration: {key}")
    if not result["installed"]:
        raise LookupError(f"Canonical integration unavailable: {key}")
    return result


def validate_canonical_integrations() -> dict[str, dict[str, object]]:
    result = discover_integrations()
    missing = [key for key, value in result.items() if not value["installed"]]
    if missing:
        details = "; ".join(
            f"{key}=expected_labels:{value['app_labels']} package:{value['package']}"
            for key, value in result.items()
            if key in missing
        )
        raise RuntimeError(
            "Hospital Operations canonical integration certification failed: "
            + ", ".join(sorted(missing))
            + " | "
            + details
        )

    patient = apps.get_model("patient_core", "Patient")
    if (
        patient._meta.label != "patient_core.Patient"
        or patient.__module__ != "apps.patient_management.patients.models.patient"
    ):
        raise RuntimeError(
            "Canonical patient integration contract failed: "
            "expected patient_core.Patient from "
            "apps.patient_management.patients.models"
        )
    return result
