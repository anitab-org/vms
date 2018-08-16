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
    """
    Contains database tests for
    - job create with valid and invalid values.
    - job edit with valid and invalid values.
    - job delete.
    - job mode representation.
    """

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        self.event = self.create_event()

    def tearDown(self):
        """
        Method consists of statements to be executed at
        end of each test.
        """
        pass

    @staticmethod
    def create_event():
        """
        Utility function to create an event with valid values.
        :return: Event type object.
        """
        event = {
            'name': 'event-name',
            'start_date': '2050-05-24',
            'end_date': '2050-05-28',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }
        created_event = create_event_with_details(event)
        return created_event

    def create_job(self):
        """
        Utility function to create a job with valid values.
        :return: Job type object.
        """
        job = {
            'name': 'job-name',
            'start_date': '2050-05-25',
            'end_date': '2050-05-26',
            'description': 'job-description',
            'event': self.event
        }
        created_job = create_job_with_details(job)
        return created_job

    def test_valid_model_create(self):
        """
        Test creation of job model with valid values.
        """
        job = {
            'name': 'job-name',
            'start_date': '2050-05-25',
            'end_date': '2050-05-26',
            'description': 'job-description',
            'event': self.event
        }
        created_job = create_job_with_details(job)

        # Check database for instance creation
        self.assertNotEqual(len(Job.objects.all()), 0)

        event_in_db = Event.objects.get(Q(name='event-name'))
        # Check if event name is correct
        self.assertEqual(event_in_db.name, self.event.name)

        job_in_db = Job.objects.get(Q(event=event_in_db))
        # Check if job details are correct
        self.assertEqual(job_in_db.name, job['name'])
        self.assertEqual(str(job_in_db.start_date), job['start_date'])
        self.assertEqual(str(job_in_db.end_date), job['end_date'])
        self.assertEqual(job_in_db.description, job['description'])

    def test_invalid_name_in_model_create(self):
        """
        Database test for model creation with invalid name.
        """
        job = {
            'name': 'job~name',
            'start_date': '2050-05-25',
            'end_date': '2050-05-26',
            'description': 'job-description',
            'event': self.event
        }

        created_job = create_job_with_details(job)
        self.assertRaisesRegexp(ValidationError,
                                JobDetailsPage.ENTER_VALID_VALUE,
                                created_job.full_clean)

    # def test_invalid_start_date_in_model_create(self):
    #     """
    #      Database test for model creation with invalid start date.
    #     """
    #     This test need to be uncommented after clean method is
    #     defined for model.
    #     job = {
    #         'name': 'job-name',
    #         'start_date': '2016-05-25',
    #         'end_date': '2050-05-26',
    #         'description': 'job-description',
    #         'event': self.event
    #     }
    #     created_job = create_job_with_details(job)
    #     self.assertRaisesRegexp(ValidationError,
    #                             JobDetailsPage.ENTER_VALID_VALUE,
    #                             created_job.full_clean)

    # def test_invalid_start_date_in_model_create(self):
    #     """
    #      Database test for model creation with invalid end date.
    #     """
    #     This test need to be uncommented after clean method
    #     is defined for model.
    #     job = {
    #         'name': 'job-name',
    #         'start_date': '2050-05-25',
    #         'end_date': '2016-05-26',
    #         'description': 'job-description',
    #         'event': self.event
    #     }
    #     created_job = create_job_with_details(job)
    #     self.assertRaisesRegexp(ValidationError,
    #                             JobDetailsPage.ENTER_VALID_VALUE,
    #                             created_job.full_clean)

    def test_invalid_description_in_model_create(self):
        """
         Database test for model creation with invalid description.
        """
        job = {
            'name': 'job-name',
            'start_date': '2050-05-25',
            'end_date': '2050-05-26',
            'description': 'job@description@',
            'event': self.event
        }
        created_job = create_job_with_details(job)
        self.assertRaisesRegexp(ValidationError,
                                JobDetailsPage.ENTER_VALID_VALUE,
                                created_job.full_clean)

    def test_model_edit_with_valid_values(self):
        """
        Test edit of job model with valid values.
        """
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
        """
        Test edit of job model with invalid values.
        """
        job = {
            'name': 'job-name',
            'start_date': '2016-05-25',
            'end_date': '2016-05-26',
            'description': 'job-description',
            'event': self.event
        }
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
        """
        Test deletion of registered job model.
        """
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
        """
        Test database representation of registered job.
        """
        self.create_job()

        # Check db for instance creation
        self.assertEqual(len(Job.objects.all()), 1)

        event_in_db = Event.objects.get(Q(name='event-name'))
        job_in_db = Job.objects.get(Q(event=event_in_db))

        # Check __str__
        self.assertEqual(str(job_in_db), job_in_db.name)
