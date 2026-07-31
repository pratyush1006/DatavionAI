"""
Documents bounded context.
"""

from __future__ import annotations

from django.apps import AppConfig


class DocumentsConfig(
    AppConfig,
):
    """
    Document management application.
    """

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.documents"

    verbose_name = "Document Management"

    _initialized = False

    def ready(
        self,
    ) -> None:
        """
        Register document workflows.
        """

        if self._initialized:
            return

        self._initialized = True

        from apps.documents.workflows.registry import (
            register_document_workflows,
        )

        register_document_workflows()
