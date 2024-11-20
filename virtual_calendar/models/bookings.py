from django.db import models

STATUSES = (
    ('upcoming', 'Upcoming'),
    ('past', 'Past'),
    ('cancelled', 'Cancelled'),
)


class Booking(models.Model):
    event_type = models.ForeignKey(
        "virtual_calendar.EventType",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="event_type_booking",
    )

    time_slot_start = models.DateTimeField()

    time_slot_end = models.DateTimeField()

    name = models.CharField(max_length=255, null=False, blank=False)

    email_address = models.EmailField(null=False, blank=False)

    additional_note = models.TextField()

    status = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        choices=STATUSES,
        default='upcoming'
    )

    created_ts = models.DateTimeField()

    def __str__(self):
        return str(self.event_type) + " with " + self.name
