from __future__ import annotations


class OrganizationContextMixin:
    """
    Inject organization context
    into API requests.
    """

    def get_api_client(
        self,
    ):
        """
        Return authenticated API client
        with organization context.
        """

        self.client.force_authenticate(
            user=self.user,
        )

        self.client.credentials(
            HTTP_X_ORGANIZATION_ID=str(self.organization.id),
        )

        return self.client
