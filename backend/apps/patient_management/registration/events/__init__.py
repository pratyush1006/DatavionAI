"""
Patient Registration domain event exports.
"""

from apps.patient_management.registration.events.registration_cancelled import (
    RegistrationCancelledEvent,
)
from apps.patient_management.registration.events.registration_checked_in import (
    RegistrationCheckedInEvent,
)
from apps.patient_management.registration.events.registration_completed import (
    RegistrationCompletedEvent,
)
from apps.patient_management.registration.events.registration_created import (
    RegistrationCreatedEvent,
)
from apps.patient_management.registration.events.registration_deleted import (
    RegistrationDeletedEvent,
)
from apps.patient_management.registration.events.registration_no_show import (
    RegistrationNoShowEvent,
)
from apps.patient_management.registration.events.registration_rejected import (
    RegistrationRejectedEvent,
)
from apps.patient_management.registration.events.registration_updated import (
    RegistrationUpdatedEvent,
)
from apps.patient_management.registration.events.registration_verified import (
    RegistrationVerifiedEvent,
)

__all__ = (
    "RegistrationCancelledEvent",
    "RegistrationCheckedInEvent",
    "RegistrationCompletedEvent",
    "RegistrationCreatedEvent",
    "RegistrationDeletedEvent",
    "RegistrationNoShowEvent",
    "RegistrationRejectedEvent",
    "RegistrationUpdatedEvent",
    "RegistrationVerifiedEvent",
)
