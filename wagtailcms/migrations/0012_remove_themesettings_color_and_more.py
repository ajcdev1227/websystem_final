# Generated by Django 4.0.10 on 2024-01-23 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcms', '0011_alter_themesettings_color_alter_themesettings_color2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='themesettings',
            name='color',
        ),
        migrations.RemoveField(
            model_name='themesettings',
            name='color2',
        ),
    ]
