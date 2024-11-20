from django.db import models
from pytz import all_timezones

from home.models import CustomUser


# Create your models here.

class AvailableTime(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='available')
    group = models.IntegerField(default=-1)
    date = models.DateField()
    times = models.TextField()


class DemoMeeting(models.Model):
    showcasher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='meetings', default=None)
    date = models.DateField(null=True)
    time = models.TimeField(null=True, default=None)
    end_time = models.TimeField(null=True, default=None)
    timezone = models.CharField(null=True, max_length=100, choices=[(tz, tz) for tz in all_timezones])
    name = models.CharField(max_length=255, null=True,)
    email = models.CharField(max_length=30, null=True)
    content = models.TextField(null=True,)
    meeting_link = models.TextField(null=True,)
    aware_datetime = models.DateTimeField(null=True, default=None)
    status = models.CharField(max_length=30, default="")
    enable_user_to_join = models.CharField(max_length=10, null=False, default="No")
    lock_meeting = models.CharField(max_length=10, null=False, default="No")
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)


class TenantOption(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='tenant_option')
    tenant_url = models.CharField(max_length=255, blank=True)
    dns_settings = models.CharField(max_length=255, blank=True)
    color_palette = models.CharField(max_length=255, blank=True)
    billing_info = models.CharField(max_length=255, blank=True)
    youtube_acc_link = models.CharField(max_length=255, blank=True)
    twilio_acc = models.CharField(max_length=255, blank=True)
    plan = models.CharField(max_length=255, blank=True)
    rtmp = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
