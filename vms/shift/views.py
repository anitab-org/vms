# standard library
from datetime import date, timedelta
from django.utils import timezone

# third party
from braces.views import LoginRequiredMixin

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DeleteView, ListView
from django.views.generic.edit import FormView, UpdateView

# local Django
from event.models import Event
from job.models import Job
from job.services import get_job_by_id
from shift.forms import HoursForm, ShiftForm, EditForm
from shift.models import Shift, EditRequest
from shift.services import (get_shift_by_id, add_shift_hours,
                            cancel_shift_registration, clear_shift_hours,
                            get_future_shifts_by_volunteer_id,
                            edit_shift_hours, get_shift_slots_remaining,
                            get_unlogged_shifts_by_volunteer_id,
                            get_logged_volunteers_by_shift_id, delete_shift,
                            get_volunteers_by_shift_id, get_volunteer_by_id,
                            get_volunteer_shifts_with_hours,
                            get_shifts_ordered_by_date, register,
                            get_shifts_with_open_slots_for_volunteer,
                            get_volunteer_shift_by_id, get_shifts_by_job_id)
from volunteer.forms import SearchVolunteerForm
from volunteer.models import Volunteer
from volunteer.services import get_all_volunteers, search_volunteers
from volunteer.utils import vol_id_check
from vms.utils import check_correct_volunteer


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


class AddHoursView(LoginRequiredMixin, FormView):
    template_name = 'shift/add_hours.html'
    form_class = HoursForm

    @method_decorator(check_correct_volunteer)
    def dispatch(self, *args, **kwargs):
        return super(AddHoursView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddHoursView, self).get_context_data(**kwargs)
        shift_id = self.kwargs['shift_id']
        volunteer_id = self.kwargs['volunteer_id']
        context['volunteer_id'] = volunteer_id
        context['shift_id'] = shift_id
        context['shift'] = get_shift_by_id(shift_id)
        return context

    def form_valid(self, form):
        shift_id = self.kwargs['shift_id']
        volunteer_id = self.kwargs['volunteer_id']
        shift = get_shift_by_id(shift_id)
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        shift_start_time = shift.start_time
        shift_end_time = shift.end_time
        try:
            if end_time > start_time:
                if (start_time >= shift_start_time and
                        end_time <= shift_end_time):
                    add_shift_hours(volunteer_id, shift_id, start_time,
                                    end_time)
                    return HttpResponseRedirect(
                        reverse('shift:view_hours', args=(volunteer_id, )))
                else:
                    messages.add_message(
                        self.request, messages.INFO,
                        'Logged hours should be between shift hours')
                    return render(
                        self.request, 'shift/add_hours.html', {
                            'form': form,
                            'shift_id': shift_id,
                            'volunteer_id': volunteer_id,
                            'shift': shift,
                        })
            else:
                messages.add_message(
                    self.request, messages.INFO,
                    'End time should be greater than start time')
                return render(
                    self.request, 'shift/add_hours.html', {
                        'form': form,
                        'shift_id': shift_id,
                        'volunteer_id': volunteer_id,
                        'shift': shift,
                    })
        except:
            raise Http404


