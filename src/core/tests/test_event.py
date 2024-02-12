from datetime import timedelta
from unittest.mock import patch
from urllib import parse

import pytest
from django.urls import reverse
from django.utils import timezone

from core.models import Event


@pytest.mark.django_db
class TestGetListEvents:
    def test_success(self, api_user_client, simple_event):
        url = reverse('api-v1:event-list')
        response = api_user_client.get(url)

        assert response.status_code == 200
        response_json = response.json()
        assert response_json[0]['id'] == simple_event.id
        assert 'attendees' in response_json[0]
        assert 'title' in response_json[0]
        assert 'description' in response_json[0]
        assert 'plan_date' in response_json[0]
        assert 'location' in response_json[0]
        assert 'organizer' in response_json[0]

    def test_unauthenticated(self, api_client):
        url = reverse('api-v1:event-list')
        response = api_client.get(url)
        assert response.status_code == 401

    def test_different_user(self, api_user2_client, simple_event):
        url = reverse('api-v1:event-list')
        response = api_user2_client.get(url)

        assert response.status_code == 200
        response_json = response.json()
        assert response_json[0]['id'] == simple_event.id
        assert 'attendees' in response_json[0]
        assert 'title' in response_json[0]
        assert 'description' in response_json[0]
        assert 'plan_date' in response_json[0]
        assert 'location' in response_json[0]
        assert 'organizer' in response_json[0]


@pytest.mark.django_db
class TestGetDetailEvents:
    def test_success(self, api_user_client, simple_event):
        url = reverse('api-v1:event-detail', kwargs={'pk': simple_event.id})
        response = api_user_client.get(url)

        assert response.status_code == 200
        response_json = response.json()
        assert response_json['id'] == simple_event.id
        assert 'attendees' in response_json
        assert 'title' in response_json
        assert 'description' in response_json
        assert 'plan_date' in response_json
        assert 'location' in response_json
        assert 'organizer' in response_json

    def test_unauthenticated(self, api_client, simple_event):
        url = reverse('api-v1:event-detail', kwargs={'pk': simple_event.id})
        response = api_client.get(url)
        assert response.status_code == 401

    def test_different_user(self, api_user2_client, simple_event):
        url = reverse('api-v1:event-detail', kwargs={'pk': simple_event.id})
        response = api_user2_client.get(url)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['id'] == simple_event.id
        assert 'attendees' in response_json
        assert 'title' in response_json
        assert 'description' in response_json
        assert 'plan_date' in response_json
        assert 'location' in response_json
        assert 'organizer' in response_json

    @pytest.mark.parametrize(
        'search_string',
        [
            'Title',
            'Description',
            'Location',
        ]
    )
    def test_search(self, search_string, api_user_client, simple_event, simple_event2):
        url = reverse('api-v1:event-list')
        query = parse.urlencode({'search': search_string})
        url = f'{url}?{query}'
        response = api_user_client.get(url)
        assert response.status_code == 200
        response_json = response.json()
        assert len(response_json) == 1
        assert response_json[0]['id'] == simple_event.id

    def test_date_filter_lte(self, api_user_client, simple_event, simple_event2):
        url = reverse('api-v1:event-list')
        time_filter = timezone.now()
        query = parse.urlencode({'plan_date__lte': time_filter.isoformat()})
        url = f'{url}?{query}'

        simple_event.plan_date = timezone.now() - timedelta(days=1)
        simple_event.save()

        simple_event2.plan_date = timezone.now() + timedelta(days=1)
        simple_event2.save()

        response = api_user_client.get(url)
        assert response.status_code == 200
        response_json = response.json()
        assert len(response_json) == 1
        assert response_json[0]['id'] == simple_event.id

    def test_date_filter_gte(self, api_user_client, simple_event, simple_event2):
        url = reverse('api-v1:event-list')
        time_filter = timezone.now()
        query = parse.urlencode({'plan_date__gte': time_filter.isoformat()})
        url = f'{url}?{query}'

        simple_event.plan_date = timezone.now() + timedelta(days=1)
        simple_event.save()

        simple_event2.plan_date = timezone.now() - timedelta(days=1)
        simple_event2.save()

        response = api_user_client.get(url)
        assert response.status_code == 200
        response_json = response.json()
        assert len(response_json) == 1
        assert response_json[0]['id'] == simple_event.id


