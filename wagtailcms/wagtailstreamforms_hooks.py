import json
import requests
from wagtailstreamforms.hooks import register
# from home import CustomUser


# Whatever you create on the form, will be sent to the API
# Whatever the form sends you, you can handle it later on the CRM
@register('process_form_submission')
def send_to_advisor_crm(instance, form):
    endpoint_url = "https://www.advisorcrm.net/scripts/_insert.php"
    payload = {}

    for field, value in form.cleaned_data.items():
        payload.update({field: value})
        print(field)
        #print(field.__dict__)

    payload_str = json.dumps(payload)

    requests.request("POST", endpoint_url, data=payload_str)
