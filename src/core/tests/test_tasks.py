from unittest.mock import patch

import pytest

from core.tasks import send_event_email_register


@pytest.mark.django_db
class TestEmailEventRegister:
    def test_send(self, user2, simple_event):
        send_event_email_register(simple_event.id, user2.id)
        with patch('core.tasks.send_mail') as send_mail_mock:
            send_event_email_register(simple_event.id, user2.id)
            assert send_mail_mock.call_count == 1
            assert send_mail_mock.call_args[0][3] == [user2.email]
            assert simple_event.title in send_mail_mock.call_args[0][0]
