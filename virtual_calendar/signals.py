from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import CalendarProfile, Availability, AvailabilityTimeSlot


# @receiver(post_save, sender=CalendarProfile)
# def create_calendar_profile(sender, instance, created, **kwargs):
#     if created:
#         Availability.objects.create(user=instance)
#
#
# @receiver(pre_delete, sender=CalendarProfile)
# def delete_calendar_profile(sender, instance, **kwargs):
#     try:
#         availability_obj = Availability.objects.get(user=instance)
#         AvailabilityTimeSlot.objects.filter(availability=availability_obj).delete()
#         availability_obj.delete()
#     except Exception as e:
#         print("Error while trying to delete Profiles Availability data", e)
