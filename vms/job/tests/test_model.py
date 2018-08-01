# third party

# Django
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.test.testcases import TestCase

# local Django
from job.models import Job
from event.models import Event
from pom.pages.jobDetailsPage import JobDetailsPage
from shift.utils import create_job_with_details, create_event_with_details


class JobModelTests(TestCase):

    def setUp(self):
        self.event = self.create_event()

    def tearDown(self):
        pass

    @staticmethod
    def create_event():
        event = ['event-name', '2050-05-24', '2050-05-28']
        created_event = create_event_with_details(event)
        return created_event

    def create_job(self):
        job = ['job-name', '2050-05-25', '2050-05-26', 'job-description', self.event]
        created_job = create_job_with_details(job)
        return created_job

    def test_valid_model_create(self):
        job = ['job-name', '2050-05-25', '2050-05-26', 'job-description', self.event]
        created_job = create_job_with_details(job)

        # Check database for instance creation
        self.assertNotEqual(len(Job.objects.all()), 0)

        event_in_db = Event.objects.get(Q(name='event-name'))
        # Check if event name is correct
        self.assertEqual(event_in_db.name, self.event.name)

        job_in_db = Job.objects.get(Q(event=event_in_db))
        # Check if job details are correct
        self.assertEqual(job_in_db.name, job[0])
        self.assertEqual(str(job_in_db.start_date), job[1])
        self.assertEqual(str(job_in_db.end_date), job[2])
        self.assertEqual(job_in_db.description, job[3])

    def test_invalid_model_create(self):
        job = ['job~name', '2016-05-25', '2016-05-26', 'job-description', self.event]
        created_job = create_job_with_details(job)

        self.assertRaisesRegexp(ValidationError,
                                JobDetailsPage.ENTER_VALID_VALUE,
                                created_job.full_clean)

        # Check database for instance creation
        self.assertNotEqual(len(Job.objects.all()), 0)

    def test_model_edit_with_valid_values(self):
        job = self.create_job()

        # Check db for instance creation
        self.assertEqual(len(Job.objects.all()), 1)

        event_in_db = Event.objects.get(Q(name='event-name'))
        job_in_db = Job.objects.get(Q(event=event_in_db))
        # Check if correct job retrieved
        self.assertEqual(job_in_db.name, job.name)

        # Edit job
        job_in_db.name = 'new-job-name'
        job_in_db.save()

        job_in_db = Job.objects.get(Q(event=event_in_db))
        # Check if save is success
        self.assertEqual(job_in_db.name, 'new-job-name')
        self.assertEqual(len(Job.objects.all()), 1)

    def test_model_edit_with_invalid_values(self):
        job = ['job-name', '2016-05-25', '2016-05-26', 'job-description', self.event]
        created_job = create_job_with_details(job)

        # Check instance created
        self.assertEqual(len(Job.objects.all()), 1)

        job_in_db = Job.objects.get(Q(name='job-name'))
        # Check if correctly stored
        self.assertEqual(job_in_db.name, created_job.name)

        # Edit job
        job_in_db.name = 'new~job~name'
        job_in_db.save()

        self.assertRaisesRegexp(ValidationError,
                                JobDetailsPage.ENTER_VALID_VALUE,
                                job_in_db.full_clean)

        # Check database for instance creation
        self.assertNotEqual(len(Job.objects.all()), 0)

    def test_model_delete(self):
        job = self.create_job()

        # Check db for instance creation
        self.assertEqual(len(Job.objects.all()), 1)

        event_in_db = Event.objects.get(Q(name='event-name'))
        job_in_db = Job.objects.get(Q(event=event_in_db))
        # Check if correct job retrieved
        self.assertEqual(job_in_db.name, job.name)

        # Delete job
        job_in_db.delete()

        # Check if delete is successful
        self.assertEqual(len(Job.objects.all()), 0)

    def test_model_representation(self):
        self.create_job()

        # Check db for instance creation
        self.assertEqual(len(Job.objects.all()), 1)

        event_in_db = Event.objects.get(Q(name='event-name'))
        job_in_db = Job.objects.get(Q(event=event_in_db))

        # Check __str__
        self.assertEqual(str(job_in_db), job_in_db.name)
