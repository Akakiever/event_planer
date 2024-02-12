from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail

from core.models import Event


@shared_task
def send_event_email_register(event_id, user_id):
    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=user_id)

    topic = f"You have registred to Event \"{event.title}\""
    message = f"You have registred to Event \"{event.title}\"\n" \
              f"{event.description}\n" \
              f"Scheduled time is {event.plan_date.strftime('%Y-%m-%d %H:%M')}"

    send_mail(
        topic,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
