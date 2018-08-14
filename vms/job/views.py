# third party
from braces.views import LoginRequiredMixin

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist


# local Django
from event.services import get_events_ordered_by_name, get_event_by_id
from job.forms import JobForm, SearchJobForm
from job.models import Job
from job.services import (get_job_by_id, get_jobs_ordered_by_title,
                          check_edit_job, remove_empty_jobs_for_volunteer,
                          search_jobs, get_jobs_by_event_id)


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


class CreateJobView(LoginRequiredMixin, AdministratorLoginRequiredMixin,
                    FormView):
    template_name = 'job/create.html'
    form_class = JobForm

    def get_context_data(self, **kwargs):
        context = super(CreateJobView, self).get_context_data(**kwargs)
        context['event_list'] = get_events_ordered_by_name()
        return context

    def form_valid(self, form):
        event_id = self.request.POST.get('event_id')
        event = get_event_by_id(event_id)
        start_date_event = event.start_date
        end_date_event = event.end_date
        start_date_job = form.cleaned_data.get('start_date')
        end_date_job = form.cleaned_data.get('end_date')
        job_name = form.cleaned_data.get('name')
        flag = Job.objects.filter(event=event, name=job_name).exists()
        event_list = get_events_ordered_by_name()
        if (start_date_job >= start_date_event and
                end_date_job <= end_date_event and not flag):
            job = form.save(commit=False)
            if event:
                job.event = event
            else:
                raise Http404
            job.save()
            return HttpResponseRedirect(reverse('job:list'))
        else:
            raise_err = 'Job dates should lie within Event dates'
            if flag:
                raise_err = 'Job with the same name already exists'
            messages.add_message(self.request, messages.INFO, raise_err)
            return render(
                self.request,
                'job/create.html',
                {'form': form, 'event_list': event_list, 'last_event': event}
            )


class JobDeleteView(LoginRequiredMixin, AdministratorLoginRequiredMixin,
                    DeleteView):
    model_form = Job
    template_name = 'job/delete.html'
    success_url = reverse_lazy('job:list')

    def get_object(self, queryset=None):
        job_id = self.kwargs['job_id']
        job = Job.objects.get(pk=job_id)
        if job:
            return job

    def delete(self, request, *args, **kwargs):
        job = self.get_object()
        shifts_in_job = job.shift_set.all()
        if job and (not shifts_in_job):
            job.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, 'job/delete_error.html')


class JobDetailView(LoginRequiredMixin, DetailView):
    template_name = 'job/details.html'

    def get_object(self, queryset=None):
        job_id = self.kwargs['job_id']
        obj = Job.objects.get(pk=job_id)
        return obj


class JobUpdateView(LoginRequiredMixin, AdministratorLoginRequiredMixin,
                    UpdateView, FormView):
    model_form = Job
    form_class = JobForm
    template_name = 'job/edit.html'
    success_url = reverse_lazy('job:list')

    def get_object(self, queryset=None):
        job_id = self.kwargs['job_id']
        obj = Job.objects.get(pk=job_id)
        return obj

    def get_context_data(self, **kwargs):
        context = super(JobUpdateView, self).get_context_data(**kwargs)
        context['event_list'] = get_events_ordered_by_name()
        return context

    def form_valid(self, form):
        job_id = self.kwargs['job_id']
        event_id = self.request.POST.get('event_id')
        job = get_job_by_id(job_id)
        event = get_event_by_id(event_id)
        start_date_event = event.start_date
        end_date_event = event.end_date
        start_date_job = form.cleaned_data.get('start_date')
        end_date_job = form.cleaned_data.get('end_date')
        event_list = get_events_ordered_by_name()
        job_edit = check_edit_job(job_id, start_date_job, end_date_job)
        if not job_edit['result']:
            return render(self.request, 'job/edit_error.html', {
                'count': job_edit['invalid_count']
            })
        if (start_date_job >= start_date_event and
                end_date_job <= end_date_event):
            job_to_edit = form.save(commit=False)
            if event:
                job_to_edit.event = event
            else:
                raise Http404
            job_to_edit.save()
            return HttpResponseRedirect(reverse('job:list'))
        else:
            messages.add_message(self.request, messages.INFO,
                                 'Job dates should lie within Event dates')
            return render(self.request, 'job/edit.html', {
                'form': form,
                'event_list': event_list,
                'job': job
            })


@login_required
def list_sign_up(request, event_id, volunteer_id):
    if event_id:
        event = get_event_by_id(event_id)
        if request.method == 'POST':
            form = SearchJobForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                city = form.cleaned_data['city']
                state = form.cleaned_data['state']
                country = form.cleaned_data['country']
                search_result = search_jobs(name, start_date, end_date,
                                            city, state, country, '')
                search_result_list = search_result.filter(event_id=event_id)
        else:
                form = SearchJobForm()
                search_result_list = get_jobs_by_event_id(event_id)
        job_list = remove_empty_jobs_for_volunteer(
            search_result_list,
            volunteer_id
        )
        return render(
            request, 'job/list_sign_up.html', {
                'form': form,
                'job_list': job_list,
                'volunteer_id': volunteer_id,
                'event': event,
            })
    else:
        raise Http404


class JobListView(AdministratorLoginRequiredMixin, FormView):
    template_name = "job/list.html"
    form_class = SearchJobForm

    def get(self, request, *args, **kwargs):
        search_result_list = get_jobs_ordered_by_title()
        return render(
            request,
            'job/list.html',
            {
                'search_result_list': search_result_list
            }
        )

    def post(self, request, *args, **kwargs):
        search_result_list = get_jobs_ordered_by_title()
        form = SearchJobForm(self.request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            event = form.cleaned_data['event']
            search_result_list = search_jobs(
                name, start_date, end_date,
                city, state, country, event
            )
        return render(
            request,
            'job/list.html',
            {
                'form': form,
                'search_result_list': search_result_list
            }
        )

