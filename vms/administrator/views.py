# third-party
from braces.views import LoginRequiredMixin

# Django
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View
from django.views.generic.edit import FormView, UpdateView

# local Django
from administrator.forms import ReportForm, AdministratorForm
from administrator.models import Administrator
from administrator.utils import admin_required, admin_id_check
from event.services import get_events_ordered_by_name
from job.services import get_jobs_ordered_by_title
from shift.services import calculate_total_report_hours, get_administrator_report
from organization.services import get_organizations_ordered_by_name, get_organization_by_id


class AdministratorLoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        admin = hasattr(request.user, 'administrator')
        if not admin:
            return render(request, 'vms/no_admin_rights.html', status=403)
        else:
            return super(AdministratorLoginRequiredMixin, self).dispatch(
                request, *args, **kwargs)


class ShowFormView(AdministratorLoginRequiredMixin, FormView):
    """
    Displays the form
    """
    model = Administrator
    form_class = ReportForm
    template_name = "administrator/report.html"
    event_list = get_events_ordered_by_name()
    job_list = get_jobs_ordered_by_title()
    organization_list = get_organizations_ordered_by_name()

    def get(self, request, *args, **kwargs):
        return render(
            request, 'administrator/report.html', {
                'event_list': self.event_list,
                'organization_list': self.organization_list,
                'job_list': self.job_list
            })


class ShowReportListView(LoginRequiredMixin, AdministratorLoginRequiredMixin,
                         ListView):
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
        return render(
            request, 'administrator/report.html', {
                'report_list': report_list,
                'total_hours': total_hours,
                'notification': True,
                'organization_list': self.organization_list,
                'selected_organization': organization,
                'event_list': self.event_list,
                'selected_event': event_name,
                'job_list': self.job_list
            })


class GenerateReportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = ShowFormView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ShowReportListView.as_view()
        return view(request, *args, **kwargs)


@login_required
@admin_required
def settings(request):
    return HttpResponseRedirect(reverse('event:search'))


'''
    The View to edit Admin Profile
'''


class AdminUpdateView(AdministratorLoginRequiredMixin, UpdateView, FormView):

    @method_decorator(admin_required)
    def dispatch(self, *args, **kwargs):
        return super(AdminUpdateView, self).dispatch(*args, **kwargs)

    form_class = AdministratorForm
    template_name = 'administrator/edit.html'
    organization_list = get_organizations_ordered_by_name()
    success_url = reverse_lazy('administrator:profile')

    def get_context_data(self, **kwargs):
        context = super(AdminUpdateView, self).get_context_data(**kwargs)
        context['organization_list'] = self.organization_list
        return context

    def get_object(self, queryset=None):
        admin_id = self.kwargs['admin_id']
        obj = Administrator.objects.get(pk=admin_id)
        return obj

    def form_valid(self, form):
        admin_id = self.kwargs['admin_id']
        administrator = Administrator.objects.get(pk=admin_id)
        admin_to_edit = form.save(commit=False)

        organization_id = self.request.POST.get('organization_name')
        organization = get_organization_by_id(organization_id)
        if organization:
            admin_to_edit.organization = organization
        else:
            admin_to_edit.organization = None

        # update the volunteer
        admin_to_edit.save()
        return HttpResponseRedirect(
            reverse('administrator:profile', args=[admin_id,]))


'''
  The view to display Admin profile.
  It uses DetailView which is a generic class-based views are designed to display data.
'''


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'administrator/profile.html'

    @method_decorator(admin_required)
    @method_decorator(admin_id_check)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        obj = Administrator.objects.get(id=self.kwargs['admin_id'])
        return obj
