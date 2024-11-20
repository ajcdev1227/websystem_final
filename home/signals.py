# signals.py
from home.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
import uuid


# @receiver(post_save, sender=CustomUser)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         unique_identifier = str(uuid.uuid4())[:8]  # Generate a unique identifier
#         UserProfile.objects.create(user=instance, unique_identifier=unique_identifier)