"""Prompt rendering with explicit variable validation."""

from __future__ import annotations

import re

from apps.ai.exceptions import AIValidationError


def render(template: str, variables: dict) -> str:
    names = set(re.findall(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", template))
    missing = sorted(names - set(variables))
    if missing:
        raise AIValidationError("Missing prompt variables: " + ", ".join(missing))
    try:
        return template.format(**variables)
    except (KeyError, ValueError) as exc:
        raise AIValidationError(str(exc)) from exc
