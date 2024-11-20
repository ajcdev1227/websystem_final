from django.shortcuts import redirect


def admin_login_required(view_func, login_url=None):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == 1:
                return view_func(request, *args, **kwargs)
        if login_url is None:
            return redirect('/login')
        else:
            return redirect(login_url)
    return wrapper_func