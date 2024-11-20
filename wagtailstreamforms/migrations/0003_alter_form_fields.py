# Generated by Django 4.1.8 on 2023-04-14 05:21

from django.db import migrations
import wagtail.blocks
import wagtailstreamforms.streamfield


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailstreamforms', '0002_form_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='fields',
            field=wagtailstreamforms.streamfield.FormFieldsStreamField([('singleline', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('help_text', wagtail.blocks.CharBlock(required=False)), ('required', wagtail.blocks.BooleanBlock(required=False)), ('default_value', wagtail.blocks.CharBlock(required=False))], icon='placeholder', label='Text field (single line)')), ('multiline', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('help_text', wagtail.blocks.CharBlock(required=False)), ('required', wagtail.blocks.BooleanBlock(required=False)), ('default_value', wagtail.blocks.CharBlock(required=False))], icon='placeholder', label='Text field (multi line)')), ('date', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('help_text', wagtail.blocks.CharBlock(required=False)), ('required', wagtail.blocks.BooleanBlock(required=False)), ('default_value', wagtail.blocks.CharBlock(required=False))], icon='date', label='Date field')), ('datetime', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('help_text', wagtail.blocks.CharBlock(required=False)), ('required', wagtail.blocks.BooleanBlock(required=False)), ('default_value', wagtail.blocks.CharBlock(required=False))], icon='time', label='Time field')), ('email', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('help_text', wagtail.blocks.CharBlock(required=False)), ('required', wagtail.blocks.BooleanBlock(required=False)), ('default_value', wagtail.blocks.CharBlock(required=False))], icon='mail', label='Email field')), ('url', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('help_text', wagtail.blocks.CharBlock(required=False)), ('required', wagtail.blocks.BooleanBlock(required=False)), ('default_value', wagtail.blocks.CharBlock(required=False))], icon='link', label='URL field')), ('number', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('help_text', wagtail.blocks.CharBlock(required=False)), ('required', wagtail.blocks.BooleanBlock(required=False)), ('default_value', wagtail.blocks.CharBlock(required=False))], icon='placeholder', label='Number field')), ('dropdown', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('help_text', wagtail.blocks.CharBlock(required=False)), ('required', wagtail.blocks.BooleanBlock(required=False)), ('empty_label', wagtail.blocks.CharBlock(required=False)), ('choices', wagtail.blocks.ListBlock(wagtail.blocks.CharBlock(label='Option')))], icon='arrow-down-big', label='Dropdown field')), ('radio', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('help_text', wagtail.blocks.CharBlock(required=False)), ('required', wagtail.blocks.BooleanBlock(required=False)), ('choices', wagtail.blocks.ListBlock(wagtail.blocks.CharBlock(label='Option')))], icon='radio-empty', label='Radio buttons')), ('checkboxes', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('help_text', wagtail.blocks.CharBlock(required=False)), ('required', wagtail.blocks.BooleanBlock(required=False)), ('choices', wagtail.blocks.ListBlock(wagtail.blocks.CharBlock(label='Option')))], icon='tick-inverse', label='Checkboxes')), ('checkbox', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('help_text', wagtail.blocks.CharBlock(required=False)), ('required', wagtail.blocks.BooleanBlock(required=False))], icon='tick-inverse', label='Checkbox field')), ('hidden', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('help_text', wagtail.blocks.CharBlock(required=False)), ('required', wagtail.blocks.BooleanBlock(required=False)), ('default_value', wagtail.blocks.CharBlock(required=False))], icon='no-view', label='Hidden field')), ('singlefile', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('help_text', wagtail.blocks.CharBlock(required=False)), ('required', wagtail.blocks.BooleanBlock(required=False))], icon='doc-full-inverse', label='File field')), ('multifile', wagtail.blocks.StructBlock([('label', wagtail.blocks.CharBlock()), ('help_text', wagtail.blocks.CharBlock(required=False)), ('required', wagtail.blocks.BooleanBlock(required=False))], icon='doc-full-inverse', label='Files field'))], use_json_field=True, verbose_name='Fields'),
        ),
    ]
