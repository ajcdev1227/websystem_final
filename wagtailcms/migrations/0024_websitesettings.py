# Generated by Django 4.0.10 on 2024-01-29 00:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('wagtailcms', '0023_alter_aboutpage_body_alter_eventtypepage_body_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebsiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=50)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('working_hours', models.CharField(blank=True, help_text='For example: 9.00 am - 9.00 pm', max_length=200, null=True)),
                ('facebook', models.URLField(blank=True, null=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('instagram', models.URLField(blank=True, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
                ('youtube', models.URLField(blank=True, null=True)),
                ('github', models.URLField(blank=True, null=True)),
                ('footer_copyright', models.CharField(blank=True, help_text='For example: © Site, All Right Reserved.', max_length=200, null=True)),
                ('footer_developer', models.CharField(blank=True, help_text='For example: Developed by:', max_length=200, null=True)),
                ('footer_logo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('navbar_logo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name': 'Website Settings',
            },
        ),
    ]
