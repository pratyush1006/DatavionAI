"""
AI contract definitions.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
)
from enum import StrEnum

from apps.datavionos.contracts.base import (
    BaseContract,
)


class AIType(StrEnum):
    """
    Supported AI capability types.
    """

    LLM = "llm"
    EMBEDDINGS = "embeddings"
    AGENT = "agent"
    VISION = "vision"
    SPEECH = "speech"
    ORCHESTRATION = "orchestration"


class AIProvider(StrEnum):
    """
    Supported AI providers.
    """

    OPENAI = "openai"
    AZURE = "azure"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    LOCAL = "local"


class AIStatus(StrEnum):
    """
    AI capability status.
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AIContract(BaseContract):
    """
    Immutable AI definition.

    Represents an AI capability registered
    within DatavionOS including LLMs,
    AI agents, embeddings, speech,
    vision and orchestration services.
    """

    identifier: str

    display_name: str

    ai_type: AIType

    provider: AIProvider

    model: str

    version: str = "1.0.0"

    description: str = ""

    enabled: bool = True

    system: bool = False

    multimodal: bool = False

    streaming: bool = True

    supports_tools: bool = True

    supports_memory: bool = True

    supports_reasoning: bool = True

    @property
    def has_tools(self) -> bool:
        """
        Whether tools are configured.
        """

        return bool(
            self.supports_tools,
        )

    @property
    def has_dependencies(self) -> bool:
        """
        Whether dependencies exist.
        """

        return bool(
            self.supports_memory,
        )

    @property
    def qualified_name(self) -> str:
        """
        Qualified AI identifier.
        """

        return f"{self.provider.value}/{self.model}:{self.version}"

    @property
    def supports_tool_calling(self) -> bool:
        """
        Whether tool calling is supported.
        """

        return self.supports_tools

    @property
    def supports_long_term_memory(self) -> bool:
        """
        Whether memory integration is supported.
        """

        return self.supports_memory


__all__ = [
    "AIContract",
    "AIType",
    "AIProvider",
    "AIStatus",
]
