import os
import uuid

from django.contrib.auth.models import AbstractUser
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django_tenants.admin import TenantAdminMixin
from django_tenants.models import TenantMixin, DomainMixin
from django_tenants_url.models import TenantUserMixin
# Create your models here.
from pytz import all_timezones
from core import settings
from django.contrib import admin
from .choices import MEETING_TYPE_CHOICES


class Domain(DomainMixin):
    pass


class Client(TenantMixin):
    tenant_name = models.CharField(max_length=100)
    tenant_uuid = models.UUIDField(default=uuid.uuid4, null=False, blank=False)
    domain_url = models.CharField(max_length=100)
    domain_host = models.CharField(max_length=100)
    paid_until = models.DateField()
    on_trial = models.BooleanField()
    enable_self_managed_compliance = models.BooleanField(
        default=False,
        null=False,
        verbose_name='Enable Self-Managed Compliance',
        help_text='Whether a tenant admin can approve/reject compliance cases without the need for a compliance officer',
    )
    created_on = models.DateField(auto_now_add=True)
    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('tenant_name', 'paid_until')


class Company(models.Model):
    company = models.CharField(max_length=255, blank=True, null=True)


class CustomUser(AbstractUser):
    phonenumber = models.CharField(max_length=255)
    c_members = models.CharField(max_length=255)  # company members
    display_name = models.CharField(max_length=255, blank=True, null=True)
    secondary_email = models.EmailField(blank=True)
    customer_id = models.CharField(max_length=255, blank=False, null=False, editable=True)
    approved = models.IntegerField(default=0)
    role = models.IntegerField(default=0)  # -1: demo user, 0: user, 1: admin, 2: super admin, 3: showcaser, 4: officer
    group = models.IntegerField(default=-1)
    calendar_id = models.CharField(max_length=255, default='')
    nylas_access_token = models.CharField(max_length=255, default='')
    domain_url = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    # personal meeting link to send to crm
    personal_meeting_link = models.CharField(max_length=255, null=True, blank=True)


class TenantUser(TenantUserMixin):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    pass


class Pages(models.Model):
    parent_id = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    page_name = models.CharField(max_length=255, blank=False, null=False)
    url = models.CharField(max_length=255, blank=False, null=False)
    status = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='pages')

    def __str__(self):
        return self.page_name


# DEPRECATED
class Meetings(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_meetings')
    title = models.CharField(max_length=255, null=False, blank=False)
    user_email = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True, default=None)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    created_on = models.DateField(null=False, auto_now_add=True)
    is_hidden = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    meeting_type = models.IntegerField(
        choices=MEETING_TYPE_CHOICES,
        default=1,
    )
    event_link = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f"{self.title} - {self.date} {self.start_time}-{self.end_time}"


class Slug(models.Model):
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=200)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=200, default='')

    class Meta:
        ordering = ['-updated_on']

    def __str__(self):
        return self.filename


class Submission(models.Model):
    """
    Page update submissions
    """

    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID',
    )

    slug = models.TextField(max_length=255, null=False)

    old_version = models.TextField(
        null=False,
        verbose_name='Old Version',
    )
    new_version = models.TextField(
        null=False,
        verbose_name='New Version'
    )

    submitter_note = models.TextField(
        max_length=1024,
        null=True,
        default=None,
        verbose_name='Note From Submitter'
    )

    approval_officer_note = models.TextField(
        max_length=1024,
        null=True,
        default=None,
        verbose_name='Note From Approval Officer'
    )

    approved_ts = models.DateTimeField(
        null=True,
        default=None,
        verbose_name='Date Approved'
    )
    """Will be null if the submission hasn't yet been approved"""

    denied_ts = models.DateTimeField(
        null=True,
        default=None,
        verbose_name='Date Denied'
    )
    """Will be null if the submission hasn't yet been denied"""

    status = models.TextField(
        null=True,
        default=None,
        verbose_name='Status'
    )

    updated_ts = models.DateTimeField(
        null=True,
        default=None,
        verbose_name='Submission Details Updated On'
    )

    created_ts = models.DateTimeField(
        auto_now=True,
        null=False,
        verbose_name='Date Submitted'
    )

    sub_view_old_url = models.TextField(
        max_length=1024,
        null=True,
        default=None,
    )

    sub_view_new_url = models.TextField(
        max_length=1024,
        null=True,
        default=None,
    )

    sub_screenshot_old_url = models.TextField(
        max_length=1024,
        null=True,
        default=None,
    )

    sub_screenshot_new_url = models.TextField(
        max_length=1024,
        null=True,
        default=None,
    )

    draft_file_endpoint = models.TextField(
        max_length=1024,
        null=True,
        default=None,
    )

    checked = models.IntegerField(
        default=0
    )

    submitter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    page = models.ForeignKey(Pages, on_delete=models.CASCADE, related_name="submissions")

    screenshot_dir = os.path.join(settings.MEDIA_ROOT, 'submission-screenshots')

    def get_screenshot_path(self, is_old: bool) -> str:
        filename = str(self.id)
        if is_old:
            filename += '.old'
        else:
            filename += '.new'
        filename += '.png'

        return os.path.join(self.screenshot_dir, filename)

    def get_screenshot_url(self, is_old: bool, request: WSGIRequest) -> str:
        return request.build_absolute_uri('/submission/screenshot/?id=' + str(self.id) + '&old=' + str(int(is_old)))

    def get_view_url(self, is_old: bool, request: WSGIRequest) -> str:
        return request.build_absolute_uri('/submission/view/?id=' + str(self.id) + '&old=' + str(int(is_old)))

    class Meta:
        pass


