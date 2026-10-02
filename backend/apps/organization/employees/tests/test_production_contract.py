from __future__ import annotations

import importlib

from django.apps import apps
from django.db import models

PACKAGE = "apps.organization.employees"


def test_employee_package_imports() -> None:
    importlib.import_module(PACKAGE)
    for module in (
        f"{PACKAGE}.models",
        f"{PACKAGE}.services",
        f"{PACKAGE}.selectors",
        f"{PACKAGE}.permissions",
        f"{PACKAGE}.policies",
    ):
        importlib.import_module(module)


def test_employee_app_registered() -> None:
    assert PACKAGE in {c.name for c in apps.get_app_configs()}


def _has_effective_tenant_scope(model, seen: set[type] | None = None) -> bool:
    if seen is None:
        seen = set()
    if model in seen:
        return False
    seen.add(model)
    fields = {field.name for field in model._meta.get_fields()}
    if "organization" in fields or "tenant" in fields:
        return True
    for field in model._meta.get_fields():
        if getattr(field, "auto_created", False):
            continue
        related_model = getattr(field, "related_model", None)
        if related_model is not None and _has_effective_tenant_scope(
            related_model, seen
        ):
            return True
    return False


def test_employee_models_tenant_scoped() -> None:
    config = apps.get_app_config("employees")
    violations: list[str] = []
    for model in config.get_models():
        if not _has_effective_tenant_scope(model):
            violations.append(model._meta.label)
    assert not violations, (
        "Employee models missing effective organization/tenant scope: "
        + ", ".join(sorted(violations))
    )


def test_employee_financial_fields_are_decimal() -> None:
    config = apps.get_app_config("employees")
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
    for model in config.get_models():
        for field in model._meta.get_fields():
            if any(token in field.name.lower() for token in tokens) and isinstance(
                field, models.FloatField
            ):
                violations.append(f"{model._meta.label}.{field.name}")
    assert not violations, "Employee financial FloatFields: " + ", ".join(
        sorted(violations)
    )
