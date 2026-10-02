"""OpenAPI authentication extensions for shared project authenticators."""

from drf_spectacular.extensions import OpenApiAuthenticationExtension


class TenantJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    """Document the tenant-aware JWT authenticator as bearer JWT auth."""

    target_class = "apps.platform.tenancy.authentication.TenantJWTAuthentication"
    name = "BearerAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
