# Generated by Django 4.0.10 on 2024-01-23 15:09

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtailcms.customblocks.text_blocks
import wagtailiconchooser.blocks
import wagtailstreamforms.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0089_log_entry_data_json_null_to_object'),
        ('wagtailcms', '0013_themesettings_color_themesettings_color2'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.StreamField([('form', wagtail.blocks.StructBlock([('form', wagtailstreamforms.blocks.FormChooserBlock()), ('form_action', wagtail.blocks.CharBlock(help_text='The form post action. "" or "." for the current page or a url', required=False)), ('form_reference', wagtailstreamforms.blocks.InfoBlock(help_text='This form will be given a unique reference once saved', required=False))])), ('ParagraphBlock_', wagtail.blocks.StructBlock([('paragraph', wagtail.blocks.TextBlock()), ('attribute_name', wagtail.blocks.CharBlock(blank=True, label='e.g. Mary Berry', required=False)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('HeadingBlock_', wagtail.blocks.StructBlock([('heading_text', wagtail.blocks.CharBlock(form_classname='title', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('ButtonBlock_', wagtail.blocks.StructBlock([('button_text', wagtail.blocks.CharBlock(label='Button Text', max_length=50, required=True)), ('button_link', wagtail.blocks.URLBlock(label='Button Link', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('TextWithHeading_', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(form_classname='title', required=True)), ('paragraph', wagtail.blocks.TextBlock(label='Paragraph', max_length=500, required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('RichTextEditorBlock_', wagtailcms.customblocks.text_blocks.RichTextEditorBlock()), ('left_image_section_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Image')), ('heading', wagtail.blocks.CharBlock(label='Heading', max_length=100, required=True)), ('paragraph', wagtail.blocks.TextBlock(label='Paragraph', max_length=500, required=True)), ('button_text', wagtail.blocks.CharBlock(label='Button Text', max_length=50, required=True)), ('button_link', wagtail.blocks.URLBlock(label='Button Link', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('right_image_section_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Image')), ('heading', wagtail.blocks.CharBlock(label='Heading', max_length=100, required=True)), ('paragraph', wagtail.blocks.TextBlock(label='Paragraph', max_length=500, required=True)), ('button_text', wagtail.blocks.CharBlock(label='Button Text', max_length=50, required=True)), ('button_link', wagtail.blocks.URLBlock(label='Button Link', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('circle_left_image_section_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Image')), ('heading', wagtail.blocks.CharBlock(label='Heading', max_length=100, required=True)), ('paragraph', wagtail.blocks.TextBlock(label='Paragraph', max_length=500, required=True)), ('button_text', wagtail.blocks.CharBlock(label='Button Text', max_length=50, required=True)), ('button_link', wagtail.blocks.URLBlock(label='Button Link', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('circle_right_image_section_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Image')), ('heading', wagtail.blocks.CharBlock(label='Heading', max_length=100, required=True)), ('paragraph', wagtail.blocks.TextBlock(label='Paragraph', max_length=500, required=True)), ('button_text', wagtail.blocks.CharBlock(label='Button Text', max_length=50, required=True)), ('button_link', wagtail.blocks.URLBlock(label='Button Link', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('TwoBoxesBlock_', wagtail.blocks.StructBlock([('heading_1', wagtail.blocks.CharBlock(label='Heading 1', max_length=100, required=True)), ('paragraph_1', wagtail.blocks.TextBlock(label='Paragraph 1', max_length=500, required=True)), ('button_text_1', wagtail.blocks.CharBlock(label='Button Text 1', max_length=50, required=True)), ('button_link_1', wagtail.blocks.URLBlock(label='Button Link 1', required=True)), ('heading_2', wagtail.blocks.CharBlock(label='Heading 2', max_length=90, required=True)), ('paragraph_2', wagtail.blocks.TextBlock(label='Paragraph 2', max_length=500, required=True)), ('button_text_2', wagtail.blocks.CharBlock(label='Button Text 2', max_length=50, required=True)), ('button_link_2', wagtail.blocks.URLBlock(label='Button Link 2', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('ThreeBoxesBlock_', wagtail.blocks.StructBlock([('heading_1', wagtail.blocks.CharBlock(label='Heading 1', max_length=100, required=True)), ('paragraph_1', wagtail.blocks.TextBlock(label='Paragraph 1', max_length=500, required=True)), ('button_text_1', wagtail.blocks.CharBlock(label='Button Text 1', max_length=50, required=True)), ('button_link_1', wagtail.blocks.URLBlock(label='Button Link 1', required=True)), ('heading_2', wagtail.blocks.CharBlock(label='Heading 2', max_length=90, required=True)), ('paragraph_2', wagtail.blocks.TextBlock(label='Paragraph 2', max_length=500, required=True)), ('button_text_2', wagtail.blocks.CharBlock(label='Button Text 2', max_length=50, required=True)), ('button_link_2', wagtail.blocks.URLBlock(label='Button Link 2', required=True)), ('heading_3', wagtail.blocks.CharBlock(label='Heading 3', max_length=90, required=True)), ('paragraph_3', wagtail.blocks.TextBlock(label='Paragraph 3', max_length=500, required=True)), ('button_text_3', wagtail.blocks.CharBlock(label='Button Text 3', max_length=50, required=True)), ('button_link_3', wagtail.blocks.URLBlock(label='Button Link 3', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('FourBoxesBlock_', wagtail.blocks.StructBlock([('heading_1', wagtail.blocks.CharBlock(label='Heading 1', max_length=100, required=True)), ('paragraph_1', wagtail.blocks.TextBlock(label='Paragraph 1', max_length=500, required=True)), ('button_text_1', wagtail.blocks.CharBlock(label='Button Text 1', max_length=50, required=True)), ('button_link_1', wagtail.blocks.URLBlock(label='Button Link 1', required=True)), ('heading_2', wagtail.blocks.CharBlock(label='Heading 2', max_length=90, required=True)), ('paragraph_2', wagtail.blocks.TextBlock(label='Paragraph 2', max_length=500, required=True)), ('button_text_2', wagtail.blocks.CharBlock(label='Button Text 2', max_length=50, required=True)), ('button_link_2', wagtail.blocks.URLBlock(label='Button Link 2', required=True)), ('heading_3', wagtail.blocks.CharBlock(label='Heading 3', max_length=90, required=True)), ('paragraph_3', wagtail.blocks.TextBlock(label='Paragraph 3', max_length=500, required=True)), ('button_text_3', wagtail.blocks.CharBlock(label='Button Text 3', max_length=50, required=True)), ('button_link_3', wagtail.blocks.URLBlock(label='Button Link 3', required=True)), ('heading_4', wagtail.blocks.CharBlock(label='Heading 4', max_length=90, required=True)), ('paragraph_4', wagtail.blocks.TextBlock(label='Paragraph 4', max_length=500, required=True)), ('button_text_4', wagtail.blocks.CharBlock(label='Button Text 4', max_length=50, required=True)), ('button_link_4', wagtail.blocks.URLBlock(label='Button Link 4', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('TwoBoxesBlockwithImage_', wagtail.blocks.StructBlock([('image_1', wagtail.images.blocks.ImageChooserBlock(label='Image 1')), ('heading_1', wagtail.blocks.CharBlock(label='Heading 1', max_length=100, required=True)), ('paragraph_1', wagtail.blocks.TextBlock(label='Paragraph 1', max_length=500, required=True)), ('button_text_1', wagtail.blocks.CharBlock(label='Button Text 1', max_length=50, required=True)), ('button_link_1', wagtail.blocks.URLBlock(label='Button Link 1', required=True)), ('image_2', wagtail.images.blocks.ImageChooserBlock(label='Image 2')), ('heading_2', wagtail.blocks.CharBlock(label='Heading 2', max_length=90, required=True)), ('paragraph_2', wagtail.blocks.TextBlock(label='Paragraph 2', max_length=500, required=True)), ('button_text_2', wagtail.blocks.CharBlock(label='Button Text 2', max_length=50, required=True)), ('button_link_2', wagtail.blocks.URLBlock(label='Button Link 2', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('ThreeBoxesBlockwithImage_', wagtail.blocks.StructBlock([('image_1', wagtail.images.blocks.ImageChooserBlock(label='Image 1')), ('heading_1', wagtail.blocks.CharBlock(label='Heading 1', max_length=100, required=True)), ('paragraph_1', wagtail.blocks.TextBlock(label='Paragraph 1', max_length=500, required=True)), ('button_text_1', wagtail.blocks.CharBlock(label='Button Text 1', max_length=50, required=True)), ('button_link_1', wagtail.blocks.URLBlock(label='Button Link 1', required=True)), ('image_2', wagtail.images.blocks.ImageChooserBlock(label='Image 2')), ('heading_2', wagtail.blocks.CharBlock(label='Heading 2', max_length=90, required=True)), ('paragraph_2', wagtail.blocks.TextBlock(label='Paragraph 2', max_length=500, required=True)), ('button_text_2', wagtail.blocks.CharBlock(label='Button Text 2', max_length=50, required=True)), ('button_link_2', wagtail.blocks.URLBlock(label='Button Link 2', required=True)), ('image_3', wagtail.images.blocks.ImageChooserBlock(label='Image 3')), ('heading_3', wagtail.blocks.CharBlock(label='Heading 3', max_length=90, required=True)), ('paragraph_3', wagtail.blocks.TextBlock(label='Paragraph 3', max_length=500, required=True)), ('button_text_3', wagtail.blocks.CharBlock(label='Button Text 3', max_length=50, required=True)), ('button_link_3', wagtail.blocks.URLBlock(label='Button Link 3', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('FourBoxesBlockwithImage_', wagtail.blocks.StructBlock([('image_1', wagtail.images.blocks.ImageChooserBlock(label='Image 1')), ('heading_1', wagtail.blocks.CharBlock(label='Heading 1', max_length=100, required=True)), ('paragraph_1', wagtail.blocks.TextBlock(label='Paragraph 1', max_length=500, required=True)), ('button_text_1', wagtail.blocks.CharBlock(label='Button Text 1', max_length=50, required=True)), ('button_link_1', wagtail.blocks.URLBlock(label='Button Link 1', required=True)), ('image_2', wagtail.images.blocks.ImageChooserBlock(label='Image 2')), ('heading_2', wagtail.blocks.CharBlock(label='Heading 2', max_length=90, required=True)), ('paragraph_2', wagtail.blocks.TextBlock(label='Paragraph 2', max_length=500, required=True)), ('button_text_2', wagtail.blocks.CharBlock(label='Button Text 2', max_length=50, required=True)), ('button_link_2', wagtail.blocks.URLBlock(label='Button Link 2', required=True)), ('image_3', wagtail.images.blocks.ImageChooserBlock(label='Image 3')), ('heading_3', wagtail.blocks.CharBlock(label='Heading 3', max_length=90, required=True)), ('paragraph_3', wagtail.blocks.TextBlock(label='Paragraph 3', max_length=500, required=True)), ('button_text_3', wagtail.blocks.CharBlock(label='Button Text 3', max_length=50, required=True)), ('button_link_3', wagtail.blocks.URLBlock(label='Button Link 3', required=True)), ('image_4', wagtail.images.blocks.ImageChooserBlock(label='Image 4')), ('heading_4', wagtail.blocks.CharBlock(label='Heading 4', max_length=90, required=True)), ('paragraph_4', wagtail.blocks.TextBlock(label='Paragraph 4', max_length=500, required=True)), ('button_text_4', wagtail.blocks.CharBlock(label='Button Text 4', max_length=50, required=True)), ('button_link_4', wagtail.blocks.URLBlock(label='Button Link 4', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('TwoBoxesBlockwithIcon_', wagtail.blocks.StructBlock([('Icon_1', wagtailiconchooser.blocks.IconChooserBlock(label='Icon 1')), ('heading_1', wagtail.blocks.CharBlock(label='Heading 1', max_length=100, required=True)), ('paragraph_1', wagtail.blocks.TextBlock(label='Paragraph 1', max_length=500, required=True)), ('button_text_1', wagtail.blocks.CharBlock(label='Button Text 1', max_length=50, required=True)), ('button_link_1', wagtail.blocks.URLBlock(label='Button Link 1', required=True)), ('Icon_2', wagtailiconchooser.blocks.IconChooserBlock(label='Icon 2')), ('heading_2', wagtail.blocks.CharBlock(label='Heading 2', max_length=90, required=True)), ('paragraph_2', wagtail.blocks.TextBlock(label='Paragraph 2', max_length=500, required=True)), ('button_text_2', wagtail.blocks.CharBlock(label='Button Text 2', max_length=50, required=True)), ('button_link_2', wagtail.blocks.URLBlock(label='Button Link 2', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('ThreeBoxesBlockwithIcon_', wagtail.blocks.StructBlock([('Icon_1', wagtailiconchooser.blocks.IconChooserBlock(label='Icon 1')), ('heading_1', wagtail.blocks.CharBlock(label='Heading 1', max_length=100, required=True)), ('paragraph_1', wagtail.blocks.TextBlock(label='Paragraph 1', max_length=500, required=True)), ('button_text_1', wagtail.blocks.CharBlock(label='Button Text 1', max_length=50, required=True)), ('button_link_1', wagtail.blocks.URLBlock(label='Button Link 1', required=True)), ('Icon_2', wagtailiconchooser.blocks.IconChooserBlock(label='Icon 2')), ('heading_2', wagtail.blocks.CharBlock(label='Heading 2', max_length=90, required=True)), ('paragraph_2', wagtail.blocks.TextBlock(label='Paragraph 2', max_length=500, required=True)), ('button_text_2', wagtail.blocks.CharBlock(label='Button Text 2', max_length=50, required=True)), ('button_link_2', wagtail.blocks.URLBlock(label='Button Link 2', required=True)), ('Icon_3', wagtailiconchooser.blocks.IconChooserBlock(label='Icon 3')), ('heading_3', wagtail.blocks.CharBlock(label='Heading 3', max_length=90, required=True)), ('paragraph_3', wagtail.blocks.TextBlock(label='Paragraph 3', max_length=500, required=True)), ('button_text_3', wagtail.blocks.CharBlock(label='Button Text 3', max_length=50, required=True)), ('button_link_3', wagtail.blocks.URLBlock(label='Button Link 3', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))]))], blank=True, use_json_field=True, verbose_name='Page Body')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='body',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='page_ptr',
        ),
        migrations.AddField(
            model_name='homepage',
            name='custompage_ptr',
            field=models.OneToOneField(auto_created=True, default=3, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcms.custompage'),
            preserve_default=False,
        ),
    ]
