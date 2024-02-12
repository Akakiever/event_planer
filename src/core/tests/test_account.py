import pytest
from django.urls import reverse
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
class TestRegistrationAPI:
    @pytest.mark.parametrize(
        'data',
        [
            {
                'username': 'user1',
                'email': 'user1@example.com',
                'password': 'qd1_dsa@As',
                'first_name': 'User',
                'last_name': 'One',
            },
            {
                'username': 'user1',
                'email': 'user1@example.com',
                'password': 'qd1_dsa@As',
            },
        ]
    )
    def test_success(self, data, api_client):
        url = reverse('api-v1:account-register')
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert 'token' in response.json()
        user = User.objects.get(username=data['username'])
        assert Token.objects.filter(user=user).exists()

    def test_invalid_password(self, api_client):
        url = reverse('api-v1:account-register')
        data = {
            'username': 'user1',
            'email': 'user1@example.com',
            'password': '123',
            'first_name': 'User',
            'last_name': 'One',
        }
        response = api_client.post(url, data)
        assert response.status_code == 400
        assert 'password' in response.json()

    @pytest.mark.parametrize(
        ('data', 'repeated_param'),
        [
            pytest.param({
                    'username': 'user2',
                    'email': 'user1@example.com',
                    'password': 'qd1_dsa@As',
                },
                'email'
            ),
            pytest.param({
                    'username': 'user1',
                    'email': 'user2@example.com',
                    'password': 'qd1_dsa@As',
                },
                'username'
            )
        ]
    )
    def test_user_taken(self, data, repeated_param, api_client, user):
        url = reverse('api-v1:account-register')
        response = api_client.post(url, data)
        assert response.status_code == 400
        assert repeated_param in response.json()


@pytest.mark.django_db
class TestLoginAPI:
    def test_success(self, api_client, user):
        url = reverse('api-v1:account-login')
        data = {
            'username': 'user1',
            'password': 'qd1_dsa@As',
        }
        response = api_client.post(url, data)
        assert response.status_code == 200
        assert 'token' in response.json()

    @pytest.mark.parametrize(
        'data',
        [
            {
                'username': 'user2',
                'password': 'qd1_dsa@As',
            },
            {
                'username': 'user1',
                'password': 'qd1_dsa@Aa',
            }
        ]
    )
    def test_login_invalid_username(self, data, api_client, user):
        url = reverse('api-v1:account-login')
        data = {
            'username': 'user2',
            'password': 'qd1_dsa@As',
        }
        response = api_client.post(url, data)
        assert response.status_code == 400
        assert 'non_field_errors' in response.json()


@pytest.mark.django_db
class TestLogoutAPI:
    def test_success(self, user, api_user_client):
        url = reverse('api-v1:account-logout')
        assert Token.objects.filter(user=user).exists()
        response = api_user_client.post(url)
        assert response.status_code == 204
        assert not Token.objects.filter(user=user).exists()
