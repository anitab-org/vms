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
from django.views.generic import ListView

# local Django
from event.forms import EventForm, EventDateForm
from event.models import Event
from event.services import check_edit_event, get_event_by_id, get_events_by_date, get_events_ordered_by_name, remove_empty_events_for_volunteer
from job.services import get_jobs_by_event_id
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
            return HttpResponseRedirect(reverse('event:list'))


class EventDeleteView(LoginRequiredMixin, AdministratorLoginRequiredMixin,
                      DeleteView):
    template_name = 'event/delete.html'
    success_url = reverse_lazy('event:list')
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
    success_url = reverse_lazy('event:list')

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
                    return HttpResponseRedirect(reverse('event:list'))
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


class EventListView(LoginRequiredMixin, AdministratorLoginRequiredMixin,
                    ListView):
    model_form = Event
    template_name = "event/list.html"

    def get_queryset(self):
        events = Event.objects.all().order_by('name')
        return events


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
