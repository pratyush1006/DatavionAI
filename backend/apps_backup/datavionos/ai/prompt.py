"""
Prompt engine contracts.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PromptTemplate:
    """
    Immutable prompt template.
    """

    name: str

    template: str

    version: str = "1.0"

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class PromptRequest:
    """
    Immutable prompt rendering request.
    """

    template: PromptTemplate

    variables: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class PromptResponse:
    """
    Immutable rendered prompt.
    """

    prompt: str

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@runtime_checkable
class PromptEngine(
    Protocol,
):
    """
    Prompt rendering engine.
    """

    async def render(
        self,
        request: PromptRequest,
    ) -> PromptResponse:
        """
        Render a prompt from a template.
        """

    async def validate(
        self,
        template: PromptTemplate,
    ) -> bool:
        """
        Validate a prompt template.
        """


__all__ = [
    "PromptEngine",
    "PromptRequest",
    "PromptResponse",
    "PromptTemplate",
]
