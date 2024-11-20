from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'home', 'home.urls', name='app'),
    host(r'demo', 'demo.urls', name='demo'),
    host(r'admin', 'adminapp.urls', name='admin'),
    host(r'auth', 'webauth.urls', name='webauth'),

    # add entry for compliance
    host(r'compliance', 'compliance.urls', name='compliance'),

    # Integration API
    host(r'integration-api', 'integration_api.urls', name='integration_api'),
)