class ScheduleMeeting(models.Model):
    creator = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='meeting', default=None)
    partner = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='schedule_meeting', default=None, null=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True, default=None)
    end_time = models.TimeField(null=True, default=None)
    timezone = models.CharField(null=True, max_length=100, choices=[(tz, tz) for tz in all_timezones])
    name = models.CharField(max_length=255, null=True, )
    email = models.CharField(max_length=254, null=True)
    content = models.TextField(null=True, )
    meeting_link = models.TextField(null=True, )
    aware_datetime = models.DateTimeField(null=True, default=None)
    status = models.CharField(max_length=30, default="")
    enable_user_to_join = models.CharField(max_length=10, null=False, default="No")
    lock_meeting = models.CharField(max_length=10, null=False, default="No")
    group = models.IntegerField(default=-1)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)


class Article(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='articles')
    title = models.TextField()
    content = models.TextField()
    file = models.CharField(max_length=255, default=None, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    

class EventType(models.Model):
    """
    An event type that outside users can schedule time for
    """

    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID',
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='User',
        help_text='The internal user that the event type applies to or was created by',
    )

    title = models.CharField(
        max_length=64,
        verbose_name='Title',
        help_text='The event title',
    )

    slug = models.CharField(
        max_length=64,
        verbose_name='Slug',
        help_text='The slug, used to construct the full event type URL for booking',
    )

    description = models.CharField(
        max_length=2048,
        verbose_name='Description',
        help_text='The event description',
    )

    duration_minutes = models.IntegerField(
        verbose_name='Duration Minutes',
        help_text='The event type duration in minutes,'
    )

    LOCATION_CHOICES = [('virtual', 'Virtual Meeting'), ('phone', 'Phone Call'), ('in_person', 'In-Person Meeting')]
    location = models.CharField(
        choices=LOCATION_CHOICES,
        verbose_name='Location',
        help_text='The type of location or setting the meeting will take place in',
        max_length=255,
    )

    is_hidden = models.BooleanField(
        default=False,
        verbose_name='Is Hidden?',
        help_text='Whether the event type is hidden from the user\'s public event listing page',
    )

    created_ts = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created On',
        help_text='The event type creation timestamp',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'slug'], name='user_slug_unique_key'),
        ]


class EventBooking(models.Model):
    """
    A booking scheduled by an outside user for an event type
    """

    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID',
    )

    event_type = models.ForeignKey(
        EventType,
        on_delete=models.CASCADE,
        verbose_name='Event Type',
        help_text='The associated event type',
    )

    start_ts = models.DateTimeField(
        verbose_name='Start Timestamp',
        help_text='The timestamp of when the event begins. This includes both date and time.',
    )

    end_ts = models.DateTimeField(
        verbose_name='End Timestamp',
        help_text='The timestamp when the event ends. This includes both date and time.',
    )

    scheduler_name = models.CharField(
        max_length=200,
        verbose_name='Scheduler Name',
        help_text='The name of the person who booked the meeting',
    )
    scheduler_email = models.CharField(
        max_length=254,
        verbose_name='Schedule Email',
        help_text='The email of the person who booked the meeting',
    )

    meeting_id = models.CharField(
        max_length=20,
        null=True,
        verbose_name='Instant Meeting ID',
        help_text='The ID of the associated instant meeting, if any'
    )

    created_ts = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created On',
        help_text='The event booking creation timestamp',
    )
