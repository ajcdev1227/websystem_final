# Generated by Django 4.2.2 on 2023-11-24 15:15

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0007_homepage_intro_homepage_thank_you_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='sub_intro',
            field=wagtail.fields.RichTextField(blank=True),
        ),
    ]
