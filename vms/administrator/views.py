from administrator.forms import ReportForm

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from shift.services import *


@login_required
def report(request):

    user = request.user
    admin = None
    try:
        admin = user.administrator
    except ObjectDoesNotExist:
        pass
    if not admin:
        return render(request, 'vms/no_admin_rights.html')
        
    organization_list = get_organizations_ordered_by_name()
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            organization = form.cleaned_data['organization']
            event_name = form.cleaned_data['event_name']
            job_name = form.cleaned_data['job_name']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            report_list = get_administrator_report(
                first_name,
                last_name,
                organization,
                event_name,
                job_name,
                start_date,
                end_date
                )
            total_hours = calculate_total_report_hours(report_list)
            return render(request, 'administrator/report.html', {'form': form, 'report_list': report_list, 'total_hours': total_hours, 'notification': True, 'organization_list': organization_list, 'selected_organization': organization})
        else:
            return render(request, 'administrator/report.html', {'form': form, 'notification': False, 'organization_list': organization_list})
    else:
        form = ReportForm()
        return render(request, 'administrator/report.html', {'form': form, 'notification': False, 'organization_list': organization_list})


@login_required
def settings(request):

    user = request.user
    admin = None
    try:
        admin = user.administrator
    except ObjectDoesNotExist:
        pass
    if not admin:
        return HttpResponse(status=403)

    return HttpResponseRedirect(reverse('event:list'))
