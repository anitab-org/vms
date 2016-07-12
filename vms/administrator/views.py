from administrator.forms import ReportForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from shift.services import *
from event.services import *
from job.services import *
from django.views.generic import TemplateView
from django.views.generic import ListView
from braces.views import LoginRequiredMixin, AnonymousRequiredMixin
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import View
from administrator.models import Administrator
from django.utils.decorators import method_decorator


class AdministratorLoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        admin = None
        try:
            admin = user.administrator
        except ObjectDoesNotExist:
            pass
        if not admin:
            return render(request, 'vms/no_admin_rights.html')
        else:
            return super(AdministratorLoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class ShowFormView(AdministratorLoginRequiredMixin, FormView):
    """
    Displays the form
    """
    model = Administrator
    form_class = ReportForm
    template_name = "administrator/report.html"



class ShowReportListView(LoginRequiredMixin, AdministratorLoginRequiredMixin, ListView):
    """
    Generate the report using ListView
    """
    template_name = "administrator/report.html"
    organization_list = get_organizations_ordered_by_name()
    event_list = get_events_ordered_by_name()
    job_list = get_jobs_ordered_by_title()

    def post(self, request, *args, **kwargs):
        report_list = get_administrator_report(
            self.request.POST['first_name'],
            self.request.POST['last_name'],
            self.request.POST['organization'],
            self.request.POST['event_name'],
            self.request.POST['job_name'],
            self.request.POST['start_date'],
            self.request.POST['end_date'],
        )
        organization = self.request.POST['organization']
        event_name = self.request.POST['event_name']
        total_hours = calculate_total_report_hours(report_list)
        return render(request, 'administrator/report.html',
                      { 'report_list': report_list, 'total_hours': total_hours, 'notification': True,
                       'organization_list': self.organization_list, 'selected_organization': organization,
                       'event_list': self.event_list, 'selected_event': event_name, 'job_list': self.job_list})

class GenerateReportView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = ShowFormView.as_view()
        return view(request, *args,**kwargs)

    def post(self, request, *args, **kwargs):
        view = ShowReportListView.as_view()
        return view(request, *args, **kwargs)


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
