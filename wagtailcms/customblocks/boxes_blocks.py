from wagtail.blocks import (
    CharBlock,
    IntegerBlock,
    StructBlock,
    TextBlock,
    URLBlock,
    ListBlock
    
)
from wagtail.images.blocks import ImageChooserBlock
from wagtailiconchooser.blocks import IconChooserBlock


""" Boxes blocks """


class InformationGridBlock(StructBlock):
    entity_type = CharBlock(
        max_length=255,
        required=True,
        label="Section Entity",
        help_text="Ex. Services, Products, Features, etc.",
    )
    title = CharBlock(max_length=255, required=True, label="Section Title")
    description = CharBlock(required=False, label="Section Description")
    cta_text = CharBlock(max_length=255, required=True, label="CTA Text")
    cta_link = URLBlock(required=True, label="CTA Link")

    information_boxes = ListBlock(
        StructBlock(
            [
                ("image", ImageChooserBlock(required=True, label="Box Image")),
                ("title", CharBlock(max_length=255, required=True, label="Box Title")),
                (
                    "description",
                    CharBlock(max_length=255, required=False, label="Box Text"),
                ),
            ],
            icon="duplicate",
        )
    )

    class Meta:
        icon = "grip"
        template = "blocks/boxesblocks/information_grid_block.html"


class FactsBlock(StructBlock):
    facts = ListBlock(
        StructBlock(
            [
                ("icon", IconChooserBlock(label="Fact Icon")),
                ("number", IntegerBlock(required=True, label="Fact Number")),
                ("text", CharBlock(max_length=255, required=True, label="Fact Text")),
            ],
            icon="duplicate",
        )
    )

    class Meta:
        icon = "image"
        template = "blocks/boxesblocks/facts_block.html"


class ProjectsBlock(StructBlock):
    section_title = CharBlock(
        max_length=255,
        required=True,
        label="Section Title",
        default="We Have Completed Latest Projects",
    )
    projects = ListBlock(
        StructBlock(
            [
                ("image", ImageChooserBlock(required=True, label="Project Image")),
                (
                    "title",
                    CharBlock(max_length=255, required=True, label="Project Title"),
                ),
                ("link", URLBlock(required=True, label="Project Link")),
            ],
            icon="duplicate",
        )
    )

    class Meta:
        icon = "folder-open-1"
        template = "blocks/boxesblocks/projects_block.html"


class TeamMembersBlock(StructBlock):
    section_title = CharBlock(
        max_length=255,
        required=True,
        label="Section Title",
        default="Exclusive Team",
    )
    team_members = ListBlock(
        StructBlock(
            [
                (
                    "name",
                    CharBlock(max_length=255, required=True, label="Team Member Name"),
                ),
                ("image", ImageChooserBlock(required=True, label="Team Member Image")),
                ("facebook", URLBlock(required=False, label="Facebook Link")),
                ("twitter", URLBlock(required=False, label="Twitter Link")),
                ("instagram", URLBlock(required=False, label="Instagram Link")),
            ],
            icon="duplicate",
        )
    )

    class Meta:
        icon = "group"
        template = "blocks/boxesblocks/team_members_block.html"


class TestimonialsBlock(StructBlock):
    section_title = CharBlock(
        max_length=255,
        required=True,
        label="Section Title",
        default="What Our Clients Say!",
    )
    testimonials = ListBlock(
        StructBlock(
            [
                ("text", TextBlock(required=True, label="Testimonial Text")),
                ("image", ImageChooserBlock(required=True, label="Author Image")),
                ("author", CharBlock(max_length=255, required=True, label="Author")),
                (
                    "profession",
                    CharBlock(max_length=255, required=True, label="Profession"),
                ),
            ],
            icon="duplicate",
        )
    )

    class Meta:
        icon = "group"
        template = "blocks/boxesblocks/testimonials_block.html"


