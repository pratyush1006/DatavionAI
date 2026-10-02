"""
Event constants for DatavionOS.

Defines framework-wide constants used by the event infrastructure.

These constants establish the standard event contract used across:

- Audit
- Workflow
- Notifications
- Analytics
- Integrations
- AI automation
"""

from __future__ import annotations

###############################################################################
# Event Metadata Keys
###############################################################################

EVENT_ID_FIELD = "event_id"

EVENT_NAME_FIELD = "event_name"

EVENT_VERSION_FIELD = "event_version"

EVENT_SOURCE_FIELD = "source"

EVENT_TIMESTAMP_FIELD = "timestamp"


###############################################################################
# Request Context Fields
###############################################################################

REQUEST_ID_FIELD = "request_id"

CORRELATION_ID_FIELD = "correlation_id"


###############################################################################
# Identity Context Fields
###############################################################################

USER_ID_FIELD = "user_id"

TENANT_ID_FIELD = "tenant_id"

ORGANIZATION_ID_FIELD = "organization_id"


###############################################################################
# Event State Fields
###############################################################################

EVENT_PAYLOAD_FIELD = "payload"

EVENT_METADATA_FIELD = "metadata"


###############################################################################
# Default Values
###############################################################################

DEFAULT_EVENT_VERSION = "1.0"

DEFAULT_EVENT_SOURCE = "datavionos"


###############################################################################
# Event Naming Convention
###############################################################################

EVENT_SEPARATOR = "."

EVENT_CREATED_SUFFIX = "created"

EVENT_UPDATED_SUFFIX = "updated"

EVENT_DELETED_SUFFIX = "deleted"


###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
    "CORRELATION_ID_FIELD",
    "DEFAULT_EVENT_SOURCE",
    "DEFAULT_EVENT_VERSION",
    "EVENT_CREATED_SUFFIX",
    "EVENT_DELETED_SUFFIX",
    "EVENT_ID_FIELD",
    "EVENT_METADATA_FIELD",
    "EVENT_NAME_FIELD",
    "EVENT_PAYLOAD_FIELD",
    "EVENT_SEPARATOR",
    "EVENT_SOURCE_FIELD",
    "EVENT_TIMESTAMP_FIELD",
    "EVENT_UPDATED_SUFFIX",
    "EVENT_VERSION_FIELD",
    "ORGANIZATION_ID_FIELD",
    "REQUEST_ID_FIELD",
    "TENANT_ID_FIELD",
    "USER_ID_FIELD",
)
