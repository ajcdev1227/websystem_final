from django.db import models

DAYS_OF_WEEK = (
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
)


class Timezone(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)
    abbreviation = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Availability(models.Model):
    """
    A block of weekly availability for a profile.
    Each block has a start and end date. This date range determine what dates the block applies to.
    The only exceptions is a block whose start and end dates are null.
    That block is the fallback for any date or range of dates that does not have a specific availability block that applies to it.

    To determine the availability of a given date, the availability block with the most narrow start and end date that the date falls within (inclusive) must be selected.
    If the date does not fall within any specific availability blocks, the block with null start and end dates will be used as a fallback.
    If no default is configured, it is assumed that no days are available.

    You do not need to make a query for each date in a range to get availability for the entire range,
    but if you do query for a range, you need to make sure to fetch all availabilities whose ranges share any of the same dates with
    your range (plus the default availability block whose start and end dates are null).

    In a scenario where you have queried for a range of dates, you need to do sorting for each date in the range locally.
    Doing the sorting locally is much faster than making a query for each date in the range. However, in a single-date query,
    you only need to do one query, and you have the ability to return the exact availability block without sorting locally.

    Note that "locally" in this context refers to running something in your application code rather than in the database.

    Example:
        Suppose there are 4 availability blocks:
        A: null - null
        B: 2024/02/01 - 2024/02/29
        C: 2024/02/11 - 2024/02/17
        D: 2024/02/18 - 2024/02/20

        If availability for 2024/02/13 is requested, block C will be chosen.
        Its range is not the most narrow out of all blocks, but its range is the narrowest out of blocks that 2024/02/13 falls within.

        If availability for 2024/02/05 is requested, block B will be chosen.
        While its range is not the most narrow within the same month, no other more narrow ranges in that month contain 2024/02/05.

        If availability for 2024/03/15 is requested, block A will be chosen.
        There are no blocks that contain 2024/03/15, so the block with a null range will be used as a default.

        If availability for 2024/02/18 is requested, block D will be chosen.
        Block D is the narrowest block, and 2024/02/18 falls within it.
    """

    profile = models.ForeignKey(
        "virtual_calendar.CalendarProfile", on_delete=models.CASCADE
    )

    start_date = models.DateField(
        null=True,
        verbose_name="Start Date",
        help_text="The date at which this availability block starts. A null value indicates that it is the default "
        "availability of the profile.",
    )

    end_date = models.DateField(
        null=True,
        verbose_name="End Date",
        help_text="The date at which this availability block ends. A null value indicates that it is the default "
        "availability of the profile.",
    )

    monday = models.BooleanField(default=True)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=True)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "start_date", "end_date"],
                name="unique date range",
            )
        ]


class AvailabilityTimeSlot(models.Model):
    """
    A time slot of available time for a weekday within a week availability block.
    These slots of time are not tied to a specific date; instead, they are associated with a day of the week and a specific date range.
    """

    availability = models.ForeignKey(
        Availability,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="availability_time_slot",
    )

    day_of_week = models.PositiveIntegerField(
        null=False, blank=False, choices=DAYS_OF_WEEK
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["availability", "day_of_week", "start_time", "end_time"],
                name="unique time slot",
            )
        ]

    def __str__(self):
        return (
            self.get_day_of_week_display()
            + ": "
            + self.start_time
            + " - "
            + self.end_time
        )
