from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import ThemeSettings

class ThemeSettingModelAdmin(ModelAdmin):
    model = ThemeSettings

    menu_label = "Theme Settings"
    menu_icon = "doc-full"
    menu_order = 600

    #list_display = (
        #"title",
  #` )
    #search_fields = ("title", )

    #ordering = ("-last_published_at",)
    #list_per_page = 100

    class Meta:
        verbose_name = "Theme Settings ModelAdmin"

#modeladmin_register(ThemeSettingModelAdmin) # Adds it like ahook # adds this to the sidebar BUT as modeladmin