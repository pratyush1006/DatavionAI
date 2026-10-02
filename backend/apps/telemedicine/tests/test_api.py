import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_session_list_is_tenant_scoped(user, session):
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/telemedicine/sessions/")
    assert response.status_code == 200