class AboutUsCardBlock(StructBlock):
    cards = ListBlock(
        StructBlock(
            [
                ("icon", IconChooserBlock(label="Card Icon")),
                ("title", CharBlock(max_length=255, required=True, label="Card Title")),
                ("text", CharBlock(max_length=255, required=True, label="Card Text")),
            ],
            icon="list-ul",
        )
    )

    class Meta:
        icon = "list-ul"
        template = "blocks/boxesblocks/about_us_card_block.html"


class FeaturesBlock(StructBlock):
    section_title = CharBlock(
        max_length=255,
        required=True,
        label="Section Title",
        default="Few Reasons Why People Choosing Us!",
    )
    section_description = CharBlock(
        max_length=255, required=False, label="Section Description"
    )
    button_text = CharBlock(
        max_length=255, required=True, label="Button Text", default="Explore More"
    )
    button_link = URLBlock(required=True, label="Button Link")

    features = ListBlock(
        StructBlock(
            [
                (
                    "title",
                    CharBlock(max_length=255, required=True, label="Feature Title"),
                ),
                ("text", CharBlock(max_length=255, required=True, label="Feature Text")),
                ("link", URLBlock(required=True, label="Feature Link")),
            ],
            icon="duplicate",
            max_num=3,
        )
    )

    class Meta:
        icon = "list-ul"
        template = "blocks/boxesblocks/features_block.html"


class TwoBoxesBlock(StructBlock):
    heading_1 = CharBlock(required=True, max_length=100, label='Heading 1')
    paragraph_1 = TextBlock(required=True, max_length=500, label='Paragraph 1')
    button_text_1 = CharBlock(required=True, max_length=50, label='Button Text 1')
    button_link_1 = URLBlock(required=True, label='Button Link 1')

    heading_2 = CharBlock(required=True, max_length=90, label='Heading 2')
    paragraph_2 = TextBlock(required=True, max_length=500, label='Paragraph 2')
    button_text_2 = CharBlock(required=True, max_length=50, label='Button Text 2')
    button_link_2 = URLBlock(required=True, label='Button Link 2')

    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(required=False, help_text="Right margin in pixels or percentage")
    bottom_margin = CharBlock(required=False, help_text="Bottom margin in pixels or percentage")
    left_margin = CharBlock(required=False, help_text="Left margin in pixels or percentage")

    class Meta:
        icon = 'copy'
        label = 'Two Boxes Block with Text'
        template = "blocks/boxesblocks/twoboxestext.html"


class ThreeBoxesBlock(StructBlock):
    heading_1 = CharBlock(required=True, max_length=100, label='Heading 1')
    paragraph_1 = TextBlock(required=True, max_length=500, label='Paragraph 1')
    button_text_1 = CharBlock(required=True, max_length=50, label='Button Text 1')
    button_link_1 = URLBlock(required=True, label='Button Link 1')

    heading_2 = CharBlock(required=True, max_length=90, label='Heading 2')
    paragraph_2 = TextBlock(required=True, max_length=500, label='Paragraph 2')
    button_text_2 = CharBlock(required=True, max_length=50, label='Button Text 2')
    button_link_2 = URLBlock(required=True, label='Button Link 2')

    heading_3 = CharBlock(required=True, max_length=90, label='Heading 3')
    paragraph_3 = TextBlock(required=True, max_length=500, label='Paragraph 3')
    button_text_3 = CharBlock(required=True, max_length=50, label='Button Text 3')
    button_link_3 = URLBlock(required=True, label='Button Link 3')

    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(required=False, help_text="Right margin in pixels or percentage")
    bottom_margin = CharBlock(required=False, help_text="Bottom margin in pixels or percentage")
    left_margin = CharBlock(required=False, help_text="Left margin in pixels or percentage")

    class Meta:
        icon = 'copy'
        label = 'Three Boxes Block with Text'
        template = "blocks/boxesblocks/threeboxeswithtext.html"


