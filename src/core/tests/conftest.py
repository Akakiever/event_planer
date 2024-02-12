import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from core.models import Event


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username='user1',
        email='user1@example.com',
        password='qd1_dsa@As',
        first_name='User',
        last_name='One',
    )


@pytest.fixture
def user_token(user):
    Token.objects.create(user=user)


@pytest.fixture
def api_user_client(user, user_token):
    api_client = APIClient()
    api_client.force_authenticate(user=user, token=user_token)
    return api_client


@pytest.fixture
def user2():
    return User.objects.create_user(
        username='user2',
        email='user2@example.com',
        password='qd1_dsa@As',
        first_name='User',
        last_name='Two',
    )


@pytest.fixture
def user2_token(user2):
    Token.objects.create(user=user2)


@pytest.fixture
def api_user2_client(user2, user2_token):
    api_client = APIClient()
    api_client.force_authenticate(user=user2, token=user2_token)
    return api_client


@pytest.fixture
def simple_event(user):
    return baker.make(
        Event,
        title='Title',
        description='Description',
        location='Location',
        organizer=user
    )


@pytest.fixture
def simple_event2(user2):
    return baker.make(
        Event,
        title='eltiT',
        description='noitpircseD',
        location='noitacoL',
        organizer=user2
    )
