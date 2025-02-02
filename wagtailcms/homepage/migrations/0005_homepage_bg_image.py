# Generated by Django 4.2.2 on 2023-11-22 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('homepage', '0004_remove_homepage_bg_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='bg_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
