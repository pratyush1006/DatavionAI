"""Register Organization admin models when Django autodiscovers this package."""

from .organization import OrganizationAdmin

__all__ = [
    "OrganizationAdmin",
]
