# Generated by Django 4.2.2 on 2023-09-03 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_schedulemeeting_partner'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedulemeeting',
            name='group',
            field=models.IntegerField(default=-1),
        ),
    ]
