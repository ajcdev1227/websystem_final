# Generated by Django 4.0.10 on 2024-03-28 21:19

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcms', '0041_eventpage_register_form'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='intro_description',
            field=wagtail.fields.RichTextField(blank=True, null=True),
        ),
    ]
