"""
DatavionOS notification framework.

Provides the public API for platform notification capabilities.

Supports:

- Notification definitions
- Multiple delivery channels
- Channel registration
- Runtime dispatching
- Provider-independent delivery

Business applications should import notification utilities from
this package instead of internal modules.
"""

from __future__ import annotations

from .channels import (
    EmailNotificationChannel,
    InAppNotificationChannel,
    NotificationChannel,
    PushNotificationChannel,
    SMSNotificationChannel,
    WebhookNotificationChannel,
)
from .config import (
    DEFAULT_NOTIFICATION_DELIVERY_CONFIGURATION,
    NotificationConfiguration,
    NotificationDeliveryConfiguration,
)
from .constants import (
    CHANNEL_EMAIL,
    CHANNEL_IN_APP,
    CHANNEL_PUSH,
    CHANNEL_SMS,
    CHANNEL_WEBHOOK,
    DEFAULT_CHANNEL,
    DEFAULT_PRIORITY,
    DEFAULT_STATUS,
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_LOW,
    PRIORITY_NORMAL,
    STATUS_CANCELLED,
    STATUS_DELIVERED,
    STATUS_FAILED,
    STATUS_PENDING,
    STATUS_QUEUED,
    STATUS_SENT,
)
from .dispatcher import (
    NotificationDispatcher,
    notification_dispatcher,
)
from .exceptions import (
    NotificationAlreadyRegisteredError,
    NotificationChannelError,
    NotificationConfigurationError,
    NotificationDispatchError,
    NotificationError,
    NotificationNotFoundError,
    NotificationProviderError,
    NotificationRecipientError,
    NotificationRegistrationError,
    NotificationTemplateError,
)
from .models import (
    Notification,
    NotificationDelivery,
    NotificationRecipient,
    NotificationResult,
)
from .registry import (
    NotificationChannelRegistry,
    notification_channel_registry,
)
from .services import (
    NotificationService,
    notification_service,
)
from .types import (
    NotificationChannel,
    NotificationID,
    NotificationMetadata,
    NotificationName,
    NotificationPayload,
    RecipientAddress,
    RecipientID,
    TemplateName,
)

__all__: tuple[str, ...] = (
    # Models
    "Notification",
    "NotificationDelivery",
    "NotificationRecipient",
    "NotificationResult",
    # Services
    "NotificationService",
    "notification_service",
    # Dispatcher
    "NotificationDispatcher",
    "notification_dispatcher",
    # Channels
    "NotificationChannel",
    "EmailNotificationChannel",
    "SMSNotificationChannel",
    "PushNotificationChannel",
    "InAppNotificationChannel",
    "WebhookNotificationChannel",
    # Registry
    "NotificationChannelRegistry",
    "notification_channel_registry",
    # Configuration
    "NotificationConfiguration",
    "NotificationDeliveryConfiguration",
    "DEFAULT_NOTIFICATION_DELIVERY_CONFIGURATION",
    # Types
    "NotificationID",
    "NotificationName",
    "NotificationMetadata",
    "NotificationPayload",
    "RecipientID",
    "RecipientAddress",
    "TemplateName",
    # Constants
    "CHANNEL_EMAIL",
    "CHANNEL_SMS",
    "CHANNEL_PUSH",
    "CHANNEL_IN_APP",
    "CHANNEL_WEBHOOK",
    "DEFAULT_CHANNEL",
    "DEFAULT_PRIORITY",
    "DEFAULT_STATUS",
    "PRIORITY_LOW",
    "PRIORITY_NORMAL",
    "PRIORITY_HIGH",
    "PRIORITY_CRITICAL",
    "STATUS_PENDING",
    "STATUS_QUEUED",
    "STATUS_SENT",
    "STATUS_DELIVERED",
    "STATUS_FAILED",
    "STATUS_CANCELLED",
    # Exceptions
    "NotificationError",
    "NotificationConfigurationError",
    "NotificationNotFoundError",
    "NotificationAlreadyRegisteredError",
    "NotificationRegistrationError",
    "NotificationChannelError",
    "NotificationProviderError",
    "NotificationDispatchError",
    "NotificationTemplateError",
    "NotificationRecipientError",
)
