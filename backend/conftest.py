import pytest


@pytest.fixture(autouse=True)
def disable_ssl_redirect_for_test_client(settings):
    """Keep in-process API tests focused on application behavior.

    Production HTTPS enforcement is validated by Django deployment checks and
    remains enabled in runtime settings. Django's APIClient issues HTTP by
    default, so without this test-only override it receives an HTTPS redirect
    before reaching the tested view.
    """
    settings.SECURE_SSL_REDIRECT = False
