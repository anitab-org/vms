# standard library
from functools import wraps

# Django
from django.shortcuts import render

from administrator.models import Administrator


def admin_required(func):
    @wraps(func)
    def wrapped_view(request, *args, **kwargs):
        admin = hasattr(request.user, 'administrator')
        if not admin:
            return render(request, 'vms/no_admin_rights.html', status=403)
        return func(request, *args, **kwargs)

    return wrapped_view


def admin_id_check(func):
    @wraps(func)
    def wrapped_view(request, admin_id):
        administrator = getattr(request.user, 'administrator',
                                hasattr(request.user, 'administrator'))
        if administrator is None:
            return render(request, 'vms/no_admin_rights.html', status=403)
        elif not administrator:
            try:
                admin = Administrator.objects.get(id=admin_id)
                if not int(admin.id) == administrator.id:
                    return render(
                        request, 'vms/no_admin_rights.html', status=403)
            except Administrator.DoesNotExist:
                return render(
                    request, 'vms/no_admin_rights.html', status=403)
        return func(request, admin_id=admin_id)

    return wrapped_view
