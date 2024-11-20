from django import forms
from pytz import all_timezones

from .models import Company, CustomUser
from wagtailcms.models import WebsiteSettings


class DateTimeForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'readonly': 'readonly'}))
    available_times = forms.CharField(widget=forms.Textarea(attrs={'readonly': 'readonly', 'hidden': 'hidden'}))
    timezone = forms.ChoiceField(choices=[(tz, tz) for tz in all_timezones], initial='EST', widget=forms.HiddenInput())


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "secondary_email",
            "phonenumber",
            "c_members",
            "domain_url",
        )

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['domain_url'].widget.attrs['readonly'] = True


class WebsiteSettingsForm(forms.ModelForm):
    class Meta:
        model = WebsiteSettings
        fields = (
            "display_email",
            "display_phone",
            "display_address",
            "working_hours",
            "facebook",
            "twitter",
            "instagram",
            "linkedin",
            "youtube",
            "github",
            "footer_copyright",
            "footer_developer",
        )

    def __init__(self, *args, **kwargs):
        super(WebsiteSettingsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
