# Generated by Django 4.2.2 on 2023-08-16 01:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TenantOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_url', models.CharField(blank=True, max_length=255)),
                ('dns_settings', models.CharField(blank=True, max_length=255)),
                ('color_palette', models.CharField(blank=True, max_length=255)),
                ('billing_info', models.CharField(blank=True, max_length=255)),
                ('youtube_acc_link', models.CharField(blank=True, max_length=255)),
                ('twilio_acc', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tenant_option', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
