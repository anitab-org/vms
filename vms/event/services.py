from django.core.exceptions import ObjectDoesNotExist

from event.models import Event
from job.models import Job
from shift.models import Shift


def event_not_empty(event_id):
    """ Checks if the event exists and is not empty """
    result = True
    event = get_event_by_id(event_id)
    if not event:
        result = False
    return result


def get_event_by_shift_id(shift_id):
    """
    Returns an event for the shift. Can be helpful for finding an event
    """
    is_valid = True
    result = None

    try:
        shift = Shift.objects.get(pk=shift_id)
        event = shift.job.event
    except ObjectDoesNotExist:
        is_valid = False

    if is_valid:
        result = event

    return result

# need to check that this event is not accociated with any jobs,
# otherwise the jobs that it is associated with will be cascade deleted
def delete_event(event_id):

    result = True
    event = get_event_by_id(event_id)

    if event_not_empty(event_id):
        # check if there are currently any jobs associated with this event
        jobs_in_event = event.job_set.all()

        # can only delete an event if no jobs are currently associated with it
        if event and (not jobs_in_event):
            event.delete()
        else:
            result = False
    else:
        result = False

    return result


def get_event_by_id(event_id):

    is_valid = True
    result = None

    try:
        event = Event.objects.get(pk=event_id)
    except ObjectDoesNotExist:
        is_valid = False

    if is_valid:
        result = event

    return result


def get_events_by_date(start_date, end_date):
    is_valid = True
    result = None
    try:
        event_list = Event.objects.filter(
                start_date__gte=start_date,
                start_date__lte=end_date
                ).order_by('start_date')
    except ObjectDoesNotExist:
        is_valid = False

    if is_valid:
        result = event_list

    return result

def get_events_ordered_by_name():
    event_list = Event.objects.all().order_by('name')
    return event_list
