# Generated by Django 4.0.10 on 2024-02-07 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0044_booking_booking_with_user_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Booking',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
