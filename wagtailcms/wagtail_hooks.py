from django.shortcuts import render, redirect
from django.templatetags.static import static
from django.urls import path, reverse
from django.utils.html import format_html

from wagtail import hooks
from wagtail.admin.menu import MenuItem
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler,
)
from .models import ThemeSettings

@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">', static("css/theme1/style.css")
    )


@hooks.register("insert_global_admin_js")
def global_admin_js():
    return format_html('<script src="{}"></script>', static("/js/admin_slug.js"))


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ["icons/primary_color.svg"]


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ["icons/secondary_color.svg"]


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ["icons/tertiary_color.svg"]


@hooks.register("register_rich_text_features")
def register_primary_color_feature(features):
    feature_name = "primary-color"
    type_ = "Primary Color"
    tag = "span"

    primary_control = {
        "type": type_,
        "icon": "primary-color",
        "description": "Primary Color",
        "style": {
            "color": "var(--primary-color)",
        },
    }

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.InlineStyleFeature(primary_control),
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {type_: {"element": tag, "props": {"class": "text-primary"}}}
        },
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)

    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_secondary_color_feature(features):
    secondary_feature = "secondary-color"
    secondary_type = "Secondary Color"
    tag = "span"

    secondary_control = {
        "type": secondary_type,
        "icon": "secondary-color",
        "description": "Secondary Color",
        "style": {
            "color": "var(--secondary-color)",
        },
    }

    features.register_editor_plugin(
        "draftail",
        secondary_feature,
        draftail_features.InlineStyleFeature(secondary_control),
    )

    secondary_db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(secondary_type)},
        "to_database_format": {
            "style_map": {
                secondary_type: {"element": tag, "props": {"class": "text-secondary"}}
            }
        },
    }

    features.register_converter_rule(
        "contentstate", secondary_feature, secondary_db_conversion
    )

    features.default_features.append(secondary_feature)


@hooks.register("register_rich_text_features")
def register_tertiary_color_feature(features):
    tertiary_feature = "tertiary-color"
    tertiary_type = "Tertiary Color"
    tag = "span"

    tertiary_control = {
        "type": tertiary_type,
        "icon": "tertiary-color",
        "description": "Tertiary Color",
        "style": {
            "color": "var(--tertiary-color)",
        },
    }

    features.register_editor_plugin(
        "draftail",
        tertiary_feature,
        draftail_features.InlineStyleFeature(tertiary_control),
    )

    tertiary_db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(tertiary_type)},
        "to_database_format": {
            "style_map": {
                tertiary_type: {"element": tag, "props": {"class": "text-tertiary"}}
            }
        },
    }

    features.register_converter_rule(
        "contentstate", tertiary_feature, tertiary_db_conversion
    )

    features.default_features.append(tertiary_feature)


# @hooks.register('register_admin_urls')
# def register_change_admin_logo_url():
#     return [
#         path('change-logo/', change_admin_logo, name="change_logo"),
#     ]

# @hooks.register('register_admin_menu_item')
# def register_change_admin_logo_menu():
#     return MenuItem('Logo Edit', reverse('change_logo'), icon_name='image', order=10000)


# this is changes the look of wagtail admin
# @hooks.register('insert_global_admin_css')
# def global_admin_css():
#     """
#         @media (prefers-color-scheme: dark) {
#             .w-theme-system .w-combobox {
#                 background-color: var(--w-color-surface-tooltip);
#             }
#         }
#
#         /* Override styles outside the media query */
#         .w-theme-system .w-combobox {
#             background-color: white/* Your custom background color for light mode */;
#         }
#
#         /* Additional styles for dark mode if needed */
#         @media (prefers-color-scheme: dark) {
#             .w-theme-system .w-combobox {
#                 /* Additional styles for dark mode */
#             }
#         }
#     """
    # return """

# <style>
#     .tippy-box{
#       position: fixed;
#       transform: translate(-50%, -50%);
#       display: flex;
#       justify-content: center;
#       align-items: center;
#       background-color: #f0f0f0;
#     }
#
#
#     .w-combobox {
#       position: fixed; /* or use 'absolute' depending on your layout needs */
#       top: 0;
#       left: 0;
#       transform: translate(0%, cal(100vh-50%));
#       background-color: #fff;
#       padding: 20px;
#       border-radius: 8px;
#       box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
#       z-index: 5;
#       min-height: 80vh;
#       width: min(1500px, 220vw);
#     }
#
#     .w-combobox__menu {
#       overflow-y: auto; /* Enable vertical scrolling if menu exceeds max height */
#       min-height: 80vh; /* Set a max height for the dropdown menu if needed */
#     }
#
#     .w-combobox__option {
#         width: min(700px, 160vw);
#         font-size: 100%;
#         padding : 20px;
#     }
# </style>
# """


def theme_settings_view(request):
    theme_setting = ThemeSettings.objects.first()

    if request.method == 'POST':
        # Handle form submission
        if theme_setting:
            theme_setting_form = theme_setting.get_form()(request.POST, instance=theme_setting)
        else:
            # Create a new instance if it doesn't exist
            theme_setting = ThemeSettings()
            theme_setting_form = theme_setting.get_form()(request.POST)

        if theme_setting_form.is_valid():
            theme_setting_form.save()

        return redirect('theme_setting')  # Redirect to the same page after saving

    else:
        # Display form
        if theme_setting:
            theme_setting_form = theme_setting.get_form()(instance=theme_setting)
        else:
            # Create a new instance if it doesn't exist
            theme_setting = ThemeSettings()
            theme_setting_form = theme_setting.get_form()

    return render(request, 'wagtailsettings/settings/edit.html', {
        'theme_setting_form': theme_setting_form,
    })


@hooks.register("register_admin_menu_item")
def register_theme_menu_item():
    return MenuItem(
        "Site Theme Settings",
        reverse("theme_setting"),  # Replace with the actual URL name
        icon_name="folder-open-inverse",
        order=1000,
        classnames="fill-purple",
    )


@hooks.register('register_admin_urls')
def register_theme_admin_urls():
    return [
        path('settings/theme/', theme_settings_view, name='theme_setting'),
    ]
