# third party
from braces.views import LoginRequiredMixin

# Django
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

# local Django
from organization.forms import OrganizationForm
from organization.models import Organization
from organization.services import ObjectDoesNotExist


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
    model_form = Organization
    template_name = 'organization/edit.html'
    success_url = reverse_lazy('organization:list')
    fields = '__all__'

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
