# standard library
from functools import wraps

# Django
from django.http import Http404
from django.shortcuts import render

# local Django
from volunteer.models import Volunteer


def check_correct_volunteer(func):
    @wraps(func)
    def wrapped_view(request, **kwargs):
        req_volunteer = getattr(request.user, "volunteer",
                                hasattr(request.user, "administrator"))
        volunteer_id = kwargs['volunteer_id']
        if not req_volunteer:
            raise Http404
        elif req_volunteer is not True:
            try:
                volunteer = Volunteer.objects.get(id=volunteer_id)
            except Volunteer.DoesNotExist:
                return render(
                    request, "vms/no_volunteer_rights.html", status=403)
            if volunteer.id == req_volunteer.id:
                return func(request, volunteer_id=volunteer_id)
            else:
                return render(
                    request, "vms/no_volunteer_rights.html", status=403)
        else:
            return render(request, "vms/no_volunteer_rights.html", status=403)

    return wrapped_view


def check_correct_volunteer_shift_sign_up(func):
    @wraps(func)
    def wrapped_view(request, **kwargs):
        req_volunteer = getattr(request.user, "volunteer",
                                hasattr(request.user, "administrator"))
        volunteer_id = kwargs['volunteer_id']
        if req_volunteer is True:
            return func(request, volunteer_id=volunteer_id)
        if not req_volunteer:
            raise Http404
        elif req_volunteer is not True:
            try:
                volunteer = Volunteer.objects.get(id=volunteer_id)
            except Volunteer.DoesNotExist:
                return render(
                    request, "vms/no_volunteer_rights.html", status=403)
            if volunteer.id == req_volunteer.id:
                return func(request, volunteer_id=volunteer_id)
            else:
                return render(
                    request, "vms/no_volunteer_rights.html", status=403)
        else:
            return render(request, "vms/no_volunteer_rights.html", status=403)

    return wrapped_view
