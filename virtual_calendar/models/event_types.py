from django.db import models
from django_extensions.db.fields import AutoSlugField


MEETING_TYPES = (
    ('online', 'Online'),
    ('in_person', 'In Person'),
    ('phone_call', 'Phone Call')
)


class EventType(models.Model):
    profile = models.ForeignKey(
        "virtual_calendar.CalendarProfile",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="event_type_profile",
    )

    title = models.CharField(max_length=255, null=False, blank=False)

    url = AutoSlugField(
        populate_from="title",
        editable=True,
        null=False,
    )

    duration = models.PositiveIntegerField(null=False, blank=False)

    meeting_type = models.CharField(max_length=255, choices=MEETING_TYPES, blank=False, null=False)

    description = models.TextField()

    created_ts = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created On',
        help_text='The timestamp when the event type was created',
        null=False,
    )

    def __str__(self):
        return self.title
