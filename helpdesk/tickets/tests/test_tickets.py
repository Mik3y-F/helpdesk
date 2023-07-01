import pytest
from rest_framework import status


@pytest.fixture
def create_ticket(api_client):
    def do_create_ticket(ticket):
        return api_client.post("/api/tickets/", ticket)

    return do_create_ticket


@pytest.mark.django_db
class TestCreateTicket:
    def test_if_user_is_anonymous_returns_401(self, create_ticket):
        response = create_ticket({"title": "a"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_valid_returns_201(self, create_ticket, authenticate, user):
        authenticate()

        response = create_ticket({"title": "a", "description": "b", "user": user.pk})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0

    def test_if_data_is_invalid_returns_400(self, create_ticket, authenticate):
        authenticate()

        response = create_ticket({"title": "a"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
