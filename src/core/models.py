from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    plan_date = models.DateTimeField()
    location = models.CharField(max_length=100)
    organizer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='events_organizer')
    attendees = models.ManyToManyField(User, related_name='events_attends')
