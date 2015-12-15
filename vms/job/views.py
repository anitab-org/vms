from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from job.models import Job
from job.forms import JobForm
from job.services import *
from event.services import *


@login_required
def is_admin(request):
    user = request.user
    admin = None

    try:
        admin = user.administrator
    except ObjectDoesNotExist:
        pass

    # check that an admin is logged in
    if admin is not None:
        return True
    else:
        return False


@login_required
def create(request):
    if is_admin(request):
        event_list = get_events_ordered_by_name()

        if request.method == 'POST':
            form = JobForm(request.POST)

            if form.is_valid():

                event_id = request.POST.get('event_id')
                event = get_event_by_id(event_id)
                start_date_event=event.start_date
                end_date_event=event.end_date
                start_date_job=form.cleaned_data.get('start_date')
                end_date_job=form.cleaned_data.get('end_date')
                if(start_date_job>=start_date_event and end_date_job<=end_date_event):
                    job = form.save(commit=False)
                    if event:
                        job.event = event
                    else:
                        raise Http404
                    job.save()
                    return HttpResponseRedirect(reverse('job:list'))
                else:
                    messages.add_message(request, messages.INFO, 'Job dates should lie within Event dates')
                    return render(
                    request,
                    'job/create.html',
                    {'form': form, 'event_list': event_list}
                    )

            else:
                return render(
                    request,
                    'job/create.html',
                    {'form': form, 'event_list': event_list}
                    )
        else:
            form = JobForm()
            return render(
                request,
                'job/create.html',
                {'form': form, 'event_list': event_list}
                )
    else:
        return render(request, 'vms/no_admin_rights.html')



@login_required
def delete(request, job_id):
    if is_admin(request):
        if job_id:
            if request.method == 'POST':
                result = delete_job(job_id)
                if result:
                    return HttpResponseRedirect(reverse('job:list'))
                else:
                    return render(request, 'job/delete_error.html', {'job_id': job_id})
            return render(request, 'job/delete.html', {'job_id': job_id})
        else:
            raise Http404
    else:
        return render(request, 'vms/no_admin_rights.html')


@login_required
def details(request, job_id):

    if job_id:
        job = get_job_by_id(job_id)
        if job:
            return render(request, 'job/details.html', {'job': job})
        else:
            raise Http404
    else:
        raise Http404


@login_required
def edit(request, job_id):
    if is_admin(request):
        job = None
        if job_id:
            job = get_job_by_id(job_id)

        event_list = get_events_ordered_by_name()

        if request.method == 'POST':
            form = JobForm(request.POST, instance=job)
            if form.is_valid():
                job_to_edit = form.save(commit=False)
                event_id = request.POST.get('event_id')
                event = get_event_by_id(event_id)
                if event:
                    job_to_edit.event = event
                else:
                    raise Http404
                job_to_edit.save()
                return HttpResponseRedirect(reverse('job:list'))
            else:
                return render(
                    request,
                    'job/edit.html',
                    {'form': form, 'event_list': event_list, 'job': job}
                    )
        else:
            form = JobForm(instance=job)
            return render(request, 'job/edit.html', {'form': form, 'event_list': event_list, 'job': job})
    else:
        return render(request, 'vms/no_admin_rights.html')


@login_required
def list(request):
    job_list = get_jobs_ordered_by_title()
    return render(request, 'job/list.html', {'job_list': job_list})


@login_required
def list_sign_up(request, event_id, volunteer_id):

    if event_id:
        event = get_event_by_id(event_id)
        if event:
            job_list = get_jobs_by_event_id(event_id)
            return render(request, 'job/list_sign_up.html', {'event': event, 'job_list': job_list, 'volunteer_id': volunteer_id})
        else:
            raise Http404
    else:
        raise Http404
