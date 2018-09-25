# Django
from django.core.exceptions import ObjectDoesNotExist

# local Django
from volunteer.models import Volunteer


def delete_volunteer(volunteer_id):
    result = False

    volunteer = get_volunteer_by_id(volunteer_id)

    if volunteer:
        # if the volunteer uploaded a resume, delete it as well
        if has_resume_file(volunteer_id):
            delete_volunteer_resume(volunteer_id)
        # Django docs recommend to set associated user
        # to not active instead of deleting the user
        user = volunteer.user
        user.is_active = False
        # make a call to update the user
        user.save()
        # then delete the volunteer
        volunteer.delete()
        result = True
    return result


def delete_volunteer_resume(volunteer_id):
    result = False

    volunteer = get_volunteer_by_id(volunteer_id)

    if volunteer and volunteer.resume_file:
        volunteer.resume_file.delete()
        result = True
    return result


def get_all_volunteers():

    volunteer_list = Volunteer.objects.all()
    return volunteer_list


def get_volunteer_by_id(volunteer_id):

    is_valid = True
    result = None

    try:
        volunteer = Volunteer.objects.get(pk=volunteer_id)
    except ObjectDoesNotExist:
        is_valid = False

    if is_valid:
        result = volunteer

    return result


def get_volunteer_resume_file_url(volunteer_id):

    result = None
    volunteer = get_volunteer_by_id(volunteer_id)

    if volunteer and volunteer.resume_file:
        result = volunteer.resume_file.url

    return result


def get_volunteers_ordered_by_first_name():
    volunteer_list = Volunteer.objects.all().order_by('first_name')
    return volunteer_list


def has_resume_file(volunteer_id):

    result = False
    volunteer = get_volunteer_by_id(volunteer_id)

    if volunteer and volunteer.resume_file:
        result = True

    return result


def search_volunteers(first_name, last_name, city, state, country,
                      organization, event, job):
    """Volunteers search
    None, one, or more parameters may be sent:
    first_name, last_name, city, state, country, organization, event, job

    If no search parameters are given, it returns all volunteers

    Examples:
    search_volunteers(None, None, None, None, None, None, None, None))
    will return all volunteers
    search_volunteers("Yoshi", None, None, None, None, None, None, None)
    will return all volunteers with the first name "Yoshi"
    search_volunteers(None, "Doe", None, None, None, None, None, None)
    will return all volunteers with the last name "Doe"
    """

    # if no search parameters are given, it returns all volunteers
    search_query = Volunteer.objects.all()
    # build query based on parameters provided
    if first_name:
        search_query = search_query.filter(first_name__icontains=first_name)
    if last_name:
        search_query = search_query.filter(last_name__icontains=last_name)
    if city:
        search_query = search_query.filter(city__name__icontains=city)
    if state:
        search_query = search_query.filter(state__name__icontains=state)
    if country:
        search_query = search_query.filter(country__name__icontains=country)
    if organization:
        search_query = search_query.filter(
            organization__name__icontains=organization
        )
    if event:
        search_query = search_query.filter(
            shift__job__event__name__icontains=event
        ).distinct()
    if job:
        search_query = search_query.filter(
            shift__job__name__icontains=job
        ).distinct()
    return search_query

