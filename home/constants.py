import os

COMPLIANCE_STATUS = {
    "pending": "PENDING",
    "approved": "APPROVED",
    "denied": "DENIED"
}

OFFICER_ROLE = 4

ENABLE_WAGTAIL_PUBLISH = os.getenv('ENABLE_WAGTAIL_PUBLISH', '').lower() in ['true', '1', 'yes', 'y']

CRM_ROOT = os.getenv('CRM_ROOT')
CRM_API_KEY = os.getenv('CRM_API_KEY')

NYLAS_CLIENT_ID = os.getenv('NYLAS_CLIENT_ID')
NYLAS_CLIENT_SECRET = os.getenv('NYLAS_CLIENT_SECRET')
APP_NYLAS_REDIRECT_URL = os.getenv('APP_NYLAS_REDIRECT_URL')
NYLAS_API_SERVER = "https://api.nylas.com"
APP_NYLAS_REDIRECT_URL_ADMIN = os.getenv('APP_NYLAS_REDIRECT_URL_ADMIN')
PYAS_CLIENT_ID = os.getenv('PYAS_CLIENT_ID')
PYAS_CLIENT_SECRET = os.getenv('PYAS_CLIENT_SECRET')
PYAS_API_KEY = os.getenv('PYAS_API_KEY')

APP_HOST = os.getenv('APP_HOST')
APP_DOMAIN = os.getenv('APP_DOMAIN')

JITSI_APP_ID = os.getenv('JITSI_APP_ID')
JITSI_API_KEY_ID = os.getenv('JITSI_API_KEY_ID')

LOGIN_TOKEN_SECRET = os.getenv('LOGIN_TOKEN_SECRET')
