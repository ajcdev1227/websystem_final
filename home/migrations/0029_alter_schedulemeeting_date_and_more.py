# Generated by Django 4.2.2 on 2023-09-03 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_schedulemeeting_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedulemeeting',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='schedulemeeting',
            name='time',
            field=models.TimeField(default=None, null=True),
        ),
    ]
