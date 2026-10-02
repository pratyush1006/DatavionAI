"""
Platform bootstrap lifecycle.

Responsible for initializing the DatavionOS kernel runtime.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from apps.core.registry import (
    feature_registry,
    module_registry,
    permission_registry,
    provider_registry,
)

logger = logging.getLogger(__name__)


@dataclass(
    frozen=True,
    slots=True,
)
class BootstrapState:
    """
    Immutable bootstrap execution state.
    """

    initialized: bool = False


_bootstrap_state = BootstrapState()


def initialize_registries() -> None:
    """
    Initialize platform registries.

    Registry population should happen through application
    modules registering themselves during startup.
    """

    logger.info(
        "Initializing DatavionOS registries.",
    )

    # Access registries to ensure kernel availability.
    registries = (
        module_registry,
        feature_registry,
        permission_registry,
        provider_registry,
    )

    logger.debug(
        "Loaded %s platform registries.",
        len(registries),
    )


def bootstrap_platform() -> None:
    """
    Bootstrap DatavionOS kernel.

    This operation is idempotent and safe to call multiple
    times during application lifecycle initialization.
    """

    global _bootstrap_state

    if _bootstrap_state.initialized:
        logger.debug(
            "DatavionOS bootstrap already completed.",
        )
        return

    logger.info(
        "Bootstrapping DatavionOS platform.",
    )

    initialize_registries()

    _bootstrap_state = BootstrapState(
        initialized=True,
    )

    logger.info(
        "DatavionOS bootstrap completed successfully.",
    )


def is_bootstrapped() -> bool:
    """
    Return whether platform bootstrap completed.
    """

    return _bootstrap_state.initialized


__all__ = [
    "BootstrapState",
    "bootstrap_platform",
    "initialize_registries",
    "is_bootstrapped",
]
