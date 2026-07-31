"""
Public contracts exposed by the DatavionOS kernel.

Contracts define the stable interfaces and immutable data structures shared
between the DatavionOS kernel, platform services, plugins, and applications.

The contract layer must remain:

- Framework agnostic where possible.
- Backward compatible across minor releases.
- Free of runtime side effects.
- Independent from concrete implementations.

Only stable public contracts should be re-exported from this package.
"""

from __future__ import annotations

from apps.datavionos.contracts.base import (
    BaseContract,
)
from apps.datavionos.contracts.metadata import (
    ContractMetadata,
)

__all__ = [
    "BaseContract",
    "ContractMetadata",
]
