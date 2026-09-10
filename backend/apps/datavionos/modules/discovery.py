"""
Dynamic DatavionOS module discovery.

Module definitions are discovered by convention from ``*_module.py`` files
inside this package. The discovery engine knows no healthcare module names.
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil
from collections.abc import Iterable
from types import ModuleType

from apps.datavionos.contracts.module import ModuleContract


def discover_module_factories() -> tuple[object, ...]:
    """Discover zero-argument module factory functions dynamically."""

    package = importlib.import_module(__package__)
    discovered: list[object] = []

    for entry in sorted(pkgutil.iter_modules(package.__path__), key=lambda item: item.name):
        if not entry.name.endswith("_module"):
            continue
        module = importlib.import_module(f"{__package__}.{entry.name}")
        discovered.extend(_factories_from_module(module))

    return tuple(discovered)


def _factories_from_module(module: ModuleType) -> Iterable[object]:
    """Return local zero-argument functions producing ModuleContract."""

    for _, candidate in inspect.getmembers(module, inspect.isfunction):
        if candidate.__module__ != module.__name__:
            continue
        if candidate.__name__.startswith("_"):
            continue
        signature = inspect.signature(candidate)
        if any(
            parameter.kind in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            ) and parameter.default is inspect.Parameter.empty
            for parameter in signature.parameters.values()
        ):
            continue
        try:
            result = candidate()
        except TypeError:
            continue
        if isinstance(result, ModuleContract):
            yield candidate


def discover_modules() -> tuple[ModuleContract, ...]:
    """Instantiate, validate, and return all discovered module contracts."""

    modules = tuple(factory() for factory in discover_module_factories())
    seen: set[str] = set()
    duplicates: set[str] = set()
    for module in modules:
        if module.identifier in seen:
            duplicates.add(module.identifier)
        seen.add(module.identifier)
        module.validate()
    if duplicates:
        raise RuntimeError(
            "Duplicate DatavionOS module identifiers discovered: "
            + ", ".join(sorted(duplicates))
        )
    return modules


__all__ = [
    "discover_module_factories",
    "discover_modules",
]