class FourBoxesBlock(StructBlock):
    heading_1 = CharBlock(required=True, max_length=100, label='Heading 1')
    paragraph_1 = TextBlock(required=True, max_length=500, label='Paragraph 1')
    button_text_1 = CharBlock(required=True, max_length=50, label='Button Text 1')
    button_link_1 = URLBlock(required=True, label='Button Link 1')

    heading_2 = CharBlock(required=True, max_length=90, label='Heading 2')
    paragraph_2 = TextBlock(required=True, max_length=500, label='Paragraph 2')
    button_text_2 = CharBlock(required=True, max_length=50, label='Button Text 2')
    button_link_2 = URLBlock(required=True, label='Button Link 2')

    heading_3 = CharBlock(required=True, max_length=90, label='Heading 3')
    paragraph_3 = TextBlock(required=True, max_length=500, label='Paragraph 3')
    button_text_3 = CharBlock(required=True, max_length=50, label='Button Text 3')
    button_link_3 = URLBlock(required=True, label='Button Link 3')

    heading_4 = CharBlock(required=True, max_length=90, label='Heading 4')
    paragraph_4 = TextBlock(required=True, max_length=500, label='Paragraph 4')
    button_text_4 = CharBlock(required=True, max_length=50, label='Button Text 4')
    button_link_4 = URLBlock(required=True, label='Button Link 4')

    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(required=False, help_text="Right margin in pixels or percentage")
    bottom_margin = CharBlock(required=False, help_text="Bottom margin in pixels or percentage")
    left_margin = CharBlock(required=False, help_text="Left margin in pixels or percentage")

    class Meta:
        icon = 'copy'
        label = 'Four Boxes Block with Text'
        template = "blocks/boxesblocks/fourboxeswithtext.html"


class TwoBoxesBlockwithImage(StructBlock):
    image_1 = ImageChooserBlock(label='Image 1')
    heading_1 = CharBlock(required=True, max_length=100, label='Heading 1')
    paragraph_1 = TextBlock(required=True, max_length=500, label='Paragraph 1')
    button_text_1 = CharBlock(required=True, max_length=50, label='Button Text 1')
    button_link_1 = URLBlock(required=True, label='Button Link 1')

    image_2 = ImageChooserBlock(label='Image 2')
    heading_2 = CharBlock(required=True, max_length=90, label='Heading 2')
    paragraph_2 = TextBlock(required=True, max_length=500, label='Paragraph 2')
    button_text_2 = CharBlock(required=True, max_length=50, label='Button Text 2')
    button_link_2 = URLBlock(required=True, label='Button Link 2')

    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(required=False, help_text="Right margin in pixels or percentage")
    bottom_margin = CharBlock(required=False, help_text="Bottom margin in pixels or percentage")
    left_margin = CharBlock(required=False, help_text="Left margin in pixels or percentage")

    class Meta:
        icon = 'copy'
        label = 'Two Boxes Block with Image & Text'
        template = "blocks/boxesblocks/twoboxeswithimageandtext.html"


class ThreeBoxesBlockwithImage(StructBlock):
    image_1 = ImageChooserBlock(label='Image 1')
    heading_1 = CharBlock(required=True, max_length=100, label='Heading 1')
    paragraph_1 = TextBlock(required=True, max_length=500, label='Paragraph 1')
    button_text_1 = CharBlock(required=True, max_length=50, label='Button Text 1')
    button_link_1 = URLBlock(required=True, label='Button Link 1')

    image_2 = ImageChooserBlock(label='Image 2')
    heading_2 = CharBlock(required=True, max_length=90, label='Heading 2')
    paragraph_2 = TextBlock(required=True, max_length=500, label='Paragraph 2')
    button_text_2 = CharBlock(required=True, max_length=50, label='Button Text 2')
    button_link_2 = URLBlock(required=True, label='Button Link 2')

    image_3 = ImageChooserBlock(label='Image 3')
    heading_3 = CharBlock(required=True, max_length=90, label='Heading 3')
    paragraph_3 = TextBlock(required=True, max_length=500, label='Paragraph 3')
    button_text_3 = CharBlock(required=True, max_length=50, label='Button Text 3')
    button_link_3 = URLBlock(required=True, label='Button Link 3')

    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(required=False, help_text="Right margin in pixels or percentage")
    bottom_margin = CharBlock(required=False, help_text="Bottom margin in pixels or percentage")
    left_margin = CharBlock(required=False, help_text="Left margin in pixels or percentage")

    class Meta:
        icon = 'copy'
        label = 'Three Boxes Block with Image & Text'
        template = "blocks/boxesblocks/threeboxeswithimageandtext.html"