class AddHoursManagerView(AdministratorLoginRequiredMixin, FormView):
    template_name = 'shift/add_hours_manager.html'
    form_class = HoursForm

    def get_context_data(self, **kwargs):
        context = super(AddHoursManagerView, self).get_context_data(**kwargs)
        shift_id = self.kwargs['shift_id']
        volunteer_id = self.kwargs['volunteer_id']
        context['volunteer_id'] = volunteer_id
        context['shift_id'] = shift_id
        context['shift'] = get_shift_by_id(shift_id)
        return context

    def form_valid(self, form):
        shift_id = self.kwargs['shift_id']
        volunteer_id = self.kwargs['volunteer_id']
        shift = get_shift_by_id(shift_id)
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        shift_start_time = shift.start_time
        shift_end_time = shift.end_time
        try:
            if end_time > start_time:
                if (start_time >= shift_start_time and
                        end_time <= shift_end_time):
                    add_shift_hours(volunteer_id, shift_id, start_time,
                                    end_time)
                    return HttpResponseRedirect(
                        reverse(
                            'shift:manage_volunteer_shifts',
                            args=(volunteer_id, )))
                else:
                    messages.add_message(
                        self.request, messages.INFO,
                        'Logged hours should be between shift hours')
                    return render(
                        self.request, 'shift/add_hours_manager.html', {
                            'form': form,
                            'shift_id': shift_id,
                            'volunteer_id': volunteer_id,
                            'shift': shift,
                        })

            else:
                messages.add_message(
                    self.request, messages.INFO,
                    'End time should be greater than start time')
                return render(
                    self.request, 'shift/add_hours_manager.html', {
                        'form': form,
                        'shift_id': shift_id,
                        'volunteer_id': volunteer_id,
                        'shift': shift,
                    })
        except:
            raise Http404


@login_required
def cancel(request, shift_id, volunteer_id):

    if shift_id and volunteer_id:

        user = request.user
        admin = None
        volunteer = None

        try:
            admin = user.administrator
        except ObjectDoesNotExist:
            pass
        try:
            volunteer = user.volunteer
        except ObjectDoesNotExist:
            pass

        # check that either an admin or volunteer is logged in
        if not admin and not volunteer:
            return render(request, 'vms/no_volunteer_rights.html', status=403)

        # if a volunteer is logged in,
        # verify that they are canceling their own shift
        if volunteer:
            if int(volunteer.id) != int(volunteer_id):
                return render(
                    request, 'vms/no_volunteer_rights.html', status=403)

        if request.method == 'POST':
            try:
                cancel_shift_registration(volunteer_id, shift_id)
                if admin:
                    vol_email = Volunteer.objects.get(pk=volunteer_id).email
                    shift_object = get_shift_by_id(shift_id)
                    job_object = Job.objects.get(shift=shift_object)
                    event_object = Event.objects.get(job=job_object)
                    message = render_to_string(
                        'shift/cancel_email.txt',
                        {
                            'admin_first_name': admin.first_name,
                            'admin_last_name': admin.last_name,
                            'shift_start_time': shift_object.start_time,
                            'shift_end_time': shift_object.end_time,
                            'admin_email': admin.email,
                            'job_name': job_object.name,
                            'event_name': event_object.name,
                            'shift_date': shift_object.date,
                        }
                    )
                    try:
                        send_mail(
                            "Shift Cancelled", message,
                            "messanger@localhost.com", [vol_email]
                        )
                    except Exception:
                        raise Exception("There was an error in sending email.")
                    return HttpResponseRedirect(
                        reverse(
                            'shift:manage_volunteer_shifts',
                            args=(volunteer_id, )))
                elif volunteer:
                    return HttpResponseRedirect(
                        reverse(
                            'shift:view_volunteer_shifts',
                            args=(volunteer_id, )))
                else:
                    raise Http404
            except Exception:
                raise Http404
        else:
            return render(request, 'shift/cancel_shift.html', {
                'shift_id': shift_id,
                'volunteer_id': volunteer_id
            })
    else:
        raise Http404


class ClearHoursManager(AdministratorLoginRequiredMixin, TemplateView):
    template_name = 'shift/clear_hours.html'

    def get_context_data(self, **kwargs):
        context = super(ClearHoursManager, self).get_context_data(**kwargs)
        shift_id = self.kwargs['shift_id']
        volunteer_id = self.kwargs['volunteer_id']
        context['volunteer_id'] = volunteer_id
        context['shift_id'] = shift_id
        context['result'] = clear_shift_hours(volunteer_id, shift_id)
        return context

    def post(self, request, *args, **kwargs):
        volunteer_id = self.kwargs['volunteer_id']
        shift_id = self.kwargs['shift_id']
        result = clear_shift_hours(volunteer_id, shift_id)
        if result:
            return HttpResponseRedirect(
                reverse(
                    'shift:manage_volunteer_shifts', args=(volunteer_id, )))
        else:
            raise Http404


