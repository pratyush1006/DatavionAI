"""
Notification template service.
"""

from __future__ import annotations

from django.template.loader import render_to_string


class NotificationTemplateService:
    """
    Render notification templates.
    """

    @staticmethod
    def render(
        *,
        template: str,
        context: dict,
    ) -> str:
        """
        Render an HTML notification template.
        """

        return render_to_string(
            f"email/{template}.html",
            context,
        )


__all__ = [
    "NotificationTemplateService",
]
