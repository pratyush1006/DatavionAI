"""
DatavionOS platform interface contracts.

This package exposes framework-independent capability contracts
used throughout the DatavionOS ecosystem.

Interfaces define behavior only and must not contain:

- Django models
- database logic
- service implementations
- infrastructure dependencies

Implemented capabilities include:

- Identity management
- Audit tracking
- Publication lifecycle
- Search indexing
- Version management
"""

from __future__ import annotations

from .auditable import (
    Auditable,
)
from .identifiable import (
    Identifiable,
)
from .publishable import (
    Publishable,
)
from .searchable import (
    Searchable,
)
from .versionable import (
    Versionable,
)

__all__: tuple[str, ...] = (
    "Auditable",
    "Identifiable",
    "Publishable",
    "Searchable",
    "Versionable",
)
