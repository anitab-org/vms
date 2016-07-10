from event.models import Event
from job.models import Job
from django.contrib.auth.models import User
from shift.models import Shift, VolunteerShift
from volunteer.models import Volunteer
from organization.models import Organization

# Contains common functions which need to be called by tests

def clear_objects():
    
    VolunteerShift.objects.all().delete()
    Volunteer.objects.all().delete()
    User.objects.all().delete()
    Shift.objects.all().delete()
    Job.objects.all().delete()
    Event.objects.all().delete()
    Organization.objects.all().delete()

def create_event_with_details(event):
    e1 = Event(
        name=event[0],
        start_date=event[1],
        end_date=event[2]
        )
    e1.save()
    return e1

def create_job_with_details(job):
    
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
    u1 = User.objects.create_user(volunteer[0])
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
    s1 = Shift(
        date=shift[0],
        start_time=shift[1],
        end_time=shift[2],
        max_volunteers=shift[3],
        job=shift[4]
        )
    s1.save()
    return s1

def get_report_list(duration_list, report_list, total_hours):

	for duration in duration_list:
		total_hours += duration
		report = {}
		report["duration"] = duration
		report_list.append(report)

	return (report_list, total_hours)
