import base64

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def password():
    return '1234567'


@pytest.fixture
def user(django_user_model, password):
    return django_user_model.objects.create_user(
        username='TestUser1', password=password
    )


@pytest.fixture
def another_user(django_user_model, password):
    return django_user_model.objects.create_user(
        username='TestUser2', password=password
    )


@pytest.fixture
def user_client(user, password):
    client = APIClient()
    credentials = base64.b64encode(
        f"{user.username}:{password}".encode('utf-8')
    ).decode('utf-8')
    client.credentials(HTTP_AUTHORIZATION=f"Basic {credentials}")
    return client
