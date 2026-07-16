"""
Signal registration for the Audit application.

The Audit application provides the infrastructure for recording
audit events. Domain-specific applications (Accounts, RBAC,
Organizations, Clinical modules, etc.) are responsible for
registering and handling their own signals and should delegate
audit recording to AuditService.

This module is reserved for future platform-wide signal
registrations if required.
"""

from __future__ import annotations

__all__: list[str] = []