class ShiftCreateView(AdministratorLoginRequiredMixin, FormView):
    template_name = 'shift/create.html'
    form_class = ShiftForm
    success_url = 'shift:list_shifts'

    def get_context_data(self, **kwargs):
        context = super(ShiftCreateView, self).get_context_data(**kwargs)
        job_id = self.kwargs['job_id']
        context['job_id'] = job_id
        job = get_job_by_id(job_id)
        event = job.event
        context['job'] = job
        context['event'] = job.event
        context['country'] = event.country
        context['state'] = event.state
        context['city'] = event.city
        context['address'] = event.address
        context['venue'] = event.venue
        return context

    def form_valid(self, form):
        job_id = self.kwargs['job_id']
        job = get_job_by_id(job_id)
        start_date_job = job.start_date
        end_date_job = job.end_date
        shift_date = form.cleaned_data['date']
        shift_start_time = form.cleaned_data['start_time']
        shift_end_time = form.cleaned_data['end_time']
        if (start_date_job <= shift_date <= end_date_job and
                shift_end_time > shift_start_time):
            shift = form.save(commit=False)
            shift.job = job
            shift.save()
            return HttpResponseRedirect(
                reverse('shift:list_shifts', args=(job_id, )))
        else:
            if shift_date < start_date_job or shift_date > end_date_job:
                messages.add_message(self.request, messages.INFO,
                                     'Shift date should lie within Job dates')
            if shift_end_time <= shift_start_time:
                messages.add_message(
                    self.request, messages.INFO,
                    'Shift end time should be greater than start time')
            return render(self.request, 'shift/create.html', {
                'form': form,
                'job_id': job_id,
                'job': job
            })


class ShiftDeleteView(AdministratorLoginRequiredMixin, DeleteView):
    model_form = Shift
    template_name = 'shift/delete.html'
    success_url = reverse_lazy('shift:list_jobs')

    def get_object(self, queryset=None):
        shift_id = self.kwargs['shift_id']
        shift = Shift.objects.get(pk=shift_id)
        if shift:
            return shift

    def delete(self, request, *args, **kwargs):
        shift_id = self.kwargs['shift_id']
        shift = self.get_object()
        job_id = shift.job.id
        result = delete_shift(shift_id)
        if result:
            shift_list = get_shifts_by_job_id(job_id)
            if shift_list:
                return HttpResponseRedirect(
                    reverse('shift:list_shifts', args=(job_id, )))
            else:
                return HttpResponseRedirect(reverse('shift:list_jobs'))
        else:
            return render(request, 'shift/delete_error.html')


class ShiftUpdateView(AdministratorLoginRequiredMixin, UpdateView):
    form_class = ShiftForm
    template_name = 'shift/edit.html'
    success_url = reverse_lazy('shift:list_shifts')

    def get_context_data(self, **kwargs):
        context = super(ShiftUpdateView, self).get_context_data(**kwargs)
        shift = get_shift_by_id(self.kwargs['shift_id'])
        context['shift'] = shift
        context['job'] = shift.job
        return context

    def get_object(self, queryset=None):
        shift_id = self.kwargs['shift_id']
        obj = Shift.objects.get(pk=shift_id)
        return obj

    def form_valid(self, form):
        shift_id = self.kwargs['shift_id']
        shift = get_shift_by_id(shift_id)
        job = shift.job
        start_date_job = job.start_date
        end_date_job = job.end_date
        shift_date = form.cleaned_data['date']
        shift_start_time = form.cleaned_data['start_time']
        shift_end_time = form.cleaned_data['end_time']
        max_vols = form.cleaned_data['max_volunteers']

        # save when all conditions satisfied
        if (start_date_job <= shift_date <= end_date_job and
                shift_end_time > shift_start_time and
                max_vols >= len(shift.volunteers.all())):
            shift_to_edit = form.save(commit=False)
            shift_to_edit.job = job
            shift_to_edit.save()
            return HttpResponseRedirect(
                reverse('shift:list_shifts', args=(shift.job.id, )))
        else:
            if shift_date < start_date_job or shift_date > end_date_job:
                messages.add_message(self.request, messages.INFO,
                                     'Shift date should lie within Job dates')
            if shift_end_time <= shift_start_time:
                messages.add_message(
                    self.request, messages.INFO,
                    'Shift end time should be greater than start time')
            if max_vols < len(shift.volunteers.all()):
                messages.add_message(
                    self.request, messages.INFO,
                    'Max volunteers should be greater than or equal to'
                    ' the already assigned volunteers.')
            return render(self.request, 'shift/edit.html', {
                'form': form,
                'shift': shift,
                'job': shift.job
            })


