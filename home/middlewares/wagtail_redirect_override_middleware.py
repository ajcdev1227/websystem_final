from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from wagtail.contrib.redirects.middleware import RedirectMiddleware

from home.constants import APP_DOMAIN


redirect_exempted_subdomains = ['auth', 'compliance']


class WagtailRedirectOverrideMiddleware:
    """
    This middleware wraps Wagtail's redirect middleware so that it can be overriden for specific domains
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest) -> HttpResponse:
        host = request.get_host()

        for subdomain in redirect_exempted_subdomains:
            if host == f"{subdomain}.{APP_DOMAIN}":
                return self.get_response(request)
        else:
            middleware = RedirectMiddleware(self.get_response)
            return middleware(request)
