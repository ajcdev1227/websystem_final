# Generated by Django 4.0.10 on 2024-02-29 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcms', '0036_alter_aboutpage_body_alter_contactpage_body_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='websitesettings',
            old_name='address',
            new_name='display_address',
        ),
        migrations.RenameField(
            model_name='websitesettings',
            old_name='email',
            new_name='display_email',
        ),
        migrations.RenameField(
            model_name='websitesettings',
            old_name='phone',
            new_name='display_phone',
        ),
    ]
