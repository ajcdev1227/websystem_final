# Generated by Django 4.0.10 on 2024-03-05 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcms', '0038_websitesettings_google_analytics_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='websitesettings',
            name='ms_clarity_key',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
