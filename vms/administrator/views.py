# third-party
from braces.views import LoginRequiredMixin
from cities_light.models import Country, Region, City

# Django
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from easy_pdf.rendering import render_to_pdf
from django.core.mail.message import EmailMessage
from django.core.mail import send_mail

# local Django
from administrator.forms import AdministratorForm
from administrator.models import Administrator
from administrator.utils import admin_required, admin_id_check
from shift.models import Report
from shift.services import generate_report, get_report_by_id
from organization.services import (create_organization,
                                   get_organizations_ordered_by_name,
                                   get_organization_by_id)


class ReportListView(ListView, LoginRequiredMixin):
    """
    Returns list of unconfirmed reports

    Extends ListView which is a generic class-based view to display lists
    """
    template_name = "administrator/report.html"

    def get_queryset(self):
        """
        defines queryset for the view

        :return: pending reports
        """
        reports = Report.objects.filter(confirm_status=0)
        return reports


def reject(request, report_id):
    """
    rejects the pending reports

    :param report_id: The id of pending report
    :return: redirect to list of pending reports
    """
    report = get_report_by_id(report_id)
    report.confirm_status = 2
    report.save()
    volunteer = report.volunteer
    admin = Administrator.objects.get(user=request.user)
    message = render_to_string(
        'administrator/reject_report.html',
        {
            'volunteer': volunteer,
            'admin': admin,
        }
    )
    send_mail(
        "Report Rejected", message,
        "messanger@localhost.com", [volunteer.email]
    )
    return HttpResponseRedirect('/administrator/report')


def approve(request, report_id):
    """
    approves the pending reports

    :param report_id: The id of pending report
    :return: redirect to list of pending reports
    """
    report = get_report_by_id(report_id)
    report.confirm_status = 1
    report.save()
    admin = Administrator.objects.get(user=request.user)
    volunteer_shift_list = report.volunteer_shifts.all()
    report_list = generate_report(volunteer_shift_list)
    volunteer = report.volunteer
    post_pdf = render_to_pdf(
        'administrator/pdf.html',
        {
            'report': report,
            'admin': admin,
            'report_list': report_list,
        },
    )
    message = render_to_string(
        'administrator/confirm_report.html',
        {
            'volunteer': volunteer,
            'admin': admin,
        }
    )
    msg = EmailMessage(
        "Report Approved", message,
        "messanger@localhost.com", [report.volunteer.email]
    )
    msg.attach('file.pdf', post_pdf, 'application/pdf')
    msg.send()
    return HttpResponseRedirect('/administrator/report')


def show_report(request, report_id):
    """
    displays the report

    :param report_id: The id of pending report
    :return: report of the volunteer
    """
    report = get_report_by_id(report_id)
    volunteer_shift_list = report.volunteer_shifts.all()
    report_list = generate_report(volunteer_shift_list)
    total_hours = report.total_hrs
    return render(
        request, 'administrator/view_report.html',
        {
            'report_list': report_list,
            'total_hours': total_hours,
            'report': report,
        }
    )


class AdministratorLoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        admin = hasattr(request.user, 'administrator')
        if not admin:
            return render(request, 'vms/no_admin_rights.html', status=403)
        else:
            return super(
                AdministratorLoginRequiredMixin, self
            ).dispatch(request, *args, **kwargs)


@login_required
@admin_required
def settings(request):
    return HttpResponseRedirect(reverse('event:list'))


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
        admin_id = self.kwargs['admin_id']
        admin = Administrator.objects.get(pk=admin_id)
        country_list = Country.objects.all()
        if admin.country:
            country = admin.country
            state_list = Region.objects.filter(country=country)
            context['state_list'] = state_list
        if admin.state:
            state = admin.state
            city_list = City.objects.filter(region=state)
            context['city_list'] = city_list
        context['organization_list'] = self.organization_list
        context['country_list'] = country_list
        return context

    def get_object(self, queryset=None):
        admin_id = self.kwargs['admin_id']
        obj = Administrator.objects.get(pk=admin_id)
        return obj

    def form_valid(self, form):
        admin_id = self.kwargs['admin_id']
        administrator = Administrator.objects.get(pk=admin_id)
        admin_to_edit = form.save(commit=False)
        try:
            country_name = self.request.POST.get('country')
            country = Country.objects.get(name=country_name)
        except ObjectDoesNotExist:
            country = None
        admin_to_edit.country = country
        try:
            state_name = self.request.POST.get('state')
            state = Region.objects.get(name=state_name)
        except ObjectDoesNotExist:
            state = None
        admin_to_edit.state = state
        try:
            city_name = self.request.POST.get('city')
            city = City.objects.get(name=city_name)
        except ObjectDoesNotExist:
            city = None
        admin_to_edit.city = city
        organization_id = self.request.POST.get('organization_name')
        organization = get_organization_by_id(organization_id)
        if organization:
            admin_to_edit.organization = organization
        else:
            unlisted_org = self.request.POST.get('unlisted_organization')
            org = create_organization(unlisted_org)
            admin_to_edit.organization = org

        # update the volunteer
        admin_to_edit.save()
        return HttpResponseRedirect(
            reverse('administrator:profile', args=[admin_id, ])
        )


'''
  The view to display Admin profile.
  It uses DetailView which is a generic
  class-based views are designed to display data.
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