class EditHoursView(LoginRequiredMixin, FormView):
    template_name = 'shift/edit_hours.html'
    form_class = EditForm

    @method_decorator(check_correct_volunteer)
    def dispatch(self, *args, **kwargs):
        return super(EditHoursView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EditHoursView, self).get_context_data(**kwargs)
        volunteer_id = self.kwargs['volunteer_id']
        shift_id = self.kwargs['shift_id']
        context['volunteer_shift'] = \
            get_volunteer_shift_by_id(volunteer_id, shift_id)
        context['shift'] = get_shift_by_id(shift_id)
        return context

    def form_valid(self, form):
        volunteer_id = self.kwargs['volunteer_id']
        shift_id = self.kwargs['shift_id']
        shift = get_shift_by_id(shift_id)
        volunteer_shift = get_volunteer_shift_by_id(volunteer_id, shift_id)
        volunteer = get_volunteer_by_id(volunteer_id)
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        shift_start_time = shift.start_time
        shift_end_time = shift.end_time
        event = shift.job.event
        site = get_current_site(self.request)
        try:
            if end_time > start_time:
                if (start_time >= shift_start_time and
                        end_time <= shift_end_time):
                    request = form.save(commit=False)
                    request.volunteer_shift = volunteer_shift
                    request.save()
                    message = render_to_string(
                        'shift/request_admin.html',
                        {
                            'volunteer': volunteer,
                            'new_start_time': start_time,
                            'new_end_time': end_time,
                            'original_start_time': shift_start_time,
                            'original_end_time': shift_end_time,
                            'event': event,
                            'edit_request': request,
                            'shift_id': shift_id,
                            'domain': site.domain,
                        }
                    )
                    try:
                        send_mail(
                            "Edit request", message,
                            "messanger@localhost.com",
                            ["systerskeeper@gmail.com"]
                        )
                    except Exception:
                        raise Exception(
                            "There was an error in sending the email."
                        )
                    volunteer_shift.edit_requested = True
                    volunteer_shift.save()
                    return HttpResponseRedirect(
                        reverse('shift:view_hours', args=(volunteer_id, )))
                else:
                    messages.add_message(
                        self.request, messages.INFO,
                        'Logged hours should be between shift hours')
                    return render(
                        self.request, 'shift/edit_hours.html', {
                            'form': form,
                            'shift_id': shift_id,
                            'volunteer_id': volunteer_id,
                            'shift': shift,
                            'volunteer_shift': volunteer_shift,
                        })

            else:
                messages.add_message(
                    self.request, messages.INFO,
                    'End time should be greater than start time'
                )
                return render(
                    self.request, 'shift/edit_hours.html', {
                        'form': form,
                        'shift_id': shift_id,
                        'volunteer_id': volunteer_id,
                        'shift': shift,
                        'volunteer_shift': volunteer_shift,
                    })
        except Exception:
            raise Http404


