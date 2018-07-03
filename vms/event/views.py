# standard library
import datetime

# third party
from braces.views import LoginRequiredMixin

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.edit import DeleteView

# local Django
from administrator.utils import admin_required
from event.forms import EventForm, EventDateForm, SearchEventForm
from event.models import Event
from event.services import check_edit_event, get_event_by_id, get_events_by_date, get_events_ordered_by_name, remove_empty_events_for_volunteer, search_events
from job.services import get_jobs_by_event_id, get_jobs_ordered_by_title
from volunteer.utils import vol_id_check
from vms.utils import check_correct_volunteer_shift_sign_up

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


class EventCreateView(LoginRequiredMixin, AdministratorLoginRequiredMixin,
                      FormView):
    template_name = 'event/create.html'
    form_class = EventForm

    def form_valid(self, form):
        start_date = form.cleaned_data['start_date']
        if start_date < (datetime.date.today() - datetime.timedelta(days=1)):
            messages.add_message(
                self.request, messages.INFO,
                'Start date should be today\'s date or later.')
            return render(self.request, 'event/create.html', {
                'form': form,
            })
        else:
            form.save()
            return HttpResponseRedirect(reverse('event:search'))


class EventDeleteView(LoginRequiredMixin, AdministratorLoginRequiredMixin,
                      DeleteView):
    template_name = 'event/delete.html'
    success_url = reverse_lazy('event:search')
    model = Event

    def get_object(self, queryset=None):
        event_id = self.kwargs['event_id']
        event = Event.objects.get(pk=event_id)
        if event:
            return event

    def delete(self, request, *args, **kwargs):
        event = self.get_object()
        jobs_in_event = event.job_set.all()
        if event and (not jobs_in_event):
            event.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, 'event/delete_error.html')


class EventUpdateView(LoginRequiredMixin, AdministratorLoginRequiredMixin,
                      UpdateView, FormView):
    form_class = EventForm
    template_name = 'event/edit.html'
    success_url = reverse_lazy('event:search')

    def get_object(self, queryset=None):
        event_id = self.kwargs['event_id']
        obj = Event.objects.get(pk=event_id)
        return obj

    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        job_obj = get_jobs_by_event_id(self.kwargs['event_id'])
        context['job_list'] = job_obj.values_list('start_date',
                                                  'end_date').distinct()
        return context

    def post(self, request, *args, **kwargs):
        event_id = self.kwargs['event_id']
        if event_id:
            event = get_event_by_id(event_id)
            form = EventForm(self.request.POST, instance=event)
            if form.is_valid():
                start_date_event = form.cleaned_data['start_date']
                end_date_event = form.cleaned_data['end_date']
                event_edit = check_edit_event(event_id, start_date_event,
                                              end_date_event)
                if not event_edit['result']:
                    return render(
                        request, 'event/edit_error.html', {
                            'count': event_edit['invalid_count'],
                            'jobs': event_edit['invalid_jobs']
                        })
                if start_date_event < datetime.date.today():
                    data = request.POST.copy()
                    data['end_date'] = end_date_event
                    messages.add_message(
                        request, messages.INFO,
                        'Start date should be today\'s date or later.')
                    form = EventForm(data)
                    return render(request, 'event/edit.html', {
                        'form': form,
                    })
                else:
                    form.save()
                    return HttpResponseRedirect(reverse('event:search'))
            else:
                data = request.POST.copy()
                try:
                    data['end_date'] = form.cleaned_data['end_date']
                except KeyError:
                    data['end_date'] = ''
                form = EventForm(data)
                return render(request, 'event/edit.html', {
                    'form': form,
                })


@login_required
@check_correct_volunteer_shift_sign_up
@vol_id_check
def list_sign_up(request, volunteer_id):
    if request.method == 'POST':
        form = EventDateForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            event_list = get_events_by_date(start_date, end_date)
            event_list = remove_empty_events_for_volunteer(
                event_list, volunteer_id)
            return render(
                request, 'event/list_sign_up.html', {
                    'form': form,
                    'event_list': event_list,
                    'volunteer_id': volunteer_id
                })
    else:
        event_list = get_events_ordered_by_name()
        event_list = remove_empty_events_for_volunteer(event_list,
                                                       volunteer_id)
        return render(request, 'event/list_sign_up.html', {
            'event_list': event_list,
            'volunteer_id': volunteer_id
        })


@login_required
@admin_required
def search(request):
    jobs_list = get_jobs_ordered_by_title()
    if request.method == 'POST':
        form = SearchEventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            job_id = form.cleaned_data['job']
            search_result_list = search_events(
                name, start_date, end_date, city, state, country, job_id)
            return render(
                request, 'event/list.html', {
                    'jobs_list': jobs_list,
                    'form': form,
                    'has_searched': True,
                    'search_result_list': search_result_list
                })
    else:
        form = SearchEventForm()

    return render(
        request, 'event/list.html', {
            'jobs_list': jobs_list,
            'form': form,
            'has_searched': False,
        })
