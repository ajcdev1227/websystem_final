# Generated by Django 4.2.2 on 2023-08-28 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_schedulemeeting_enable_user_to_join_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedulemeeting',
            name='lock_meeting',
            field=models.CharField(default='No', max_length=10),
        ),
    ]
