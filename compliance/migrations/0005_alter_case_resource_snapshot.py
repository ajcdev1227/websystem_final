# Generated by Django 4.0.10 on 2024-02-01 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compliance', '0004_case_resource_snapshot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='resource_snapshot',
            field=models.CharField(default='[]', help_text='A snapshot of the resource associated with the case, encoded as a JSON string', max_length=10485760, verbose_name='Resource Snapshot JSON'),
        ),
    ]