class EditRequestManagerView(AdministratorLoginRequiredMixin, UpdateView):
    template_name = 'shift/edit_hours_manager.html'
    form_class = EditForm

    def get_context_data(self, **kwargs):
        context = super(EditRequestManagerView, self).get_context_data(**kwargs)
        shift_id = self.kwargs['shift_id']
        context['shift'] = get_shift_by_id(shift_id)
        volunteer_id = self.kwargs['volunteer_id']
        context['volunteer'] = get_volunteer_by_id(volunteer_id)
        context['volunteer_shift'] = \
            get_volunteer_shift_by_id(volunteer_id, shift_id)
        return context

    def get_object(self, queryset=None):
        edit_request_id = self.kwargs['edit_request_id']
        obj = EditRequest.objects.get(pk=edit_request_id)
        return obj

    def form_valid(self, form):
        edit_request_id = self.kwargs['edit_request_id']
        edit_request = EditRequest.objects.get(pk=edit_request_id)
        volunteer_id = self.kwargs['volunteer_id']
        volunteer = get_volunteer_by_id(volunteer_id)
        shift_id = self.kwargs['shift_id']
        shift = get_shift_by_id(shift_id)
        event = shift.job.event
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        shift_start_time = shift.start_time
        shift_end_time = shift.end_time
        try:
            if end_time > start_time:
                if (start_time >= shift_start_time and
                        end_time <= shift_end_time):
                    edit_shift_hours(volunteer_id, shift_id, start_time,
                                     end_time)
                    vol_email = volunteer.email
                    message = render_to_string(
                        'shift/request_status.html',
                        {
                            'volunteer_first_name': volunteer.first_name,
                            'event': event
                        }
                    )
                    try:
                        send_mail(
                            "Log Hours Edited", message,
                            "messanger@localhost.com", [vol_email]
                        )
                    except Exception:
                        raise Exception("There was an error in sending mail.")
                    return HttpResponseRedirect(
                        reverse(
                            'shift:manage_volunteer_shifts',
                            args=(volunteer_id, )))
                else:
                    messages.add_message(
                        self.request, messages.INFO,
                        'Logged hours should be between shift hours')
                    return render(
                        self.request, 'shift/edit_hours_manager.html', {
                            'form': form,
                            'shift_id': shift_id,
                            'volunteer_id': volunteer_id,
                            'shift': shift,
                            'edit_request_id': edit_request_id,
                        })

            else:
                messages.add_message(
                    self.request, messages.INFO,
                    'End time should be greater than start time')
                return render(
                    self.request, 'shift/edit_hours_manager.html', {
                        'form': form,
                        'shift_id': shift_id,
                        'volunteer_id': volunteer_id,
                        'shift': shift,
                        'edit_request_id': edit_request_id,
                    })

        except Exception:
            raise Http404


class EditHoursManagerView(AdministratorLoginRequiredMixin, FormView):
    template_name = 'shift/edit_hours_manager.html'
    form_class = HoursForm

    def get_context_data(self, **kwargs):
        context = super(EditHoursManagerView, self).get_context_data(**kwargs)
        volunteer_id = self.kwargs['volunteer_id']
        shift_id = self.kwargs['shift_id']
        context['volunteer_shift'] = \
            get_volunteer_shift_by_id(volunteer_id, shift_id)
        context['shift'] = get_shift_by_id(shift_id)
        return context

    def form_valid(self, form):
        volunteer_id = self.kwargs['volunteer_id']
        shift_id = self.kwargs['shift_id']
        shift = get_shift_by_id(shift_id)
        volunteer_shift = get_volunteer_shift_by_id(volunteer_id, shift_id)
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        shift_start_time = shift.start_time
        shift_end_time = shift.end_time
        try:
            if end_time > start_time:
                if (start_time >= shift_start_time and
                        end_time <= shift_end_time):
                    edit_shift_hours(volunteer_id, shift_id, start_time,
                                     end_time)
                    return HttpResponseRedirect(
                        reverse(
                            'shift:manage_volunteer_shifts',
                            args=(volunteer_id, )))
                else:
                    messages.add_message(
                        self.request, messages.INFO,
                        'Logged hours should be between shift hours')
                    return render(
                        self.request, 'shift/edit_hours_manager.html', {
                            'form': form,
                            'shift_id': shift_id,
                            'volunteer_id': volunteer_id,
                            'shift': shift,
                            'volunteer_shift': volunteer_shift,
                        })

            else:
                messages.add_message(
                    self.request, messages.INFO,
                    'End time should be greater than start time')
                return render(
                    self.request, 'shift/edit_hours_manager.html', {
                        'form': form,
                        'shift_id': shift_id,
                        'volunteer_id': volunteer_id,
                        'shift': shift,
                        'volunteer_shift': volunteer_shift,
                    })

        except:
            raise Http404


