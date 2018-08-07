# standard library
from functools import wraps

# Django
from django.shortcuts import render


def volunteer_denied(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            if not hasattr(request.user, 'administrator'):
                return render(request, 'vms/no_admin_rights.html', status=403)
        return func(request, *args, **kwargs)

    return wrapper


# account can only be created if both passwords match
def match_password(password1, password2):
    return password1 == password2

