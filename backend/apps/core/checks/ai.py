"""
AI provider system checks for the DatavionOS platform.

Validates AI infrastructure configuration.
"""

from __future__ import annotations

from django.conf import settings
from django.core.checks import Error, Tags, Warning, register


@register(Tags.compatibility)
def ai_provider_check(
    app_configs,
    **kwargs,
):
    """
    Validate AI provider configuration.
    """

    messages = []

    provider = getattr(
        settings,
        "AI_PROVIDER",
        None,
    )

    if not provider:
        messages.append(
            Warning(
                "AI_PROVIDER is not configured.",
                hint=(
                    "Configure OpenAI, Azure OpenAI, Gemini, "
                    "Anthropic or another supported provider."
                ),
                id="datavion.W005",
            )
        )

        return messages

    provider = provider.lower()

    # --------------------------------------------------------------
    # OpenAI
    # --------------------------------------------------------------

    if provider == "openai":
        if not getattr(
            settings,
            "OPENAI_API_KEY",
            None,
        ):
            messages.append(
                Error(
                    "OPENAI_API_KEY is not configured.",
                    hint=("Configure OpenAI credentials before enabling AI features."),
                    id="datavion.E007",
                )
            )

    # --------------------------------------------------------------
    # Azure OpenAI
    # --------------------------------------------------------------

    elif provider in {
        "azure",
        "azure_openai",
    }:
        required = [
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT",
        ]

        for setting in required:
            if not getattr(
                settings,
                setting,
                None,
            ):
                messages.append(
                    Error(
                        f"{setting} is not configured.",
                        hint=("Configure Azure OpenAI settings."),
                        id="datavion.E008",
                    )
                )

    # --------------------------------------------------------------
    # Gemini
    # --------------------------------------------------------------

    elif provider == "gemini":
        if not getattr(
            settings,
            "GEMINI_API_KEY",
            None,
        ):
            messages.append(
                Error(
                    "GEMINI_API_KEY is not configured.",
                    hint=("Configure Gemini credentials."),
                    id="datavion.E009",
                )
            )

    # --------------------------------------------------------------
    # Anthropic
    # --------------------------------------------------------------

    elif provider == "anthropic":
        if not getattr(
            settings,
            "ANTHROPIC_API_KEY",
            None,
        ):
            messages.append(
                Error(
                    "ANTHROPIC_API_KEY is not configured.",
                    hint=("Configure Anthropic credentials."),
                    id="datavion.E010",
                )
            )

    else:
        messages.append(
            Warning(
                f"Unknown AI provider '{provider}'.",
                hint=("Use a supported AI provider."),
                id="datavion.W016",
            )
        )

    # --------------------------------------------------------------
    # Model configuration
    # --------------------------------------------------------------

    if not getattr(
        settings,
        "AI_MODEL",
        None,
    ):
        messages.append(
            Warning(
                "AI_MODEL is not configured.",
                hint=("Configure the default LLM model."),
                id="datavion.W017",
            )
        )

    return messages


__all__ = [
    "ai_provider_check",
]
