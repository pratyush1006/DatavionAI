"""Stable AI platform enums and defaults."""

from __future__ import annotations

import os

from django.db import models


class AIApplicationCode(models.TextChoices):
    CLINICAL_AI = "CLINICAL_AI", "Clinical AI"
    LABORATORY_AI = "LABORATORY_AI", "Laboratory AI"
    PHARMACY_AI = "PHARMACY_AI", "Pharmacy AI"
    IMAGING_AI = "IMAGING_AI", "Imaging AI"
    REVENUE_CYCLE_AI = "REVENUE_CYCLE_AI", "Revenue Cycle AI"


class AIApplicationStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"


class AIProviderType(models.TextChoices):
    OPENAI = "openai", "OpenAI"
    GEMINI = "gemini", "Gemini"
    MOCK = "mock", "Mock"


class AIRequestStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCEEDED = "succeeded", "Succeeded"
    FAILED = "failed", "Failed"


class AIMessageRole(models.TextChoices):
    SYSTEM = "system", "System"
    USER = "user", "User"
    ASSISTANT = "assistant", "Assistant"
    TOOL = "tool", "Tool"


class KnowledgeSourceType(models.TextChoices):
    TEXT = "text", "Text"
    FILE = "file", "File"
    URL = "url", "URL"
    DOMAIN = "domain", "Domain"


class KnowledgeDocumentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    INDEXED = "indexed", "Indexed"
    FAILED = "failed", "Failed"


DEFAULT_MODEL = (
    os.environ.get("AI_DEFAULT_MODEL", "gpt-4o-mini")
    if "os" in globals()
    else "gpt-4o-mini"
)
DEFAULT_TEMPERATURE = 0.0
DEFAULT_TOP_K = 5
MAX_PROMPT_LENGTH = 100_000
