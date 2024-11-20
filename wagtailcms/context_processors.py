from .models import ThemeSettings


def theme(request):
    # theme = ThemeSetting.objects.first().selected_theme
    theme_instance = ThemeSettings.objects.first()
    selected_theme = theme_instance.selected_theme if theme_instance else 'default'
    headline_font  = theme_instance.headline_font if theme_instance else 'inherit'
    headline_size = theme_instance.headline_size if theme_instance else 'inherit'
    paragraph_font = theme_instance.paragraph_font if theme_instance else 'inherit'
    paragraph_size = theme_instance.paragraph_size if theme_instance else 'inherit'
    color = theme_instance.color if theme_instance else '#00000'
    color2 = theme_instance.color2 if theme_instance else '#00000'
    # Tagline = theme_instance.tagline if theme_instance else None
    # Description = theme_instance.description if theme_instance else None
    # Button_text = theme_instance.button_text if theme_instance else None
    # Background_image = theme_instance.background_image if theme_instance else None

    return {
        'selected_theme': selected_theme,
        'headline_font': headline_font,  # 'Tagline' : Tagline,
        'headline_size': headline_size,  # 'Description' : Description,
        'paragraph_font': paragraph_font,  # 'Button_text' : Button_text,
        'paragraph_size': paragraph_size,  # 'Background_image': Background_image
        'color': color,
        'color2': color2
    }


# #from .models import AdminLogo
#
#
# def admin_logo(request):
#     hostname = request.get_host()
#
#     if not (
#         'admin.localhost:8000' == hostname
#         or 'auth' == hostname
#         or 'auth' == hostname
#     ):
#         try:
#             logo = AdminLogo.objects.first()
#             return {'branding': logo}
#         except:
#             return {'branding': {'logo': {'url': '/media/admin_logos/wagtail.svg'}}}
#     return {'branding': ''}

# add other context proceesses