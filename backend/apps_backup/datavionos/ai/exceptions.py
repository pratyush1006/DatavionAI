"""
AI exception hierarchy.
"""

from __future__ import annotations


class AIError(
    Exception,
):
    """
    Base AI exception.
    """


class AIProviderError(
    AIError,
):
    """
    Raised when an AI provider fails.
    """


class ChatModelError(
    AIError,
):
    """
    Raised when chat completion fails.
    """


class EmbeddingModelError(
    AIError,
):
    """
    Raised when embedding generation fails.
    """


class PromptEngineError(
    AIError,
):
    """
    Raised when prompt rendering fails.
    """


class VectorStoreError(
    AIError,
):
    """
    Raised when vector store operations fail.
    """


class RAGEngineError(
    AIError,
):
    """
    Raised when a retrieval-augmented generation workflow fails.
    """


class TokenLimitExceededError(
    AIError,
):
    """
    Raised when a request exceeds the supported token limit.
    """


__all__ = [
    "AIError",
    "AIProviderError",
    "ChatModelError",
    "EmbeddingModelError",
    "PromptEngineError",
    "VectorStoreError",
    "RAGEngineError",
    "TokenLimitExceededError",
]
