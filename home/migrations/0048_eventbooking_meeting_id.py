# Generated by Django 4.0.10 on 2024-02-19 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0047_eventtype_eventbooking_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventbooking',
            name='meeting_id',
            field=models.CharField(help_text='The ID of the associated instant meeting, if any', max_length=20, null=True, verbose_name='Instant Meeting ID'),
        ),
    ]