class JobListView(AdministratorLoginRequiredMixin,
                  ListView):  # Replaced by list_jobs
    template_name = 'shift/list_jobs.html'
    model_form = Job

    def get_queryset(self):
        job = Job.objects.all().order_by('name')
        return job


class ShiftListView(AdministratorLoginRequiredMixin,
                    TemplateView):  # Replaced by list_shifts
    template_name = 'shift/list_shifts.html'

    def get_context_data(self, **kwargs):
        context = super(ShiftListView, self).get_context_data(**kwargs)
        job_id = self.kwargs['job_id']
        context['shift_list'] = get_shifts_ordered_by_date(job_id)
        return context


@login_required
def list_shifts_sign_up(request, job_id, volunteer_id):
    if job_id:
        job = get_job_by_id(job_id)
        if job:
            shift_list = []
            shift_list_all = \
                get_shifts_with_open_slots_for_volunteer(job_id, volunteer_id)
            for shift in shift_list_all:
                sdate = shift["date"]
                today = date.today()
                if sdate >= today:
                    shift_list.append(shift)
            return render(request, 'shift/list_shifts_sign_up.html', {
                'shift_list': shift_list,
                'job': job,
                'volunteer_id': volunteer_id
            })
        else:
            raise Http404
    else:
        raise Http404


class ManageVolunteerShiftView(AdministratorLoginRequiredMixin, TemplateView):
    template_name = 'shift/manage_volunteer_shifts.html'

    def get_context_data(self, **kwargs):
        context = super(ManageVolunteerShiftView, self).get_context_data(
            **kwargs)
        volunteer_id = self.kwargs['volunteer_id']
        context['volunteer'] = get_volunteer_by_id(volunteer_id)
        context['upcoming_shift_list'] = \
            get_future_shifts_by_volunteer_id(volunteer_id)
        context['shift_list'] = \
            get_unlogged_shifts_by_volunteer_id(volunteer_id)
        context['shift_list_with_hours'] = \
            get_volunteer_shifts_with_hours(volunteer_id)
        return context


@login_required
def sign_up(request, shift_id, volunteer_id):
    if shift_id:
        shift = get_shift_by_id(shift_id)
        if shift:

            user = request.user
            admin = None
            volunteer = None

            try:
                admin = user.administrator
            except ObjectDoesNotExist:
                pass
            try:
                volunteer = user.volunteer
            except ObjectDoesNotExist:
                pass

            if not admin and not volunteer:
                return HttpResponse(status=403)

            if volunteer:
                if int(volunteer.id) != int(volunteer_id):
                    return HttpResponse(status=403)

            if request.method == 'POST':
                try:
                    result = register(volunteer_id, shift_id)
                    if result == "IS_VALID":
                        if admin:
                            vol_email = Volunteer.objects.get(
                                pk=volunteer_id).email
                            shift_object = get_shift_by_id(shift_id)
                            job_object = Job.objects.get(shift=shift_object)
                            event_object = Event.objects.get(job=job_object)
                            message = render_to_string(
                                'shift/sign_up_email.txt',
                                {
                                    'admin_first_name': admin.first_name,
                                    'admin_last_name': admin.last_name,
                                    'shift_start_time': shift_object.start_time,
                                    'shift_end_time': shift_object.end_time,
                                    'admin_email': admin.email,
                                    'job_name': job_object.name,
                                    'event_name': event_object.name,
                                    'shift_date': shift_object.date,
                                }
                            )
                            try:
                                send_mail(
                                    "Shift Assigned", message,
                                    "messanger@localhost.com", [vol_email],
                                    fail_silently=False
                                )
                            except Exception:
                                raise Exception(
                                    "There was an error in sending email."
                                )
                            return HttpResponseRedirect(
                                reverse(
                                    'shift:manage_volunteer_shifts',
                                    args=(volunteer_id, )))
                        if volunteer:
                            return HttpResponseRedirect(
                                reverse(
                                    'shift:view_volunteer_shifts',
                                    args=(volunteer_id, )))
                    else:
                        return render(request, 'shift/sign_up_error.html', {
                            'error_code': result
                        })
                except ObjectDoesNotExist:
                    raise Http404
            else:
                return render(request, 'shift/sign_up.html', {
                    'shift': shift,
                    'volunteer_id': volunteer_id
                })
        else:
            raise Http404
    else:
        raise Http404


