# Generated by Django 4.2.2 on 2023-11-24 00:03

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0006_homepage_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='intro',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='thank_you_text',
            field=wagtail.fields.RichTextField(blank=True),
        ),
    ]
