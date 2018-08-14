# third party
from braces.views import LoginRequiredMixin

# Django
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

# local Django
from administrator.models import Administrator
from organization.forms import OrganizationForm
from organization.models import Organization
from organization.services import get_organization_by_id, ObjectDoesNotExist
from volunteer.models import Volunteer


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
            return super(AdministratorLoginRequiredMixin, self).dispatch(
                request, *args, **kwargs)


class OrganizationCreateView(LoginRequiredMixin,
                             AdministratorLoginRequiredMixin, FormView):
    template_name = 'organization/create.html'
    form_class = OrganizationForm

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('organization:list'))


class OrganizationDeleteView(LoginRequiredMixin,
                             AdministratorLoginRequiredMixin, DeleteView):
    template_name = 'organization/delete.html'
    success_url = reverse_lazy('organization:list')
    model = Organization

    def get_object(self, queryset=None):
        organization_id = self.kwargs['organization_id']
        org = Organization.objects.get(pk=organization_id)
        if org:
            return org

    def delete(self, request, *args, **kwargs):
        org = self.get_object()
        volunteers_in_organization = org.volunteer_set.all()
        administrators_in_organization = org.administrator_set.all()
        if org and (not volunteers_in_organization) and (
                not administrators_in_organization):
            org.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, 'organization/delete_error.html')


class OrganizationUpdateView(LoginRequiredMixin,
                             AdministratorLoginRequiredMixin, UpdateView):
    template_name = 'organization/edit.html'
    success_url = reverse_lazy('organization:list')
    form_class = OrganizationForm

    def get_object(self, queryset=None):
        org_id = self.kwargs['organization_id']
        obj = Organization.objects.get(pk=org_id)
        return obj


class OrganizationListView(LoginRequiredMixin, ListView):
    model_form = Organization
    template_name = "organization/list.html"

    def get_queryset(self):
        organizations = Organization.objects.order_by('name')
        return organizations


def approve(request, organization_id):
    """
    approves the pending organizatons

    :param organization_id: The id of the pending organization
    :return: redirect to list of organizations
    """
    unlisted_org = get_organization_by_id(organization_id)
    unlisted_org.approved_status = 1
    unlisted_org.save()
    return HttpResponseRedirect('/organization/list')


def reject(request, organization_id):
    """
    rejects the pending organizatons

    :param organization_id: The id of the pending organization
    :return: redirect to list of organizations
    """
    unlisted_org = get_organization_by_id(organization_id)
    unlisted_org.approved_status = 2
    unlisted_org.save()
    try:
        vol_email = Volunteer.objects.get(organization=unlisted_org).email
        try:
            send_mail(
                "Organization Rejected",
                "The organization you filled while sign-up has been rejected",
                "messanger@localhost.com",
                [vol_email],
                fail_silently=False
            )
        except Exception:
            raise Exception("There was an error in sending emails.")
    except Exception:
        admin_email = Administrator.objects.get(organization=unlisted_org).email
        try:
            send_mail(
                "Organization Rejected",
                "The organization you filled while sign-up has been rejected",
                "messanger@localhost.com",
                [admin_email],
                fail_silently=False
            )
        except Exception:
            raise Exception("There was an error in sending emails.")
    return HttpResponseRedirect('/organization/list')
