import django_filters
from django.db import models as django_models
from django_filters import rest_framework as filters

from core.models import Event


class EventDateFilter(filters.FilterSet):
    class Meta:
        model = Event
        fields = {
            'plan_date': ('lte', 'gte')
        }

    filter_overrides = {
        django_models.DateTimeField: {
            'filter_class': django_filters.IsoDateTimeFilter
        },
    }
