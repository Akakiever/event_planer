# Generated by Django 5.0.2 on 2024-02-11 16:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('plan_date', models.DateTimeField()),
                ('location', models.CharField(max_length=100)),
                ('attendees', models.ManyToManyField(related_name='events_attends', to=settings.AUTH_USER_MODEL)),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='events_organizer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
