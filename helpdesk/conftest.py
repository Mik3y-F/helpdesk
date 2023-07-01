import pytest

from helpdesk.users.models import User
from helpdesk.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def authenticate(api_client, user):
    def do_authenticate_user(is_staff=False):
        user.is_staff = is_staff
        api_client.force_authenticate(user=user)

    return do_authenticate_user
