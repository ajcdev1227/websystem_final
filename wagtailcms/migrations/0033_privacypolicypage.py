# Generated by Django 4.0.10 on 2024-02-02 22:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('wagtailcore', '0089_log_entry_data_json_null_to_object'),
        ('wagtailcms', '0032_defaultpage_locationspage_servicespage_teampage'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivacyPolicyPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('content', wagtail.fields.RichTextField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('cover_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='privacy_policy_cover_image', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
