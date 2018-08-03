# third party
from cities_light.models import Country, Region, City

# Django
from django.contrib.auth.models import User

# local Django
from administrator.models import Administrator
from event.models import Event
from job.models import Job
from shift.models import Shift, VolunteerShift, EditRequest, Report
from shift.services import calculate_duration
from volunteer.models import Volunteer
from organization.models import Organization

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


def create_edit_request_with_details(start_time, end_time, logged_shift):
    er1 = EditRequest(volunteer_shift=logged_shift, start_time=start_time, end_time=end_time)
    er1.save()
    return er1


def create_event_with_details(event):
    """
    Creates and returns event with passed name and dates
    """ 
    if len(event) == 4:
       e1 = Event(name=event[0], start_date=event[1], end_date=event[2], description=event[3])
    else: 
       e1 = Event(name=event[0], start_date=event[1], end_date=event[2])
    e1.save()
    return e1


def create_report_with_details(vol, logged_shift):
     total_hours = calculate_duration(logged_shift.start_time, logged_shift.end_time)
     r1 = Report.objects.create(volunteer=vol, total_hrs=total_hours)
     r1.volunteer_shifts.add(logged_shift)
     r1.save()
     return r1


def create_job_with_details(job):
    """
    Creates and returns job with passed name and dates
    """

    j1 = Job(
        name=job[0],
        start_date=job[1],
        end_date=job[2],
        description=job[3],
        event=job[4])

    j1.save()
    return j1


def create_volunteer_with_details(volunteer, org_obj):
    """
    Creates and returns volunteer with passed name and dates
    """
    u1 = User.objects.create_user(username=volunteer[0], password='volunteer')
    v1 = Volunteer(
        first_name=volunteer[1],
        last_name=volunteer[2],
        address=volunteer[3],
        city=volunteer[4],
        state=volunteer[5],
        country=volunteer[6],
        phone_number=volunteer[7],
        email=volunteer[8],
        user=u1,
        organization=org_obj)
    v1.save()
    return v1


def create_volunteer_with_details_dynamic_password(volunteer):
    """
    Creates and returns volunteer with passed name and dates
    """
    u1 = User.objects.create_user(username=volunteer[0], password=volunteer[1])
    v1 = Volunteer(
        email=volunteer[2],
        first_name=volunteer[3],
        last_name=volunteer[4],
        address=volunteer[5],
        city=volunteer[6],
        state=volunteer[7],
        country=volunteer[8],
        phone_number=volunteer[9],
        user=u1
    )

    v1.save()
    return v1


def create_shift_with_details(shift):
    """
    Creates and returns shift with passed name and dates
    """
    if len(shift) == 5:
        s1 = Shift(
            date=shift[0],
            start_time=shift[1],
            end_time=shift[2],
            max_volunteers=shift[3],
            job=shift[4])
    elif len(shift) == 7:
        s1 = Shift(
            date=shift[0],
            start_time=shift[1],
            end_time=shift[2],
            max_volunteers=shift[3],
            job=shift[4],
            address=shift[5],
            venue=shift[6]
        )
    s1.save()
    return s1


def log_hours_with_details(volunteer, shift, start, end):
    logged_shift = VolunteerShift.objects.create(
        shift=shift, volunteer=volunteer, start_time=start, end_time=end)

    return logged_shift


def create_organization_with_details(org_name):
    org = Organization.objects.create(name=org_name)

    return org


def set_shift_location(shift, loc):
    """
    Sets and returns shift with passed location details
    """
    shift.address = loc[0]
    shift.city = loc[1]
    shift.state = loc[2]
    shift.country = loc[3]
    shift.venue = loc[4]

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


def get_country_by_name(country_name):
    country = Country.objects.get(name=country_name)
    return country


def get_state_by_name(state_name):
    state = Region.objects.get(name=state_name)
    return state


def get_city_by_name(city_name):
    city = City.objects.get(name=city_name)
    return city


def create_organization():
    org = Organization.objects.create(name='DummyOrg')

    return org


def create_country():
    country = Country.objects.create(
        name_ascii='India',
        slug='india',
        geoname_id='1269750',
        alternate_names='',
        name='India',
        code2='IN',
        code3='IND',
        continent='AS',
        tld='in',
        phone='91')
    return country


def create_state():
    country = Country.objects.get(name='India')
    state = Region.objects.create(
        name_ascii = "Uttarakhand",
        slug='uttarakhand',
        geoname_id='1444366',
        alternate_names='',
        name='Uttarakhand',
        geoname_code='39',
        country=country
        )
    return state


