"""
Audit logging utilities for DatavionAI.

Business modules should never log directly.
Always use log_audit_event().
"""

import logging

audit_logger = logging.getLogger("audit")


def log_audit_event(
    *,
    action: str,
    resource: str,
    message: str,
    user_id: int | None = None,
    resource_id: int | None = None,
) -> None:
    """
    Log an audit event.

    Example:
        log_audit_event(
            action="CREATE",
            resource="Employee",
            resource_id=101,
            user_id=5,
            message="Employee created successfully.",
        )
    """

    audit_logger.info(
        ("ACTION=%s " "RESOURCE=%s " "RESOURCE_ID=%s " "USER_ID=%s " "MESSAGE=%s"),
        action,
        resource,
        resource_id,
        user_id,
        message,
    )
