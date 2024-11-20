# Generated by Django 4.0.10 on 2024-01-26 17:39

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
        ('wagtailcms', '0019_alter_eventtypepage_body_alter_homepage_body'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.StreamField([('form', wagtail.blocks.StructBlock([('form', wagtailstreamforms.blocks.FormChooserBlock()), ('form_action', wagtail.blocks.CharBlock(help_text='The form post action. "" or "." for the current page or a url', required=False)), ('form_reference', wagtailstreamforms.blocks.InfoBlock(help_text='This form will be given a unique reference once saved', required=False))])), ('ParagraphBlock_', wagtail.blocks.StructBlock([('paragraph', wagtail.blocks.TextBlock()), ('attribute_name', wagtail.blocks.CharBlock(blank=True, label='e.g. Mary Berry', required=False)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('HeadingBlock_', wagtail.blocks.StructBlock([('heading_text', wagtail.blocks.CharBlock(form_classname='title', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('ButtonBlock_', wagtail.blocks.StructBlock([('button_text', wagtail.blocks.CharBlock(label='Button Text', max_length=50, required=True)), ('button_link', wagtail.blocks.URLBlock(label='Button Link', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('TextWithHeading_', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(form_classname='title', required=True)), ('paragraph', wagtail.blocks.TextBlock(label='Paragraph', max_length=500, required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('RichTextEditorBlock_', wagtailcms.customblocks.text_blocks.RichTextEditorBlock()), ('carousel_block', wagtail.blocks.StructBlock([('slide', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=255, required=True)), ('description', wagtail.blocks.RichTextBlock(required=False)), ('cta_text', wagtail.blocks.CharBlock(max_length=255, required=True)), ('cta_url', wagtail.blocks.URLBlock(required=True)), ('background_image', wagtail.images.blocks.ImageChooserBlock(required=False))], icon='duplicate')))])), ('left_image_section_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Image')), ('heading', wagtail.blocks.CharBlock(label='Heading', max_length=100, required=True)), ('paragraph', wagtail.blocks.TextBlock(label='Paragraph', max_length=500, required=True)), ('button_text', wagtail.blocks.CharBlock(label='Button Text', max_length=50, required=True)), ('button_link', wagtail.blocks.URLBlock(label='Button Link', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('right_image_section_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Image')), ('heading', wagtail.blocks.CharBlock(label='Heading', max_length=100, required=True)), ('paragraph', wagtail.blocks.TextBlock(label='Paragraph', max_length=500, required=True)), ('button_text', wagtail.blocks.CharBlock(label='Button Text', max_length=50, required=True)), ('button_link', wagtail.blocks.URLBlock(label='Button Link', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('circle_left_image_section_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Image')), ('heading', wagtail.blocks.CharBlock(label='Heading', max_length=100, required=True)), ('paragraph', wagtail.blocks.TextBlock(label='Paragraph', max_length=500, required=True)), ('button_text', wagtail.blocks.CharBlock(label='Button Text', max_length=50, required=True)), ('button_link', wagtail.blocks.URLBlock(label='Button Link', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('circle_right_image_section_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Image')), ('heading', wagtail.blocks.CharBlock(label='Heading', max_length=100, required=True)), ('paragraph', wagtail.blocks.TextBlock(label='Paragraph', max_length=500, required=True)), ('button_text', wagtail.blocks.CharBlock(label='Button Text', max_length=50, required=True)), ('button_link', wagtail.blocks.URLBlock(label='Button Link', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('facts', wagtail.blocks.StructBlock([('fact', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('icon', wagtailiconchooser.blocks.IconChooserBlock(label='Fact Icon')), ('number', wagtail.blocks.IntegerBlock(label='Fact Number', required=True)), ('text', wagtail.blocks.CharBlock(label='Fact Text', max_length=255, required=True))], icon='duplicate')))])), ('projects', wagtail.blocks.StructBlock([('section_title', wagtail.blocks.CharBlock(default='We Have Completed Latest Projects', label='Section Title', max_length=255, required=True)), ('projects', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Project Image', required=True)), ('title', wagtail.blocks.CharBlock(label='Project Title', max_length=255, required=True)), ('link', wagtail.blocks.URLBlock(label='Project Link', required=True))], icon='duplicate')))])), ('team_members', wagtail.blocks.StructBlock([('section_title', wagtail.blocks.CharBlock(default='Exclusive Team', label='Section Title', max_length=255, required=True)), ('team_members', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock(label='Team Member Name', max_length=255, required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(label='Team Member Image', required=True)), ('facebook', wagtail.blocks.URLBlock(label='Facebook Link', required=False)), ('twitter', wagtail.blocks.URLBlock(label='Twitter Link', required=False)), ('instagram', wagtail.blocks.URLBlock(label='Instagram Link', required=False))], icon='duplicate')))])), ('testimonials', wagtail.blocks.StructBlock([('section_title', wagtail.blocks.CharBlock(default='What Our Clients Say!', label='Section Title', max_length=255, required=True)), ('testimonials', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('text', wagtail.blocks.TextBlock(label='Testimonial Text', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(label='Author Image', required=True)), ('author', wagtail.blocks.CharBlock(label='Author', max_length=255, required=True)), ('profession', wagtail.blocks.CharBlock(label='Profession', max_length=255, required=True))], icon='duplicate')))])), ('about_us_cards', wagtail.blocks.StructBlock([('cards', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('icon', wagtailiconchooser.blocks.IconChooserBlock(label='Card Icon')), ('title', wagtail.blocks.CharBlock(label='Card Title', max_length=255, required=True)), ('text', wagtail.blocks.CharBlock(label='Card Text', max_length=255, required=True))], icon='list-ul')))])), ('features_blocks', wagtail.blocks.StructBlock([('section_title', wagtail.blocks.CharBlock(default='Few Reasons Why People Choosing Us!', label='Section Title', max_length=255, required=True)), ('section_description', wagtail.blocks.CharBlock(label='Section Description', max_length=255, required=False)), ('button_text', wagtail.blocks.CharBlock(default='Explore More', label='Button Text', max_length=255, required=True)), ('button_link', wagtail.blocks.URLBlock(label='Button Link', required=True)), ('features', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Feature Title', max_length=255, required=True)), ('text', wagtail.blocks.CharBlock(label='Feature Text', max_length=255, required=True)), ('link', wagtail.blocks.URLBlock(label='Feature Link', required=True))], icon='duplicate', max_num=3)))])), ('TwoBoxesBlock_', wagtail.blocks.StructBlock([('heading_1', wagtail.blocks.CharBlock(label='Heading 1', max_length=100, required=True)), ('paragraph_1', wagtail.blocks.TextBlock(label='Paragraph 1', max_length=500, required=True)), ('button_text_1', wagtail.blocks.CharBlock(label='Button Text 1', max_length=50, required=True)), ('button_link_1', wagtail.blocks.URLBlock(label='Button Link 1', required=True)), ('heading_2', wagtail.blocks.CharBlock(label='Heading 2', max_length=90, required=True)), ('paragraph_2', wagtail.blocks.TextBlock(label='Paragraph 2', max_length=500, required=True)), ('button_text_2', wagtail.blocks.CharBlock(label='Button Text 2', max_length=50, required=True)), ('button_link_2', wagtail.blocks.URLBlock(label='Button Link 2', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('ThreeBoxesBlock_', wagtail.blocks.StructBlock([('heading_1', wagtail.blocks.CharBlock(label='Heading 1', max_length=100, required=True)), ('paragraph_1', wagtail.blocks.TextBlock(label='Paragraph 1', max_length=500, required=True)), ('button_text_1', wagtail.blocks.CharBlock(label='Button Text 1', max_length=50, required=True)), ('button_link_1', wagtail.blocks.URLBlock(label='Button Link 1', required=True)), ('heading_2', wagtail.blocks.CharBlock(label='Heading 2', max_length=90, required=True)), ('paragraph_2', wagtail.blocks.TextBlock(label='Paragraph 2', max_length=500, required=True)), ('button_text_2', wagtail.blocks.CharBlock(label='Button Text 2', max_length=50, required=True)), ('button_link_2', wagtail.blocks.URLBlock(label='Button Link 2', required=True)), ('heading_3', wagtail.blocks.CharBlock(label='Heading 3', max_length=90, required=True)), ('paragraph_3', wagtail.blocks.TextBlock(label='Paragraph 3', max_length=500, required=True)), ('button_text_3', wagtail.blocks.CharBlock(label='Button Text 3', max_length=50, required=True)), ('button_link_3', wagtail.blocks.URLBlock(label='Button Link 3', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('FourBoxesBlock_', wagtail.blocks.StructBlock([('heading_1', wagtail.blocks.CharBlock(label='Heading 1', max_length=100, required=True)), ('paragraph_1', wagtail.blocks.TextBlock(label='Paragraph 1', max_length=500, required=True)), ('button_text_1', wagtail.blocks.CharBlock(label='Button Text 1', max_length=50, required=True)), ('button_link_1', wagtail.blocks.URLBlock(label='Button Link 1', required=True)), ('heading_2', wagtail.blocks.CharBlock(label='Heading 2', max_length=90, required=True)), ('paragraph_2', wagtail.blocks.TextBlock(label='Paragraph 2', max_length=500, required=True)), ('button_text_2', wagtail.blocks.CharBlock(label='Button Text 2', max_length=50, required=True)), ('button_link_2', wagtail.blocks.URLBlock(label='Button Link 2', required=True)), ('heading_3', wagtail.blocks.CharBlock(label='Heading 3', max_length=90, required=True)), ('paragraph_3', wagtail.blocks.TextBlock(label='Paragraph 3', max_length=500, required=True)), ('button_text_3', wagtail.blocks.CharBlock(label='Button Text 3', max_length=50, required=True)), ('button_link_3', wagtail.blocks.URLBlock(label='Button Link 3', required=True)), ('heading_4', wagtail.blocks.CharBlock(label='Heading 4', max_length=90, required=True)), ('paragraph_4', wagtail.blocks.TextBlock(label='Paragraph 4', max_length=500, required=True)), ('button_text_4', wagtail.blocks.CharBlock(label='Button Text 4', max_length=50, required=True)), ('button_link_4', wagtail.blocks.URLBlock(label='Button Link 4', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('TwoBoxesBlockwithImage_', wagtail.blocks.StructBlock([('image_1', wagtail.images.blocks.ImageChooserBlock(label='Image 1')), ('heading_1', wagtail.blocks.CharBlock(label='Heading 1', max_length=100, required=True)), ('paragraph_1', wagtail.blocks.TextBlock(label='Paragraph 1', max_length=500, required=True)), ('button_text_1', wagtail.blocks.CharBlock(label='Button Text 1', max_length=50, required=True)), ('button_link_1', wagtail.blocks.URLBlock(label='Button Link 1', required=True)), ('image_2', wagtail.images.blocks.ImageChooserBlock(label='Image 2')), ('heading_2', wagtail.blocks.CharBlock(label='Heading 2', max_length=90, required=True)), ('paragraph_2', wagtail.blocks.TextBlock(label='Paragraph 2', max_length=500, required=True)), ('button_text_2', wagtail.blocks.CharBlock(label='Button Text 2', max_length=50, required=True)), ('button_link_2', wagtail.blocks.URLBlock(label='Button Link 2', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('ThreeBoxesBlockwithImage_', wagtail.blocks.StructBlock([('image_1', wagtail.images.blocks.ImageChooserBlock(label='Image 1')), ('heading_1', wagtail.blocks.CharBlock(label='Heading 1', max_length=100, required=True)), ('paragraph_1', wagtail.blocks.TextBlock(label='Paragraph 1', max_length=500, required=True)), ('button_text_1', wagtail.blocks.CharBlock(label='Button Text 1', max_length=50, required=True)), ('button_link_1', wagtail.blocks.URLBlock(label='Button Link 1', required=True)), ('image_2', wagtail.images.blocks.ImageChooserBlock(label='Image 2')), ('heading_2', wagtail.blocks.CharBlock(label='Heading 2', max_length=90, required=True)), ('paragraph_2', wagtail.blocks.TextBlock(label='Paragraph 2', max_length=500, required=True)), ('button_text_2', wagtail.blocks.CharBlock(label='Button Text 2', max_length=50, required=True)), ('button_link_2', wagtail.blocks.URLBlock(label='Button Link 2', required=True)), ('image_3', wagtail.images.blocks.ImageChooserBlock(label='Image 3')), ('heading_3', wagtail.blocks.CharBlock(label='Heading 3', max_length=90, required=True)), ('paragraph_3', wagtail.blocks.TextBlock(label='Paragraph 3', max_length=500, required=True)), ('button_text_3', wagtail.blocks.CharBlock(label='Button Text 3', max_length=50, required=True)), ('button_link_3', wagtail.blocks.URLBlock(label='Button Link 3', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('FourBoxesBlockwithImage_', wagtail.blocks.StructBlock([('image_1', wagtail.images.blocks.ImageChooserBlock(label='Image 1')), ('heading_1', wagtail.blocks.CharBlock(label='Heading 1', max_length=100, required=True)), ('paragraph_1', wagtail.blocks.TextBlock(label='Paragraph 1', max_length=500, required=True)), ('button_text_1', wagtail.blocks.CharBlock(label='Button Text 1', max_length=50, required=True)), ('button_link_1', wagtail.blocks.URLBlock(label='Button Link 1', required=True)), ('image_2', wagtail.images.blocks.ImageChooserBlock(label='Image 2')), ('heading_2', wagtail.blocks.CharBlock(label='Heading 2', max_length=90, required=True)), ('paragraph_2', wagtail.blocks.TextBlock(label='Paragraph 2', max_length=500, required=True)), ('button_text_2', wagtail.blocks.CharBlock(label='Button Text 2', max_length=50, required=True)), ('button_link_2', wagtail.blocks.URLBlock(label='Button Link 2', required=True)), ('image_3', wagtail.images.blocks.ImageChooserBlock(label='Image 3')), ('heading_3', wagtail.blocks.CharBlock(label='Heading 3', max_length=90, required=True)), ('paragraph_3', wagtail.blocks.TextBlock(label='Paragraph 3', max_length=500, required=True)), ('button_text_3', wagtail.blocks.CharBlock(label='Button Text 3', max_length=50, required=True)), ('button_link_3', wagtail.blocks.URLBlock(label='Button Link 3', required=True)), ('image_4', wagtail.images.blocks.ImageChooserBlock(label='Image 4')), ('heading_4', wagtail.blocks.CharBlock(label='Heading 4', max_length=90, required=True)), ('paragraph_4', wagtail.blocks.TextBlock(label='Paragraph 4', max_length=500, required=True)), ('button_text_4', wagtail.blocks.CharBlock(label='Button Text 4', max_length=50, required=True)), ('button_link_4', wagtail.blocks.URLBlock(label='Button Link 4', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('TwoBoxesBlockwithIcon_', wagtail.blocks.StructBlock([('Icon_1', wagtailiconchooser.blocks.IconChooserBlock(label='Icon 1')), ('heading_1', wagtail.blocks.CharBlock(label='Heading 1', max_length=100, required=True)), ('paragraph_1', wagtail.blocks.TextBlock(label='Paragraph 1', max_length=500, required=True)), ('button_text_1', wagtail.blocks.CharBlock(label='Button Text 1', max_length=50, required=True)), ('button_link_1', wagtail.blocks.URLBlock(label='Button Link 1', required=True)), ('Icon_2', wagtailiconchooser.blocks.IconChooserBlock(label='Icon 2')), ('heading_2', wagtail.blocks.CharBlock(label='Heading 2', max_length=90, required=True)), ('paragraph_2', wagtail.blocks.TextBlock(label='Paragraph 2', max_length=500, required=True)), ('button_text_2', wagtail.blocks.CharBlock(label='Button Text 2', max_length=50, required=True)), ('button_link_2', wagtail.blocks.URLBlock(label='Button Link 2', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))])), ('ThreeBoxesBlockwithIcon_', wagtail.blocks.StructBlock([('Icon_1', wagtailiconchooser.blocks.IconChooserBlock(label='Icon 1')), ('heading_1', wagtail.blocks.CharBlock(label='Heading 1', max_length=100, required=True)), ('paragraph_1', wagtail.blocks.TextBlock(label='Paragraph 1', max_length=500, required=True)), ('button_text_1', wagtail.blocks.CharBlock(label='Button Text 1', max_length=50, required=True)), ('button_link_1', wagtail.blocks.URLBlock(label='Button Link 1', required=True)), ('Icon_2', wagtailiconchooser.blocks.IconChooserBlock(label='Icon 2')), ('heading_2', wagtail.blocks.CharBlock(label='Heading 2', max_length=90, required=True)), ('paragraph_2', wagtail.blocks.TextBlock(label='Paragraph 2', max_length=500, required=True)), ('button_text_2', wagtail.blocks.CharBlock(label='Button Text 2', max_length=50, required=True)), ('button_link_2', wagtail.blocks.URLBlock(label='Button Link 2', required=True)), ('Icon_3', wagtailiconchooser.blocks.IconChooserBlock(label='Icon 3')), ('heading_3', wagtail.blocks.CharBlock(label='Heading 3', max_length=90, required=True)), ('paragraph_3', wagtail.blocks.TextBlock(label='Paragraph 3', max_length=500, required=True)), ('button_text_3', wagtail.blocks.CharBlock(label='Button Text 3', max_length=50, required=True)), ('button_link_3', wagtail.blocks.URLBlock(label='Button Link 3', required=True)), ('top_margin', wagtail.blocks.CharBlock(help_text='Top margin in pixels or percentage', required=False)), ('right_margin', wagtail.blocks.CharBlock(help_text='Right margin in pixels or percentage', required=False)), ('bottom_margin', wagtail.blocks.CharBlock(help_text='Bottom margin in pixels or percentage', required=False)), ('left_margin', wagtail.blocks.CharBlock(help_text='Left margin in pixels or percentage', required=False))]))], blank=True, use_json_field=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
