from django.db import models
from django_extensions.db.fields import AutoSlugField

from home.models import CustomUser
from virtual_calendar.models.settings import Timezone


class CalendarProfile(models.Model):
    # ID is explicitly defined here so that ORM and intellisense can give us better options for table joins

    # In Django, adding an id field to a model is optional, as Django automatically creates a primary key
    # field named id for every model unless explicitly overridden.
    id = models.AutoField(
        primary_key=True,
        null=False,
    )

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        null=False,
    )

    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )

    url = AutoSlugField(
        populate_from="title",
        editable=True,
        null=False,
    )

    about = models.TextField(
        max_length=2000,
        blank=True,
        null=False,
        default='',
    )

    timezone = models.ForeignKey(
        Timezone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profile_timezone",
    )

    created_ts = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created On',
        help_text='The timestamp when the profile was created',
        null=False,
    )

    def __str__(self):
        return self.title
