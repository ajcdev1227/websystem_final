# Generated by Django 4.0.10 on 2024-02-18 23:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(help_text='The date at which this availability block starts. A null value indicates that it is the default availability of the profile.', null=True, verbose_name='Start Date')),
                ('end_date', models.DateField(help_text='The date at which this availability block ends. A null value indicates that it is the default availability of the profile.', null=True, verbose_name='End Date')),
                ('monday', models.BooleanField(default=True)),
                ('tuesday', models.BooleanField(default=True)),
                ('wednesday', models.BooleanField(default=True)),
                ('thursday', models.BooleanField(default=True)),
                ('friday', models.BooleanField(default=True)),
                ('saturday', models.BooleanField(default=False)),
                ('sunday', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Timezone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CalendarProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('url', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title')),
                ('about', models.TextField(blank=True, default='', max_length=2000)),
                ('created_ts', models.DateTimeField(auto_now_add=True, help_text='The timestamp when the profile was created', verbose_name='Created On')),
                ('timezone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile_timezone', to='virtual_calendar.timezone')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AvailabilityTimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.PositiveIntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')])),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('availability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availability_time_slot', to='virtual_calendar.availability')),
            ],
        ),
        migrations.AddField(
            model_name='availability',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='virtual_calendar.calendarprofile'),
        ),
        migrations.AddConstraint(
            model_name='availabilitytimeslot',
            constraint=models.UniqueConstraint(fields=('availability', 'day_of_week', 'start_time', 'end_time'), name='unique time slot'),
        ),
        migrations.AddConstraint(
            model_name='availability',
            constraint=models.UniqueConstraint(fields=('profile', 'start_date', 'end_date'), name='unique date range'),
        ),
    ]
