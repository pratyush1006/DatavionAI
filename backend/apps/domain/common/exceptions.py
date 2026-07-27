"""
Domain exception hierarchy.
"""

from __future__ import annotations


class DomainException(
    Exception,
):
    """
    Base domain exception.
    """


class BusinessRuleViolationException(
    DomainException,
):
    """
    Raised when a business rule is violated.
    """


class InvalidAggregateStateException(
    DomainException,
):
    """
    Raised when an aggregate enters an invalid state.
    """


class InvalidValueObjectException(
    DomainException,
):
    """
    Raised when a value object cannot be created.
    """


class ConcurrencyViolationException(
    DomainException,
):
    """
    Raised when optimistic concurrency fails.
    """


__all__ = [
    "BusinessRuleViolationException",
    "ConcurrencyViolationException",
    "DomainException",
    "InvalidAggregateStateException",
    "InvalidValueObjectException",
]