def create_city():
    country = Country.objects.get(name='India')
    state = Region.objects.get(name='Uttarakhand')
    city = City.objects.create(
        name_ascii = 'Roorkee',
        slug='roorkee',
        geoname_id=1258044,
        alternate_names='',
        name='Roorkee',
        region=state,
        country=country,
        )
    return city


def create_other_city():
    country = Country.objects.get(name='India')
    state = Region.objects.get(name='Uttarakhand')
    city = City.objects.create(
        name_ascii = 'Mussoorie',
        slug='mussoorie',
        geoname_id=1262374,
        alternate_names='',
        name='Mussoorie',
        region=state,
        country=country,
        )
    return city


def create_second_country():
    country = Country.objects.create(
        name_ascii='United States',
        slug='united states',
        geoname_id='6252001',
        alternate_names='',
        name='United States',
        code2='US',
        code3='USA',
        continent='NA',
        tld='us',
        phone='1')
    return country


def create_second_state():
    country = Country.objects.get(name='United States')
    state = Region.objects.create(
        name_ascii = "Washington",
        slug='washington',
        geoname_id='5815135',
        alternate_names='',
        name='Washington',
        geoname_code='WA',
        country=country)
    return state


def create_second_city():
    country = Country.objects.get(name='United States')
    state = Region.objects.get(name='Washington')
    city = City.objects.create(
        name_ascii = 'Bothell',
        slug='bothell',
        geoname_id=5787829,
        alternate_names='',
        name='Bothell',
        region=state,
        country=country,
        )
    return city


def create_admin_with_unlisted_org():
    user_1 = User.objects.create_user(username='admin', password='admin')
    org_1 = Organization.objects.create(name='organization', approved_status=0)
    org_1.save()
    country = create_second_country()
    state = create_second_state()
    city = create_second_city()
    admin = Administrator.objects.create(
        user=user_1,
        address='address',
        city=city,
        state=state,
        country=country,
        phone_number='9999999999',
        email='admin@admin.com',
        organization=org_1)

    return admin


def create_admin():
    user_1 = User.objects.create_user(username='admin', password='admin')
    org_name = 'organization'
    org_1 = create_organization_with_details(org_name)
    country = create_second_country()
    state = create_second_state()
    city = create_second_city()
    admin = Administrator.objects.create(
        user=user_1,
        address='address',
        city=city,
        state=state,
        country=country,
        phone_number='9999999999',
        email='admin@admin.com',
        first_name='Son',
        last_name='Goku',
        organization=org_1)

    return admin


def create_volunteer():
    user_1 = User.objects.create_user(
        username='volunteer', password='volunteer')
    org_name = 'volunteerorganization'
    org_1 = create_organization_with_details(org_name)
    country = create_country()
    state = create_state()
    city = create_city()
    volunteer = Volunteer.objects.create(
        user=user_1,
        address='address',
        city=city,
        state=state,
        country=country,
        phone_number='9999999999',
        email='volunteer@volunteer.com',
        first_name='Prince',
        last_name='Vegeta',
        organization=org_1)

    return volunteer


def register_past_event_utility():
    event = Event.objects.create(
        name='event', start_date='2012-05-10', end_date='2012-06-16')

    return event


def register_past_job_utility():
    job = Job.objects.create(
        name='job',
        start_date='2012-05-10',
        end_date='2012-06-15',
        event=Event.objects.get(name='event'))

    return job


def register_past_shift_utility():
    shift = Shift.objects.create(
        date='2012-06-15',
        start_time='09:00',
        end_time='15:00',
        max_volunteers='6',
        job=Job.objects.get(name='job'))

    return shift


def register_event_utility():
    event = Event.objects.create(
        name='event', start_date='2050-05-10', end_date='2050-06-16')

    return event


def register_job_utility():
    job = Job.objects.create(
        name='job',
        start_date='2050-05-10',
        end_date='2050-06-15',
        event=Event.objects.get(name='event'))

    return job


def register_shift_utility():
    shift = Shift.objects.create(
        date='2050-06-15',
        start_time='09:00',
        end_time='15:00',
        max_volunteers='6',
        job=Job.objects.get(name='job'))

    return shift


def register_volunteer_for_shift_utility(shift, volunteer):
    vol_shift = VolunteerShift.objects.create(shift=shift, volunteer=volunteer)
    return vol_shift


def log_hours_utility():
    VolunteerShift.objects.create(
        shift=Shift.objects.get(job__name='job'),
        volunteer=Volunteer.objects.get(user__username='volunteer'),
        start_time='09:00',
        end_time='12:00')
