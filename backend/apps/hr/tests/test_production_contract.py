from __future__ import annotations

import importlib
from pathlib import Path

from django.apps import apps
from django.db import models

REQUIRED = (
    "attendance",
    "holidays",
    "leave",
    "onboarding",
    "payroll",
    "performance",
    "shifts",
)


def _roots() -> dict[str, Path]:
    result: dict[str, Path] = {}
    base = Path(__file__).resolve().parents[1]
    for root in (base, base.parent / "human_resources"):
        if not root.exists():
            continue
        for child in root.iterdir():
            if (
                child.is_dir()
                and not child.name.startswith("_")
                and (child / "__init__.py").exists()
            ):
                result.setdefault(child.name, child)
    return result


def test_required_domains_exist() -> None:
    roots = _roots()
    missing = [name for name in REQUIRED if name not in roots]
    assert not missing, f"Missing HR domains: {missing}"


def test_required_domains_registered() -> None:
    names = {c.name for c in apps.get_app_configs()}
    missing = [
        name for name in REQUIRED if not any(x.endswith(f".{name}") for x in names)
    ]
    assert not missing, f"HR domains not registered: {missing}"


def test_hr_import_closure() -> None:
    failures: list[str] = []
    roots = _roots()
    for name in REQUIRED:
        root = roots.get(name)
        if root is None:
            continue
        module = ".".join(root.relative_to(Path(__file__).resolve().parents[3]).parts)
        try:
            importlib.import_module(module)
        except Exception as exc:
            failures.append(f"{module}: {exc}")
    assert not failures, " | ".join(failures)


def _has_effective_tenant_scope(model, seen: set[type] | None = None) -> bool:
    """Return whether a model is directly or transitively organization scoped."""
    if seen is None:
        seen = set()
    if model in seen:
        return False
    seen.add(model)

    direct_fields = {field.name for field in model._meta.get_fields()}
    if "organization" in direct_fields or "tenant" in direct_fields:
        return True

    for field in model._meta.get_fields():
        if getattr(field, "auto_created", False):
            continue
        related_model = getattr(field, "related_model", None)
        if related_model is None:
            continue
        if _has_effective_tenant_scope(related_model, seen):
            return True
    return False


def test_hr_models_have_effective_tenant_scope() -> None:
    violations: list[str] = []
    for config in apps.get_app_configs():
        if not config.name.startswith(("apps.hr.", "apps.human_resources.")):
            continue
        for model in config.get_models():
            if not _has_effective_tenant_scope(model):
                violations.append(model._meta.label)
    assert not violations, (
        "HR models missing effective organization/tenant scope: "
        + ", ".join(sorted(violations))
    )


def test_hr_money_fields_are_decimal() -> None:
    tokens = (
        "salary",
        "amount",
        "pay",
        "rate",
        "bonus",
        "deduction",
        "tax",
        "gross",
        "net",
        "allowance",
    )
    violations: list[str] = []
    for config in apps.get_app_configs():
        if not config.name.startswith(("apps.hr.", "apps.human_resources.")):
            continue
        for model in config.get_models():
            for field in model._meta.get_fields():
                if any(token in field.name.lower() for token in tokens) and isinstance(
                    field, models.FloatField
                ):
                    violations.append(f"{model._meta.label}.{field.name}")
    assert not violations, "HR financial FloatFields: " + ", ".join(sorted(violations))


def test_no_anonymous_hr_api() -> None:
    violations: list[str] = []
    for root in _roots().values():
        for path in root.rglob("*.py"):
            if "tests" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            if "AllowAny" in text and "api" in path.parts:
                violations.append(str(path))
    assert not violations, "Anonymous HR API detected: " + ", ".join(violations)


def test_no_naive_datetime_now() -> None:
    violations: list[str] = []
    for root in _roots().values():
        for path in root.rglob("*.py"):
            if "tests" in path.parts:
                continue
            if "datetime.now()" in path.read_text(encoding="utf-8"):
                violations.append(str(path))
    assert not violations, "Naive datetime.now() detected: " + ", ".join(violations)
