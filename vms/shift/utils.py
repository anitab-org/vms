from event.models import Event
from job.models import Job
from administrator.models import Administrator
from django.contrib.auth.models import User
from shift.models import Shift, VolunteerShift
from volunteer.models import Volunteer
from organization.models import Organization
from cities_light.models import Country

# Contains common functions which need to be frequently called by tests

def clear_objects():
    """
    - Deletes objects from multiple tables
    - Called once all tests in a module are completed
    """
    
    VolunteerShift.objects.all().delete()
    Volunteer.objects.all().delete()
    User.objects.all().delete()
    Shift.objects.all().delete()
    Job.objects.all().delete()
    Event.objects.all().delete()
    Organization.objects.all().delete()

def create_event_with_details(event):
    """
    Creates and returns event with passed name and dates
    """
    e1 = Event(
        name=event[0],
        start_date=event[1],
        end_date=event[2]
        )
    e1.save()
    return e1

def create_job_with_details(job):
    """
    Creates and returns job with passed name and dates
    """
    
    j1 = Job(
        name=job[0],
        start_date=job[1],
        end_date=job[2],
        description=job[3],
        event=job[4]
        )

    j1.save()
    return j1

def create_volunteer_with_details(volunteer):
    """
    Creates and returns volunteer with passed name and dates
    """
    u1 = User.objects.create_user(
        username = volunteer[0],
        password = 'volunteer'
        )
    v1 = Volunteer(
        first_name=volunteer[1],
        last_name=volunteer[2],
        address=volunteer[3],
        city=volunteer[4],
        state=volunteer[5],
        country=volunteer[6],
        phone_number=volunteer[7],
        email=volunteer[8],
        user=u1
        )

    v1.save()
    return v1

def create_shift_with_details(shift):
    """
    Creates and returns shift with passed name and dates
    """
    s1 = Shift(
        date=shift[0],
        start_time=shift[1],
        end_time=shift[2],
        max_volunteers=shift[3],
        job=shift[4]
        )
    s1.save()
    return s1

def log_hours_with_details(volunteer, shift, start, end):
    logged_shift = VolunteerShift.objects.create(
        shift = shift,
        volunteer = volunteer,
        start_time = start,
        end_time = end
        )

    return logged_shift

def create_organization_with_details(org_name):
    org = Organization.objects.create(
        name = org_name)

    return org

def set_shift_location(shift,loc):
    """
    Sets and returns shift with passed location details
    """
    shift.address=loc[0]
    shift.city=loc[1]
    shift.state=loc[2]
    shift.country=loc[3]
    shift.venue=loc[4]
    
    shift.save()
    return shift

def get_report_list(duration_list, report_list, total_hours):
    """
    - Contains steps to generate report list with passes parameters
    - Called frequently by test case in shift unit tests
    """

    for duration in duration_list:
        total_hours += duration
        report = {}
        report["duration"] = duration
        report_list.append(report)

    return (report_list, total_hours)

def create_organization():
    org = Organization.objects.create(
        name = 'DummyOrg')

    return org

def create_country():
    Country.objects.create(
        name_ascii = 'India',
        slug ='india',
        geoname_id = '1269750',
        alternate_names = '',
        name = 'India',
        code2 = 'IN',
        code3 = 'IND',
        continent = 'AS',
        tld = 'in',
        phone = '91')

def create_admin():

    user_1 = User.objects.create_user(
        username = 'admin',
        password = 'admin'
        )

    admin = Administrator.objects.create(
        user = user_1,
        address = 'address',
        city = 'city',
        state = 'state',
        country = 'country',
        phone_number = '9999999999',
        email = 'admin@admin.com',
        unlisted_organization = 'organization')

    return admin

def create_volunteer():

    user_1 = User.objects.create_user(
        username = 'volunteer',
        password = 'volunteer'
        )

    volunteer = Volunteer.objects.create(
        user = user_1,
        address = 'address',
        city = 'city',
        state = 'state',
        country = 'country',
        phone_number = '9999999999',
        email = 'volunteer@volunteer.com',
        unlisted_organization = 'organization')

    return volunteer

def register_event_utility():
    event = Event.objects.create(
        name = 'event',
        start_date = '2016-05-10',
        end_date = '2018-06-16'
        )

    return event

def register_job_utility():
    job = Job.objects.create(
        name = 'job',
        start_date = '2016-05-10',
        end_date = '2017-06-15',
        event = Event.objects.get(name = 'event')
        )

    return job

def register_shift_utility():
    shift = Shift.objects.create(
        date = '2017-06-15',
        start_time = '09:00',
        end_time = '15:00',
        max_volunteers ='6',
        job = Job.objects.get(name = 'job')
        )

    return shift

def register_volunteer_for_shift_utility(shift, volunteer):
        vol_shift = VolunteerShift.objects.create(
            shift=shift,
            volunteer=volunteer)
        return vol_shift

def log_hours_utility():
    VolunteerShift.objects.create(
        shift = Shift.objects.get(job__name = 'job'),
        volunteer = Volunteer.objects.get(user__username = 'volunteer'),
        start_time = '09:00',
        end_time = '12:00'
        )
