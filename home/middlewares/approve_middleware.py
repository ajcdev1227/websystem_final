from django.http import HttpResponseRedirect


class ApproveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.approved == 0:
                return HttpResponseRedirect('/pending')
            else:
                return HttpResponseRedirect('/test')

        response = self.get_response(request)
        return response
