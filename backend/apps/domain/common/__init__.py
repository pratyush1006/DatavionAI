"""
Common domain building blocks.
"""

from apps.domain.common.aggregate import (
    AggregateRoot,
)
from apps.domain.common.domain_event import (
    DomainEvent,
)
from apps.domain.common.entity import (
    Entity,
)
from apps.domain.common.exceptions import (
    BusinessRuleViolationException,
    ConcurrencyViolationException,
    DomainException,
    InvalidAggregateStateException,
    InvalidValueObjectException,
)
from apps.domain.common.factory import (
    Factory,
)
from apps.domain.common.repository import (
    Repository,
)
from apps.domain.common.service import (
    DomainService,
)
from apps.domain.common.specification import (
    AndSpecification,
    NotSpecification,
    OrSpecification,
    Specification,
)
from apps.domain.common.value_object import (
    ValueObject,
)

__all__ = [
    # Core
    "AggregateRoot",
    "DomainEvent",
    "Entity",
    "ValueObject",
    # Domain Patterns
    "Repository",
    "Factory",
    "DomainService",
    "Specification",
    "AndSpecification",
    "OrSpecification",
    "NotSpecification",
    # Exceptions
    "DomainException",
    "BusinessRuleViolationException",
    "InvalidAggregateStateException",
    "InvalidValueObjectException",
    "ConcurrencyViolationException",
]
