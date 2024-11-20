from wagtail.blocks import (
    CharBlock,
    StructBlock,
    TextBlock,
    URLBlock,
    ListBlock,
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock

""" Image blocks """


class CarouselBlock(StructBlock):
    slide = ListBlock(
        StructBlock(
            [
                ("title", CharBlock(max_length=255, required=True)),
                ("description", CharBlock(max_length=255, required=True)),
                ("cta_text", CharBlock(max_length=255, required=True)),
                ("cta_url", URLBlock(required=True)),
                ("background_image", ImageChooserBlock(required=False)),
            ],
            icon="duplicate",
        )
    )

    class Meta:
        icon = "image"
        template = "blocks/carousel_block.html"


class VideoBlock(StructBlock):
    video_file = DocumentChooserBlock(required=False)
    video_url = URLBlock(required=False)

    class Meta:
        icon = 'media'
        template = "blocks/video_block.html"


class AboutUsBlock(StructBlock):
    image = ImageChooserBlock(required=True)
    title = CharBlock(required=True, max_length=255)
    description = CharBlock(required=True, max_length=255)

    tabs = ListBlock(
        StructBlock(
            [
                ("title", CharBlock(max_length=255, required=True)),
                ("text", CharBlock(max_length=255, required=True)),
            ],
            icon="duplicate",
            max_num=4,
        )
    )

    class Meta:
        icon = "image"
        template = "blocks/about_us_block.html"


class ServicesBlock(StructBlock):
    title = CharBlock(required=True, max_length=255)

    tabs = ListBlock(
        StructBlock(
            [
                ("tab_title", CharBlock(max_length=255, required=True)),
                ("image", ImageChooserBlock(required=True)),
                ("title", CharBlock(max_length=255, required=True)),
                ("text", CharBlock(max_length=255, required=True)),
                (
                    "bullet_points",
                    ListBlock(
                        StructBlock(
                            [
                                ("text", CharBlock(max_length=255, required=True)),
                            ],
                            icon="duplicate",
                            max_num=4,
                        )
                    ),
                ),
                ("cta_text", CharBlock(max_length=255, required=True)),
                ("cta_url", URLBlock(required=True)),
            ],
            icon="duplicate",
            max_num=4,
        )
    )

    class Meta:
        icon = "folder-open-1"
        template = "blocks/services_block.html"


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """

    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(
        required=False, help_text="Right margin in pixels or percentage"
    )
    bottom_margin = CharBlock(
        required=False, help_text="Bottom margin in pixels or percentage"
    )
    left_margin = CharBlock(
        required=False, help_text="Left margin in pixels or percentage"
    )

    class Meta:
        icon = "image"
        template = "blocks/image_block.html"


class LeftImageSectionBlock(StructBlock):
    """Image on the left and text on the right"""

    image = ImageChooserBlock(label="Image")
    heading = CharBlock(required=True, max_length=100, label="Heading")
    paragraph = TextBlock(required=True, max_length=500, label="Paragraph")
    button_text = CharBlock(required=True, max_length=50, label="Button Text")
    button_link = URLBlock(required=True, label="Button Link")

    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(
        required=False, help_text="Right margin in pixels or percentage"
    )
    bottom_margin = CharBlock(
        required=False, help_text="Bottom margin in pixels or percentage"
    )
    left_margin = CharBlock(
        required=False, help_text="Left margin in pixels or percentage"
    )

    class Meta:
        icon = "image"
        label = "Left Image Section Block"
        template = "blocks/imageblocks/left_image_section_block.html"


class CircleLeftImageSectionBlock(StructBlock):
    """Image on the left and text on the right"""

    image = ImageChooserBlock(label="Image")
    heading = CharBlock(required=True, max_length=100, label="Heading")
    paragraph = TextBlock(required=True, max_length=500, label="Paragraph")
    button_text = CharBlock(required=True, max_length=50, label="Button Text")
    button_link = URLBlock(required=True, label="Button Link")

    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(
        required=False, help_text="Right margin in pixels or percentage"
    )
    bottom_margin = CharBlock(
        required=False, help_text="Bottom margin in pixels or percentage"
    )
    left_margin = CharBlock(
        required=False, help_text="Left margin in pixels or percentage"
    )

    class Meta:
        icon = "image"
        label = "Circle Left Image Section Block"
        template = "blocks/imageblocks/circle_left_image_section_block.html"


class RightImageSectionBlock(StructBlock):
    """Image on the right and text on the left"""

    image = ImageChooserBlock(label="Image")
    heading = CharBlock(required=True, max_length=100, label="Heading")
    paragraph = TextBlock(required=True, max_length=500, label="Paragraph")
    button_text = CharBlock(required=True, max_length=50, label="Button Text")
    button_link = URLBlock(required=True, label="Button Link")

    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(
        required=False, help_text="Right margin in pixels or percentage"
    )
    bottom_margin = CharBlock(
        required=False, help_text="Bottom margin in pixels or percentage"
    )
    left_margin = CharBlock(
        required=False, help_text="Left margin in pixels or percentage"
    )

    class Meta:
        icon = "image"
        label = "Right Image Section Block"
        template = "blocks/imageblocks/right_image_section_block.html"


class CircleRightImageSectionBlock(StructBlock):
    """Circle Image on the right and text on the left"""

    image = ImageChooserBlock(label="Image")
    heading = CharBlock(required=True, max_length=100, label="Heading")
    paragraph = TextBlock(required=True, max_length=500, label="Paragraph")
    button_text = CharBlock(required=True, max_length=50, label="Button Text")
    button_link = URLBlock(required=True, label="Button Link")

    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(
        required=False, help_text="Right margin in pixels or percentage"
    )
    bottom_margin = CharBlock(
        required=False, help_text="Bottom margin in pixels or percentage"
    )
    left_margin = CharBlock(
        required=False, help_text="Left margin in pixels or percentage"
    )

    class Meta:
        icon = "image"
        label = "Circle Right Image Section Block"
        template = "blocks/imageblocks/circle_right_image_section_block.html"
