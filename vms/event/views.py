# standard library
import datetime
import json
import requests

# third party
from braces.views import LoginRequiredMixin

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.views import APIView
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import DetailView

# local Django
from administrator.utils import admin_required
from cities_light.models import Country, Region, City
from event.forms import EventForm, SearchEventForm
from event.models import Event
from event.services import (check_edit_event, get_event_by_id,
                            get_events_ordered_by_name,
                            remove_empty_events_for_volunteer, search_events)
from job.services import get_jobs_by_event_id
from volunteer.utils import vol_id_check
from vms.utils import check_correct_volunteer_shift_sign_up
from shift.utils import create_event_with_details


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

    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)
        context['country_list'] = Country.objects.all()
        return context

    def form_valid(self, form):
        country_list = Country.objects.all()
        start_date = form.cleaned_data['start_date']
        if start_date < (datetime.date.today() - datetime.timedelta(days=1)):
            messages.add_message(
                self.request, messages.INFO,
                'Start date should be today\'s date or later.')
            return render(self.request, 'event/create.html', {
                'form': form,
                'country_list': country_list,
            })
        else:
            event = form.save(commit=False)
            try:
                country_name = self.request.POST.get('country')
                country = Country.objects.get(name=country_name)
                event.country = country
            except ObjectDoesNotExist:
                country_name = None
            try:
                state_name = self.request.POST.get('state')
                state = Region.objects.get(name=state_name)
                event.state = state
            except ObjectDoesNotExist:
                state_name = None
            try:
                city_name = self.request.POST.get('city')
                city = City.objects.get(name=city_name)
                event.city = city
            except ObjectDoesNotExist:
                city_name = None
            event.save()
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


class EventDetailView(LoginRequiredMixin, DetailView):
    """
    The view to show the details of an Event
    Extends DetailView which is a generic class
    based view designed to display data.
    """

    template_name = 'event/details.html'

    def get_object(self, queryset=None):
        """
        This view shows the information about the event
        :param self: the event itself
        :return the object
        """

        event_id = self.kwargs['event_id']
        obj = Event.objects.get(pk=event_id)
        return obj


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
        context['country_list'] = Country.objects.all()
        event_id = self.kwargs['event_id']
        event = get_event_by_id(event_id)
        if event.country:
            country = event.country
            state_list = Region.objects.filter(country=country)
            context['state_list'] = state_list
        if event.state:
            state = event.state
            city_list = City.objects.filter(region=state)
            context['city_list'] = city_list
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
                    event_to_edit = form.save(commit=False)
                    try:
                        country_name = self.request.POST.get('country')
                        country = Country.objects.get(name=country_name)
                    except ObjectDoesNotExist:
                        country = None
                    event_to_edit.country = country
                    try:
                        state_name = self.request.POST.get('state')
                        state = Region.objects.get(name=state_name)
                    except ObjectDoesNotExist:
                        state = None
                    event_to_edit.state = state
                    try:
                        city_name = self.request.POST.get('city')
                        city = City.objects.get(name=city_name)
                    except ObjectDoesNotExist:
                        city = None
                    event_to_edit.city = city
                    event_to_edit.save()
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


@login_required
@check_correct_volunteer_shift_sign_up
@vol_id_check
def list_sign_up(request, volunteer_id):
    if request.method == 'POST':
        form = SearchEventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            search_result_list = search_events(
                name, start_date, end_date,
                city, state, country, ''
            )
    else:
        form = SearchEventForm()
        search_result_list = get_events_ordered_by_name()
    event_list = remove_empty_events_for_volunteer(search_result_list,
                                                   volunteer_id)
    return render(
        request, 'event/list_sign_up.html', {
            'form': form,
            'event_list': event_list,
            'volunteer_id': volunteer_id,
        })


@login_required
@admin_required
def list_events(request):
    """
    list of filtered events
    :return: search_result_list: filtered events based on name,
                                 start date, end date, state,
                                 city, country, job
    :return: SearchEventForm
    """
    search_result_list = get_events_ordered_by_name()
    today = datetime.date.today()
    if request.method == 'POST':
        form = SearchEventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            job = form.cleaned_data['job']
            search_result_list = search_events(
                name, start_date, end_date, city, state, country, job)
    else:
        form = SearchEventForm()

    return render(
        request, 'event/list.html', {
            'form': form,
            'search_result_list': search_result_list,
            'today': today
        })


class ApiForVolaView(APIView):

    @classmethod
    def return_event_data(cls, events):
        """function to return all or filtered event data"""
        event_list = list()
        for event in events:
            event_data = dict()
            event_data['event_name'] = event.name
            event_data['start_date'] = event.start_date
            event_data['end_date'] = event.end_date
            event_data['description'] = event.description
            event_data['address'] = event.address
            event_data['city'] = event.city.name if event.city else None
            event_data['state'] = event.state.name if event.state else None
            event_data['country'] = \
                event.country.name if event.country else None
            event_data['venue'] = event.venue
            event_list.append(event_data)
        return JsonResponse(event_list, safe=False)

    @classmethod
    def get(cls, request):
        # fetching all meetups
        events = Event.objects.all().order_by('start_date')
        api_for_vola_view = ApiForVolaView()
        return api_for_vola_view.return_event_data(events)

    @classmethod
    def post(cls, request):
        date = request.data['date']
        # fetching all events whose start date is
        # greater than or equal to the date posted
        events = Event.objects.filter(
            start_date__gte=date
        ).order_by('start_date')
        api_for_vola_view = ApiForVolaView()
        return api_for_vola_view.return_event_data(events)


def get_meetup(request):
    date = str(datetime.datetime.today().date())
    data = {'date': date}
    response = requests.post(
        'http://127.0.0.1:8000/meetup/api/v1/request_meetup_data/',
        data
    )
    if response.status_code == 200:
        json_data = json.loads(response.text)
        for meetup in json_data:
            start_date = meetup['start_date']
            venue = meetup['venue']
            name = meetup['event_name']
            end_date = start_date
            event_details = [name, start_date, end_date]
            event = create_event_with_details(event_details)
            event.venue = venue
            event.save()
        return HttpResponseRedirect(reverse('event:list'))
    else:
        return render(request, 'vms/no_connection.html')
