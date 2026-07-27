"""
AI models.
"""

from __future__ import annotations

from apps.ai.models.knowledge import (
    DocumentChunk,
    KnowledgeDocument,
)
from apps.ai.models.model import AIModel
from apps.ai.models.prediction import Prediction
from apps.ai.models.prompt import PromptTemplate
from apps.ai.models.recommendation import Recommendation

__all__ = [
    "AIModel",
    "DocumentChunk",
    "KnowledgeDocument",
    "Prediction",
    "PromptTemplate",
    "Recommendation",
]
