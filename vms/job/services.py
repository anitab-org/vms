from django.core.exceptions import ObjectDoesNotExist

from job.models import Job
from shift.services import get_shifts_with_open_slots_for_volunteer

def job_not_empty(job_id):
    """ Check if the job exists and is not empty """
    result = True
    job = get_job_by_id(job_id)
    if not job:
        result = False
    return result


def delete_job(job_id):

    result = True
    job = get_job_by_id(job_id)

    if job_not_empty(job_id):
        shifts_in_job = job.shift_set.all()

    if job and (not shifts_in_job):
        job.delete()
    else:
        result = False

    return result


def get_job_by_id(job_id):

    is_valid = True
    result = None

    try:
        job = Job.objects.get(pk=job_id)
    except ObjectDoesNotExist:
        is_valid = False

    if is_valid:
        result = job

    return result


def get_jobs_by_event_id(e_id):
    job_list = Job.objects.filter(event_id=e_id)
    return job_list


def get_jobs_ordered_by_title():
    job_list = Job.objects.all().order_by('name')
    return job_list


def remove_empty_jobs_for_volunteer(job_list, volunteer_id):
    """ Removes all jobs from a job list without shifts """
    new_job_list = []
    for job in job_list:
        shift_list = get_shifts_with_open_slots_for_volunteer(job.id, volunteer_id)
        if shift_list:
            new_job_list.append(job)
    return new_job_list