@pytest.mark.django_db
class TestCreateEvent:
    def test_successful(self, api_user_client, user):
        url = reverse('api-v1:event-list')
        plan_date = timezone.now() + timedelta(days=1)
        data = {
            'title': 'title',
            'description': 'description',
            'plan_date': plan_date.isoformat(),
            'location': 'location'
        }
        response = api_user_client.post(url, data)

        assert response.status_code == 201
        response_json = response.json()
        assert 'id' in response_json
        assert Event.objects.filter(id=response_json['id'], organizer=user).exists()

    def test_unauthenticated(self, api_client):
        url = reverse('api-v1:event-list')
        plan_date = timezone.now() + timedelta(days=1)
        data = {
            'title': 'title',
            'description': 'description',
            'plan_date': plan_date.isoformat(),
            'location': 'location'
        }
        response = api_client.post(url, data)

        assert response.status_code == 401

    def test_invalid_value(self, api_user_client):
        url = reverse('api-v1:event-list')
        plan_date = timezone.now() - timedelta(days=1)
        data = {
            'title': 'title',
            'description': 'description',
            'plan_date': plan_date.isoformat(),
            'location': 'location'
        }
        response = api_user_client.post(url, data)

        assert response.status_code == 400
        assert 'plan_date' in response.json()


@pytest.mark.django_db
class TestUpdateEvent:
    def test_successful(self, api_user_client, simple_event):
        url = reverse('api-v1:event-detail', kwargs={'pk': simple_event.id})
        plan_date = timezone.now() + timedelta(days=1)
        data = {
            'title': 'title',
            'description': 'description',
            'plan_date': plan_date.isoformat(),
            'location': 'location'
        }
        response = api_user_client.put(url, data)
        assert response.status_code == 200

        simple_event.refresh_from_db()

        assert simple_event.title == 'title'
        assert simple_event.description == 'description'
        assert simple_event.location == 'location'
        assert simple_event.plan_date == plan_date

    def test_unauthenticated(self, api_client, simple_event):
        url = reverse('api-v1:event-detail', kwargs={'pk': simple_event.id})
        plan_date = timezone.now() + timedelta(days=1)
        data = {
            'title': 'title',
            'description': 'description',
            'plan_date': plan_date.isoformat(),
            'location': 'location'
        }
        response = api_client.put(url, data)
        assert response.status_code == 401

    def test_unauthorized(self, api_user2_client, simple_event):
        url = reverse('api-v1:event-detail', kwargs={'pk': simple_event.id})
        plan_date = timezone.now() + timedelta(days=1)
        data = {
            'title': 'title',
            'description': 'description',
            'plan_date': plan_date.isoformat(),
            'location': 'location'
        }
        response = api_user2_client.put(url, data)
        assert response.status_code == 403


@pytest.mark.django_db
class TestRegistration:
    def test_success(self, api_user2_client, simple_event, user2):
        url = reverse('api-v1:event-register', kwargs={'pk': simple_event.id})
        with patch('core.tasks.send_event_email_register.apply_async') as send_event_email_mock:
            response = api_user2_client.post(url)
            assert response.status_code == 204
            assert simple_event.attendees.filter(id=user2.id).exists()
            assert send_event_email_mock.call_count == 1
            assert send_event_email_mock.call_args[0][0] == (simple_event.id, user2.id)

    def test_unauthenticated(self, api_client, simple_event):
        url = reverse('api-v1:event-register', kwargs={'pk': simple_event.id})
        response = api_client.post(url)
        assert response.status_code == 401

    def test_organizer(self, api_user_client, simple_event):
        url = reverse('api-v1:event-register', kwargs={'pk': simple_event.id})
        response = api_user_client.post(url)
        assert response.status_code == 403

    def test_repeat(self, api_user2_client, simple_event, user2):
        url = reverse('api-v1:event-register', kwargs={'pk': simple_event.id})

        simple_event.attendees.add(user2)

        response = api_user2_client.post(url)
        assert response.status_code == 400