class FourBoxesBlockwithImage(StructBlock):
    image_1 = ImageChooserBlock(label='Image 1')
    heading_1 = CharBlock(required=True, max_length=100, label='Heading 1')
    paragraph_1 = TextBlock(required=True, max_length=500, label='Paragraph 1')
    button_text_1 = CharBlock(required=True, max_length=50, label='Button Text 1')
    button_link_1 = URLBlock(required=True, label='Button Link 1')

    image_2 = ImageChooserBlock(label='Image 2')
    heading_2 = CharBlock(required=True, max_length=90, label='Heading 2')
    paragraph_2 = TextBlock(required=True, max_length=500, label='Paragraph 2')
    button_text_2 = CharBlock(required=True, max_length=50, label='Button Text 2')
    button_link_2 = URLBlock(required=True, label='Button Link 2')

    image_3 = ImageChooserBlock(label='Image 3')
    heading_3 = CharBlock(required=True, max_length=90, label='Heading 3')
    paragraph_3 = TextBlock(required=True, max_length=500, label='Paragraph 3')
    button_text_3 = CharBlock(required=True, max_length=50, label='Button Text 3')
    button_link_3 = URLBlock(required=True, label='Button Link 3')

    image_4 = ImageChooserBlock(label='Image 4')
    heading_4 = CharBlock(required=True, max_length=90, label='Heading 4')
    paragraph_4 = TextBlock(required=True, max_length=500, label='Paragraph 4')
    button_text_4 = CharBlock(required=True, max_length=50, label='Button Text 4')
    button_link_4 = URLBlock(required=True, label='Button Link 4')

    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(required=False, help_text="Right margin in pixels or percentage")
    bottom_margin = CharBlock(required=False, help_text="Bottom margin in pixels or percentage")
    left_margin = CharBlock(required=False, help_text="Left margin in pixels or percentage")

    class Meta:
        icon = 'copy'
        label = 'Four Boxes Block with Image & Text'
        template = "blocks/boxesblocks/fourboxeswithimageandtext.html"


class TwoBoxesBlockwithIcon(StructBlock):
    
    Icon_1 = IconChooserBlock(label='Icon 1')
    heading_1 = CharBlock(required=True, max_length=100, label='Heading 1')
    paragraph_1 = TextBlock(required=True, max_length=500, label='Paragraph 1')
    button_text_1 = CharBlock(required=True, max_length=50, label='Button Text 1')
    button_link_1 = URLBlock(required=True, label='Button Link 1')

    Icon_2 = IconChooserBlock(label='Icon 2')
    heading_2 = CharBlock(required=True, max_length=90, label='Heading 2')
    paragraph_2 = TextBlock(required=True, max_length=500, label='Paragraph 2')
    button_text_2 = CharBlock(required=True, max_length=50, label='Button Text 2')
    button_link_2 = URLBlock(required=True, label='Button Link 2')
    
    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(required=False, help_text="Right margin in pixels or percentage")
    bottom_margin = CharBlock(required=False, help_text="Bottom margin in pixels or percentage")
    left_margin = CharBlock(required=False, help_text="Left margin in pixels or percentage")

    class Meta:
        icon = 'copy'
        label = 'Two Boxes Block with Icon & Text'
        template = "blocks/boxesblocks/twoboxeswithIconandtext.html"


