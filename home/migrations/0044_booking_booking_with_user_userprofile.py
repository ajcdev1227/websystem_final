# Generated by Django 4.0.10 on 2024-02-06 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0043_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_with_user',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_identifier', models.CharField(max_length=50, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