class ViewHoursView(LoginRequiredMixin, FormView, TemplateView):
    template_name = 'shift/hours_list.html'
    form_class = HoursForm

    @method_decorator(check_correct_volunteer)
    @method_decorator(vol_id_check)
    def dispatch(self, *args, **kwargs):
        return super(ViewHoursView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ViewHoursView, self).get_context_data(**kwargs)
        volunteer_id = self.kwargs['volunteer_id']
        context['volunteer'] = get_volunteer_by_id(volunteer_id)
        context['shift_list'] = \
            get_unlogged_shifts_by_volunteer_id(volunteer_id)
        context['logged_volunteer_shift_list'] = \
            get_volunteer_shifts_with_hours(volunteer_id)
        context['init_date'] = timezone.now() - timedelta(days=7)
        return context


@login_required
@check_correct_volunteer
@vol_id_check
def view_volunteer_shifts(request, volunteer_id):
    shift_list = get_future_shifts_by_volunteer_id(volunteer_id)
    return render(request, 'shift/volunteer_shifts.html', {
        'shift_list': shift_list,
        'volunteer_id': volunteer_id,
    })


class VolunteerSearchView(AdministratorLoginRequiredMixin, FormView):
    template_name = 'shift/volunteer_search.html'
    form_class = SearchVolunteerForm
    success_url = 'volunteer_list'

    def get_context_data(self, **kwargs):
        context = super(VolunteerSearchView, self).get_context_data(**kwargs)
        context['volunteer_list'] = get_all_volunteers()
        context['has_searched'] = False
        return context

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        city = form.cleaned_data['city']
        state = form.cleaned_data['state']
        country = form.cleaned_data['country']
        organization = form.cleaned_data['organization']

        volunteer_list = search_volunteers(first_name, last_name, city, state,
                                           country, organization)
        return render(self.request, 'shift/volunteer_search.html', {
            'form': form,
            'has_searched': True,
            'volunteer_list': volunteer_list
        })


@login_required
def view_volunteers(request, shift_id):
    user = request.user
    admin = None

    try:
        admin = user.administrator
    except ObjectDoesNotExist:
        pass

    # check that an admin is logged in
    if not admin:
        return render(request, 'vms/no_admin_rights.html')
    else:
        if shift_id:
            shift = get_shift_by_id(shift_id)
            if shift:
                volunteer_list = get_volunteers_by_shift_id(shift_id)
                logged_volunteer_list = \
                    get_logged_volunteers_by_shift_id(shift_id)
                slots_remaining = get_shift_slots_remaining(shift_id)
                return render(
                    request, 'shift/list_volunteers.html', {
                        'volunteer_list': volunteer_list,
                        'shift': shift,
                        'slots_remaining': slots_remaining,
                        'logged_volunteer_list': logged_volunteer_list
                    })
            else:
                raise Http404
        else:
            raise Http404

