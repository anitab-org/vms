from functools import wraps
from django.shortcuts import render

def volunteer_denied(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            if not hasattr(request.user, 'administrator'):
                return render(request, 'vms/no_admin_rights.html', status=403)
        return func(request, *args, **kwargs)
    return wrapper
    