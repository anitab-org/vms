from functools import wraps
from django.shortcuts import render

def admin_required(func):
    @wraps(func)
    def wrapped_view(request, *args, **kwargs):
        admin = hasattr(request.user, 'administrator')
        if not admin:
            return render(request, 'vms/no_admin_rights.html', status=403)
        return func(request, *args, **kwargs)
    return wrapped_view
