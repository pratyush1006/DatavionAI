"""Tests for metadata-driven DatavionOS module discovery."""

from __future__ import annotations

from django.test import SimpleTestCase

from apps.datavionos.modules.discovery import discover_modules
from apps.datavionos.registries.module import module_registry


class ModuleDiscoveryTests(SimpleTestCase):
    """Validate dynamic discovery and dependency ordering."""

    def test_modules_are_discovered_dynamically(self) -> None:
        modules = discover_modules()
        self.assertTrue(modules)
        identifiers = {module.identifier for module in modules}
        self.assertEqual(len(identifiers), len(modules))

    def test_dependency_order_is_dependency_first(self) -> None:
        modules = discover_modules()
        ordered = module_registry.dependency_order(modules)
        positions = {module.identifier: index for index, module in enumerate(ordered)}
        for module in modules:
            for dependency in module.dependencies:
                self.assertLess(positions[dependency], positions[module.identifier])