class ThreeBoxesBlockwithIcon(StructBlock):
    Icon_1 = IconChooserBlock(label='Icon 1')
    heading_1 = CharBlock(required=True, max_length=100, label='Heading 1')
    paragraph_1 = TextBlock(required=True, max_length=500, label='Paragraph 1')
    button_text_1 = CharBlock(required=True, max_length=50, label='Button Text 1')
    button_link_1 = URLBlock(required=True, label='Button Link 1')

    Icon_2 = IconChooserBlock(label='Icon 2')
    heading_2 = CharBlock(required=True, max_length=90, label='Heading 2')
    paragraph_2 = TextBlock(required=True, max_length=500, label='Paragraph 2')
    button_text_2 = CharBlock(required=True, max_length=50, label='Button Text 2')
    button_link_2 = URLBlock(required=True, label='Button Link 2')

    Icon_3 = IconChooserBlock(label='Icon 3')
    heading_3 = CharBlock(required=True, max_length=90, label='Heading 3')
    paragraph_3 = TextBlock(required=True, max_length=500, label='Paragraph 3')
    button_text_3 = CharBlock(required=True, max_length=50, label='Button Text 3')
    button_link_3 = URLBlock(required=True, label='Button Link 3')

    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(required=False, help_text="Right margin in pixels or percentage")
    bottom_margin = CharBlock(required=False, help_text="Bottom margin in pixels or percentage")
    left_margin = CharBlock(required=False, help_text="Left margin in pixels or percentage")

    class Meta:
        icon = 'copy'
        label = 'Three Boxes Block with Icon & Text'
        template = "blocks/boxesblocks/threeboxeswithIconandtext.html"


class FourBoxesBlockwithIcon(StructBlock):
    Icon_1 = IconChooserBlock(label='Icon 1')
    heading_1 = CharBlock(required=True, max_length=100, label='Heading 1')
    paragraph_1 = TextBlock(required=True, max_length=500, label='Paragraph 1')
    button_text_1 = CharBlock(required=True, max_length=50, label='Button Text 1')
    button_link_1 = URLBlock(required=True, label='Button Link 1')

    Icon_2 = IconChooserBlock(label='Icon 2')
    heading_2 = CharBlock(required=True, max_length=90, label='Heading 2')
    paragraph_2 = TextBlock(required=True, max_length=500, label='Paragraph 2')
    button_text_2 = CharBlock(required=True, max_length=50, label='Button Text 2')
    button_link_2 = URLBlock(required=True, label='Button Link 2')

    Icon_3 = IconChooserBlock(label='Icon 3')
    heading_3 = CharBlock(required=True, max_length=90, label='Heading 3')
    paragraph_3 = TextBlock(required=True, max_length=500, label='Paragraph 3')
    button_text_3 = CharBlock(required=True, max_length=50, label='Button Text 3')
    button_link_3 = URLBlock(required=True, label='Button Link 3')

    Icon_4 = IconChooserBlock(label='Icon 4')
    heading_4 = CharBlock(required=True, max_length=90, label='Heading 4')
    paragraph_4 = TextBlock(required=True, max_length=500, label='Paragraph 4')
    button_text_4 = CharBlock(required=True, max_length=50, label='Button Text 4')
    button_link_4 = URLBlock(required=True, label='Button Link 4')
    
    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(required=False, help_text="Right margin in pixels or percentage")
    bottom_margin = CharBlock(required=False, help_text="Bottom margin in pixels or percentage")
    left_margin = CharBlock(required=False, help_text="Left margin in pixels or percentage")

    class Meta:
        icon = 'copy'
        label = 'Four Boxes Block with Icon & Text'
        template = "blocks/boxesblocks/fourboxeswithIconandtext.html"
