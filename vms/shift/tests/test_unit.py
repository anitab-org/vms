# third party
import datetime

# Django
from django.db.models import Q
from django.test.testcases import TestCase

# local Django
from shift.models import Shift, VolunteerShift, Report, EditRequest
from shift.utils import (create_country, create_event_with_details,
                         create_job_with_details, create_city,
                         create_organization_with_details,
                         create_shift_with_details,
                         create_volunteer_with_details,
                         register_volunteer_for_shift_utility,
                         create_edit_request_with_details,
                         log_hours_with_details, create_state,
                         create_report_with_details)
from volunteer.models import Volunteer


class ShiftModelTests(TestCase):
    """
    Contains database tests of Shift model for
    - Creation of model with valid and invalid values.
    - Edit of model with valid and invalid values.
    - Deletion of model
    - Model representation
    """

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        self.event = ShiftModelTests.create_event()
        self.job = self.create_job()

    def tearDown(self):
        """
        Method consists of statements to be executed at
        end of each test.
        """
        pass

    @staticmethod
    def create_event():
        """
        Utility function to create a valid event.
        :return: Event type object
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
        Utility function to create a valid job.
        :return: Job type object
        """
        job = {
            'name': 'job-name',
            'start_date': '2050-05-24',
            'end_date': '2050-05-28',
            'description': 'job-description',
            'event': self.event
        }
        created_job = create_job_with_details(job)
        return created_job

    def create_valid_shift(self):
        """
        Utility function to create a valid shift.
        :return: Shift type object
        """
        shift = {
            'date': '2050-05-24',
            'start_time': '09:00:00',
            'end_time': '12:00:00',
            'max_volunteers': '10',
            'job': self.job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        created_shift = create_shift_with_details(shift)
        return created_shift

    def create_invalid_shift(self):
        """
        Utility function to create an invalid shift.
        :return: Shift type object
        """
        shift = {
            'date': '2050-05-29',
            'start_time': '12:00:00',
            'end_time': '09:00:00',
            'max_volunteers': '10',
            'job': self.job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        created_shift = create_shift_with_details(shift)
        return created_shift

    def test_valid_model_create(self):
        """
        Database test for model creation with valid values.
        """
        shift = self.create_valid_shift()

        # Check database for shift creation
        self.assertEqual(len(Shift.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        # Check correctness
        self.assertEqual(str(shift_in_db.date), shift.date)
        self.assertEqual(str(shift_in_db.start_time), shift.start_time)
        self.assertEqual(str(shift_in_db.end_time), shift.end_time)
        self.assertEqual(str(shift_in_db.max_volunteers), shift.max_volunteers)
        self.assertEqual(shift_in_db.address, shift.address)
        self.assertEqual(shift_in_db.venue, shift.venue)

    def test_invalid_model_create(self):
        """
        Database test for model creation with invalid values.
        """
        # Can't check unless a clean function is defined in forms.
        pass

    def test_model_edit_with_valid_values(self):
        """
        Database test for model edit with valid values.
        """
        shift = self.create_valid_shift()

        # Check database for shift creation
        self.assertEqual(len(Shift.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        # Check correctness
        self.assertEqual(str(shift_in_db.date), shift.date)
        self.assertEqual(str(shift_in_db.start_time), shift.start_time)
        self.assertEqual(str(shift_in_db.end_time), shift.end_time)
        self.assertEqual(str(shift_in_db.max_volunteers), shift.max_volunteers)
        self.assertEqual(shift_in_db.address, shift.address)
        self.assertEqual(shift_in_db.venue, shift.venue)

        shift_in_db.max_volunteers = 11
        shift_in_db.save()

        # Checking no new instance created.
        self.assertEqual(len(Shift.objects.all()), 1)
        shift_in_db = Shift.objects.get(Q(job=self.job))
        # Check correctness
        self.assertEqual(str(shift_in_db.date), shift.date)
        self.assertEqual(str(shift_in_db.start_time), shift.start_time)
        self.assertEqual(str(shift_in_db.end_time), shift.end_time)
        self.assertEqual(str(shift_in_db.max_volunteers), '11')
        self.assertEqual(shift_in_db.address, shift.address)
        self.assertEqual(shift_in_db.venue, shift.venue)

    def test_model_edit_with_invalid_values(self):
        """
        Database test for model edit with invalid values.
        """
        shift = self.create_valid_shift()

        # Check database for shift creation
        self.assertEqual(len(Shift.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        # Check correctness
        self.assertEqual(str(shift_in_db.date), shift.date)
        self.assertEqual(str(shift_in_db.start_time), shift.start_time)
        self.assertEqual(str(shift_in_db.end_time), shift.end_time)
        self.assertEqual(str(shift_in_db.max_volunteers), shift.max_volunteers)

        # Can't check unless a clean function is defined in forms.

    def test_model_delete(self):
        """
        Database test for model deletion.
        """
        shift = self.create_valid_shift()

        # Check database for shift creation
        self.assertEqual(len(Shift.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        # Check correctness
        self.assertEqual(str(shift_in_db.date), shift.date)
        self.assertEqual(str(shift_in_db.start_time), shift.start_time)
        self.assertEqual(str(shift_in_db.end_time), shift.end_time)
        self.assertEqual(str(shift_in_db.max_volunteers), shift.max_volunteers)

        shift_in_db.delete()

        # Check instance deletion.
        self.assertEqual(len(Shift.objects.all()), 0)

    def test_model_representation(self):
        """
        Database test for model representation.
        """
        shift = self.create_valid_shift()

        # Check database for shift creation
        self.assertEqual(len(Shift.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        # Check correctness
        self.assertEqual(str(shift_in_db), 'job-name - 2050-05-24')


class VolunteerShiftModelTests(TestCase):
    """
    Contains database tests of VolunteerShift model for
    - Creation of model with valid and invalid values.
    - Edit of model with valid and invalid values.
    - Deletion of model
    - Model representation
    """
    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        self.event = self.create_event()
        self.job = self.create_job()

    def tearDown(self):
        """
        Method consists of statements to be executed at
        end of each test.
        """
        pass

    @staticmethod
    def create_event():
        """
        Utility function to create a valid event.
        :return: Event type object
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
        Utility function to create a valid job.
        :return: Job type object
        """
        job = {
            'name': 'job-name',
            'start_date': '2050-05-24',
            'end_date': '2050-05-28',
            'description': 'job-description',
            'event': self.event
        }
        created_job = create_job_with_details(job)
        return created_job

    def create_shift(self):
        """
        Utility function to create a valid shift.
        :return: Shift type object
        """
        shift = {
            'date': '2050-05-24',
            'start_time': '09:00:00',
            'end_time': '12:00:00',
            'max_volunteers': '10',
            'job': self.job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        created_shift = create_shift_with_details(shift)
        return created_shift

    @staticmethod
    def create_valid_volunteer():
        """
        Utility function to create a valid volunteer.
        :return: Volunteer type object
        """
        country = create_country()
        state = create_state()
        city = create_city()
        vol = {
            'username': "Goku",
            'first_name': "Son",
            'last_name': "Goku",
            'address': "Kame House",
            'city': city,
            'state': state,
            'country': country,
            'phone_number': "9999999999",
            'email': "idonthave@gmail.com"
        }
        org_name = 'Google'
        org_obj = create_organization_with_details(org_name)
        return create_volunteer_with_details(vol, org_obj)

    @staticmethod
    def create_invalid_volunteer():
        """
        Utility function to create an invalid volunteer.
        :return: Volunteer type object
        """
        country = create_country()
        state = create_state()
        city = create_city()
        vol = {
            'username': "Goku!",
            'first_name': "Son",
            'last_name': "Goku",
            'address': "Kame House",
            'city': city,
            'state': state,
            'country': country,
            'phone_number': "9999999999",
            'email': "idonthave@gmail.com"
        }
        org_name = 'Google'
        org_obj = create_organization_with_details(org_name)
        return create_volunteer_with_details(vol, org_obj)

    @staticmethod
    def create_volunteer_shift(shift, volunteer):
        """
        Utility function to link a shift to a volunteer.
        :return: VolunteerShift type object
        """
        vol_shift = register_volunteer_for_shift_utility(shift, volunteer)
        return vol_shift

    def test_valid_model_create(self):
        """
        Database test for model creation with valid values.
        """
        shift = self.create_shift()
        volunteer = self.create_valid_volunteer()

        vol_shift = self.create_volunteer_shift(shift, volunteer)

        # Check db instance creation
        self.assertEqual(len(VolunteerShift.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        vol_shift_in_db = VolunteerShift.objects.get(Q(shift=shift_in_db))
        # Verify correctness
        self.assertEqual(str(vol_shift_in_db.shift.date), vol_shift.shift.date)
        self.assertEqual(
            str(vol_shift_in_db.shift.start_time),
            vol_shift.shift.start_time
        )
        self.assertEqual(
            str(vol_shift_in_db.shift.end_time),
            vol_shift.shift.end_time
        )
        self.assertEqual(
            vol_shift_in_db.volunteer.first_name,
            vol_shift.volunteer.first_name
        )
        self.assertEqual(
            vol_shift_in_db.volunteer.last_name,
            vol_shift.volunteer.last_name
        )
        self.assertEqual(vol_shift_in_db.report_status, vol_shift.report_status)

    def test_invalid_model_create(self):
        """
        Database test for model creation with invalid values.
        """
        shift = self.create_shift()
        volunteer = self.create_invalid_volunteer()

        vol_shift = self.create_volunteer_shift(shift, volunteer)

        # Can't check error until clean method defined in model
        # self.assertRaisesRegexp(
        #     ValidationError,
        #     BasePage.ENTER_VALID_VALUE, vol_shift.full_clean
        # )

    def test_model_edit_with_valid_values(self):
        """
        Database test for model edit with valid values.
        """
        shift = self.create_shift()
        volunteer = self.create_valid_volunteer()

        vol_shift = self.create_volunteer_shift(shift, volunteer)

        # Check db instance creation
        self.assertEqual(len(VolunteerShift.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        volunteer_in_db = Volunteer.objects.get(Q(first_name='Son'))
        vol_shift_in_db = VolunteerShift.objects.get(Q(shift=shift_in_db))
        # Verify correctness
        self.assertEqual(str(vol_shift_in_db.shift.date), vol_shift.shift.date)
        self.assertEqual(
            str(vol_shift_in_db.shift.start_time),
            vol_shift.shift.start_time
        )
        self.assertEqual(
            str(vol_shift_in_db.shift.end_time),
            vol_shift.shift.end_time
        )
        self.assertEqual(
            vol_shift_in_db.volunteer.first_name,
            vol_shift.volunteer.first_name
        )
        self.assertEqual(
            vol_shift_in_db.volunteer.last_name,
            vol_shift.volunteer.last_name
        )
        self.assertEqual(vol_shift_in_db.report_status, vol_shift.report_status)

        volunteer_in_db.first_name = 'Prince'
        volunteer_in_db.last_name = 'Vegeta'
        volunteer_in_db.save()
        vol_shift_in_db.volunteer = volunteer_in_db
        vol_shift_in_db.report_status = True
        vol_shift_in_db.save()

        # Check single instance
        self.assertEqual(len(VolunteerShift.objects.all()), 1)
        # Verify correctness
        vol_shift_in_db = VolunteerShift.objects.get(Q(shift=shift_in_db))
        # Verify correctness
        self.assertEqual(str(vol_shift_in_db.shift.date), vol_shift.shift.date)
        self.assertEqual(
            str(vol_shift_in_db.shift.start_time),
            vol_shift.shift.start_time
        )
        self.assertEqual(
            str(vol_shift_in_db.shift.end_time),
            vol_shift.shift.end_time
        )
        self.assertEqual(vol_shift_in_db.volunteer.first_name, 'Prince')
        self.assertEqual(vol_shift_in_db.volunteer.last_name, 'Vegeta')
        self.assertEqual(vol_shift_in_db.report_status, True)

    def test_model_edit_with_invalid_values(self):
        """
        Database test for model edit with invalid values.
        """
        shift = self.create_shift()
        volunteer = self.create_valid_volunteer()

        vol_shift = self.create_volunteer_shift(shift, volunteer)

        # Check db instance creation
        self.assertEqual(len(VolunteerShift.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        vol_shift_in_db = VolunteerShift.objects.get(Q(shift=shift_in_db))
        # Verify correctness
        self.assertEqual(str(vol_shift_in_db.shift.date), vol_shift.shift.date)
        self.assertEqual(
            str(vol_shift_in_db.shift.start_time),
            vol_shift.shift.start_time
        )
        self.assertEqual(
            str(vol_shift_in_db.shift.end_time),
            vol_shift.shift.end_time
        )
        self.assertEqual(
            vol_shift_in_db.volunteer.first_name,
            vol_shift.volunteer.first_name
        )
        self.assertEqual(
            vol_shift_in_db.volunteer.last_name,
            vol_shift.volunteer.last_name
        )
        self.assertEqual(vol_shift_in_db.report_status, vol_shift.report_status)

        vol_shift_in_db.volunteer.first_name = 'Son~'

        # Can't check error until clean method defined in model
        # self.assertRaisesRegexp(
        #     ValidationError,
        #     BasePage.ENTER_VALID_VALUE,
        #     vol_shift_in_db.full_clean
        # )

    def test_model_delete(self):
        """
        Database test for model deletion.
        """
        shift = self.create_shift()
        volunteer = self.create_valid_volunteer()

        vol_shift = self.create_volunteer_shift(shift, volunteer)

        # Check db instance creation
        self.assertEqual(len(VolunteerShift.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        vol_shift_in_db = VolunteerShift.objects.get(Q(shift=shift_in_db))
        # Verify correctness
        self.assertEqual(str(vol_shift_in_db.shift.date), vol_shift.shift.date)
        self.assertEqual(
            str(vol_shift_in_db.shift.start_time),
            vol_shift.shift.start_time
        )
        self.assertEqual(
            str(vol_shift_in_db.shift.end_time),
            vol_shift.shift.end_time
        )
        self.assertEqual(
            str(vol_shift_in_db.shift.max_volunteers),
            vol_shift.shift.max_volunteers
        )
        self.assertEqual(
            vol_shift_in_db.volunteer.first_name,
            vol_shift.volunteer.first_name
        )
        self.assertEqual(
            vol_shift_in_db.volunteer.last_name,
            vol_shift.volunteer.last_name
        )
        self.assertEqual(
            vol_shift_in_db.volunteer.email,
            vol_shift.volunteer.email
        )
        self.assertEqual(
            vol_shift_in_db.volunteer.phone_number,
            vol_shift.volunteer.phone_number
        )
        self.assertEqual(vol_shift_in_db.report_status, vol_shift.report_status)

        vol_shift_in_db.delete()
        # Check no instance in db
        self.assertEqual(len(VolunteerShift.objects.all()), 0)

    def test_model_representation(self):
        """
        Database test for model representation.
        """
        shift = self.create_shift()
        volunteer = self.create_valid_volunteer()

        vol_shift = self.create_volunteer_shift(shift, volunteer)

        # Check db instance creation
        self.assertEqual(len(VolunteerShift.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        vol_shift_in_db = VolunteerShift.objects.get(Q(shift=shift_in_db))

        # Check correctness
        self.assertEqual(str(vol_shift_in_db), 'job-name - 2050-05-24 - Son')


class EditRequestModelTests(TestCase):
    """
    Contains database tests of EditRequest model for
    - Creation of model with valid values.
    - Edit of model with valid values.
    - Deletion of model
    - Model representation
    """

    def setUp(self):
        self.event = self.create_event()
        self.job = self.create_job()

    def tearDown(self):
        pass

    @staticmethod
    def create_event():
        """
        Utility function to create a valid event.
        :return: Event type object
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
        Utility function to create a valid job.
        :return: Job type object
        """
        job = {
            'name': 'job-name',
            'start_date': '2015-05-24',
            'end_date': '2015-05-28',
            'description': 'job-description',
            'event': self.event
        }
        created_job = create_job_with_details(job)
        return created_job

    def create_shift(self):
        """
        Utility function to create a valid shift.
        :return: Shift type object
        """
        shift = {
            'date': '2015-05-24',
            'start_time': '09:00:00',
            'end_time': '12:00:00',
            'max_volunteers': '10',
            'job': self.job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        created_shift = create_shift_with_details(shift)
        return created_shift

    @staticmethod
    def create_volunteer():
        """
        Utility function to create a valid volunteer.
        :return: Volunteer type object
        """
        country = create_country()
        state = create_state()
        city = create_city()
        vol = {
            'username': "Goku",
            'first_name': "Son",
            'last_name': "Goku",
            'address': "Kame House",
            'city': city,
            'state': state,
            'country': country,
            'phone_number': "9999999999",
            'email': "idonthave@gmail.com"
        }
        org_name = 'Google'
        org_obj = create_organization_with_details(org_name)
        return create_volunteer_with_details(vol, org_obj)

    @staticmethod
    def create_edit_request(volunteer, shift):
        """
        Utility function to create a valid edit request.
        :param volunteer: The volunteer who makes a request for editing hours
        :param shift: Volunteer's logged shift which is to be edited
        :return: EditRequest type object
        """
        start = datetime.time(hour=9, minute=0, second=0)
        end = datetime.time(hour=12, minute=0, second=0)
        logged_shift = log_hours_with_details(volunteer, shift, start, end)
        start_time = datetime.time(hour=10, minute=0, second=0)
        end_time = datetime.time(hour=12, minute=0, second=0)
        return create_edit_request_with_details(
            start_time, end_time, logged_shift
        )

    def test_valid_model_create(self):
        """
        Database test for model creation with valid values.
        """
        shift = self.create_shift()
        volunteer = self.create_volunteer()

        edit_request = self.create_edit_request(volunteer, shift)

        # Check db instance creation
        self.assertEqual(len(EditRequest.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        vol_shift_in_db = VolunteerShift.objects.get(Q(shift=shift_in_db))
        edit_request_in_db = \
            EditRequest.objects.get(Q(volunteer_shift=vol_shift_in_db))

        # verify correctness
        self.assertEqual(
            edit_request_in_db.volunteer_shift.volunteer.first_name,
            edit_request.volunteer_shift.volunteer.first_name
        )
        self.assertEqual(
            edit_request_in_db.volunteer_shift.volunteer.last_name,
            edit_request.volunteer_shift.volunteer.last_name
        )
        self.assertEqual(
            str(edit_request_in_db.volunteer_shift.shift.start_time),
            edit_request.volunteer_shift.shift.start_time
        )
        self.assertEqual(
            str(edit_request_in_db.volunteer_shift.shift.end_time),
            edit_request.volunteer_shift.shift.end_time
        )
        self.assertEqual(edit_request_in_db.start_time, edit_request.start_time)
        self.assertEqual(edit_request_in_db.end_time, edit_request.end_time)

    def test_model_edit_with_valid_values(self):
        """
        Database test for model edit with valid values.
        """
        shift = self.create_shift()
        volunteer = self.create_volunteer()

        edit_request = self.create_edit_request(volunteer, shift)

        # Check db instance creation
        self.assertEqual(len(EditRequest.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        volunteer_in_db = Volunteer.objects.get(Q(first_name='Son'))
        vol_shift_in_db = VolunteerShift.objects.get(Q(shift=shift_in_db))
        edit_request_in_db = \
            EditRequest.objects.get(Q(volunteer_shift=vol_shift_in_db))

        # verify correctness
        self.assertEqual(
            edit_request_in_db.volunteer_shift.volunteer.first_name,
            edit_request.volunteer_shift.volunteer.first_name
        )
        self.assertEqual(
            edit_request_in_db.volunteer_shift.volunteer.last_name,
            edit_request.volunteer_shift.volunteer.last_name
        )
        self.assertEqual(
            str(edit_request_in_db.volunteer_shift.shift.start_time),
            edit_request.volunteer_shift.shift.start_time
        )
        self.assertEqual(
            str(edit_request_in_db.volunteer_shift.shift.end_time),
            edit_request.volunteer_shift.shift.end_time
        )
        self.assertEqual(edit_request_in_db.start_time, edit_request.start_time)
        self.assertEqual(edit_request_in_db.end_time, edit_request.end_time)

        volunteer_in_db.first_name = 'Prince'
        volunteer_in_db.last_name = 'Vegeta'
        volunteer_in_db.save()
        vol_shift_in_db.volunteer = volunteer_in_db
        vol_shift_in_db.save()
        start = datetime.time(hour=9, minute=30, second=0)
        end = datetime.time(hour=11, minute=30, second=0)
        edit_request_in_db.start_time = start
        edit_request_in_db.end_time = end
        edit_request_in_db.volunteer_shift.volunteer = volunteer_in_db
        edit_request_in_db.save()

        self.assertEqual(len(EditRequest.objects.all()), 1)

        edit_request_in_db = \
            EditRequest.objects.get(Q(volunteer_shift=vol_shift_in_db))

        # verify correctness
        self.assertEqual(
            str(edit_request_in_db.volunteer_shift.shift.start_time),
            edit_request.volunteer_shift.shift.start_time
        )
        self.assertEqual(
            str(edit_request_in_db.volunteer_shift.shift.end_time),
            edit_request.volunteer_shift.shift.end_time
        )
        self.assertEqual(edit_request_in_db.start_time, start)
        self.assertEqual(edit_request_in_db.end_time, end)
        self.assertEqual(
            edit_request_in_db.volunteer_shift.volunteer.first_name,
            'Prince'
        )
        self.assertEqual(
            edit_request_in_db.volunteer_shift.volunteer.last_name,
            'Vegeta'
        )

    def test_model_delete(self):
        """
        Database test for model deletion.
        """
        shift = self.create_shift()
        volunteer = self.create_volunteer()

        edit_request = self.create_edit_request(volunteer, shift)

        # Check db instance creation
        self.assertEqual(len(EditRequest.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        vol_shift_in_db = VolunteerShift.objects.get(Q(shift=shift_in_db))
        edit_request_in_db = \
            EditRequest.objects.get(Q(volunteer_shift=vol_shift_in_db))

        # verify correctness
        self.assertEqual(
            edit_request_in_db.volunteer_shift.volunteer.first_name,
            edit_request.volunteer_shift.volunteer.first_name
        )
        self.assertEqual(
            edit_request_in_db.volunteer_shift.volunteer.last_name,
            edit_request.volunteer_shift.volunteer.last_name
        )
        self.assertEqual(
            str(edit_request_in_db.volunteer_shift.shift.start_time),
            edit_request.volunteer_shift.shift.start_time
        )
        self.assertEqual(
            str(edit_request_in_db.volunteer_shift.shift.end_time),
            edit_request.volunteer_shift.shift.end_time
        )
        self.assertEqual(edit_request_in_db.start_time, edit_request.start_time)
        self.assertEqual(edit_request_in_db.end_time, edit_request.end_time)

        edit_request_in_db.delete()
        self.assertEqual(len(EditRequest.objects.all()), 0)

    def test_model_representation(self):
        """
        Database test for model representation.
        """
        shift = self.create_shift()
        volunteer = self.create_volunteer()

        self.create_edit_request(volunteer, shift)

        # Check db instance creation
        self.assertEqual(len(EditRequest.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        vol_shift_in_db = VolunteerShift.objects.get(Q(shift=shift_in_db))
        edit_request_in_db = \
            EditRequest.objects.get(Q(volunteer_shift=vol_shift_in_db))

        # Check correctness
        self.assertEqual(
            str(edit_request_in_db),
            'job-name - 2015-05-24 - Son Goku'
        )


class ReportVolunteerShiftModelTests(TestCase):

    def setUp(self):
        self.event = self.create_event()
        self.job = self.create_job()

    def tearDown(self):
        pass

    @staticmethod
    def create_event():
        event = {
            'name': 'event-name',
            'start_date': '2015-05-24',
            'end_date': '2015-05-28',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }
        created_event = create_event_with_details(event)
        return created_event

    def create_job(self):
        job = {
            'name': 'job-name',
            'start_date': '2015-05-24',
            'end_date': '2015-05-28',
            'description': 'job-description',
            'event': self.event
        }
        created_job = create_job_with_details(job)
        return created_job

    def create_shift(self):
        shift = {
            'date': '2050-05-24',
            'start_time': '09:00:00',
            'end_time': '12:00:00',
            'max_volunteers': '10',
            'job': self.job,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        created_shift = create_shift_with_details(shift)
        return created_shift

    @staticmethod
    def create_volunteer():
        country = create_country()
        state = create_state()
        city = create_city()
        vol = {
            'username': "Goku",
            'first_name': "Son",
            'last_name': "Goku",
            'address': "Kame House",
            'city': city,
            'state': state,
            'country': country,
            'phone_number': "9999999999",
            'email': "idonthave@gmail.com"
        }
        org_name = 'Google'
        org_obj = create_organization_with_details(org_name)
        return create_volunteer_with_details(vol, org_obj)

    @staticmethod
    def create_report(volunteer, shift):
        start = datetime.time(hour=9, minute=0)
        end = datetime.time(hour=12, minute=0)
        logged_shift = log_hours_with_details(volunteer, shift, start, end)
        return create_report_with_details(volunteer, logged_shift)

    def test_valid_model_create(self):
        shift = self.create_shift()
        volunteer = self.create_volunteer()

        report = self.create_report(volunteer, shift)

        # Check db instance creation
        self.assertEqual(len(Report.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        vol_shift_in_db = VolunteerShift.objects.get(Q(shift=shift_in_db))
        report_in_db = Report.objects.get(Q(volunteer_shifts=vol_shift_in_db))

        # Verify correctness
        self.assertEqual(
            report_in_db.volunteer_shifts.all()[0].shift.start_time,
            report.volunteer_shifts.all()[0].shift.start_time
        )
        self.assertEqual(
            report_in_db.volunteer_shifts.all()[0].shift.end_time,
            report.volunteer_shifts.all()[0].shift.end_time
        )
        self.assertEqual(
            report_in_db.volunteer_shifts.all()[0].report_status,
            report.volunteer_shifts.all()[0].report_status
        )
        self.assertEqual(
            report_in_db.volunteer.first_name,
            report.volunteer.first_name
        )
        self.assertEqual(
            report_in_db.volunteer.last_name,
            report.volunteer.last_name
        )
        self.assertEqual(report_in_db.confirm_status, report.confirm_status)

    def test_model_edit_with_valid_values(self):
        shift = self.create_shift()
        volunteer = self.create_volunteer()

        report = self.create_report(volunteer, shift)

        # Check db instance creation
        self.assertEqual(len(Report.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        volunteer_in_db = Volunteer.objects.get(Q(first_name='Son'))
        vol_shift_in_db = VolunteerShift.objects.get(Q(shift=shift_in_db))
        report_in_db = Report.objects.get(Q(volunteer_shifts=vol_shift_in_db))

        # Verify correctness
        self.assertEqual(
            report_in_db.volunteer_shifts.all()[0].shift.start_time,
            report.volunteer_shifts.all()[0].shift.start_time
        )
        self.assertEqual(
            report_in_db.volunteer_shifts.all()[0].shift.end_time,
            report.volunteer_shifts.all()[0].shift.end_time
        )
        self.assertEqual(
            report_in_db.volunteer.first_name,
            report.volunteer.first_name
        )
        self.assertEqual(
            report_in_db.volunteer.last_name,
            report.volunteer.last_name
        )
        self.assertEqual(report_in_db.confirm_status, report.confirm_status)
        self.assertEqual(
            report_in_db.volunteer_shifts.all()[0].report_status,
            report.volunteer_shifts.all()[0].report_status
        )

        volunteer_in_db.first_name = 'Prince'
        volunteer_in_db.last_name = 'Vegeta'
        volunteer_in_db.save()
        vol_shift_in_db.volunteer = volunteer_in_db
        vol_shift_in_db.report_status = True
        vol_shift_in_db.save()
        report_in_db.volunteer = volunteer_in_db
        report_in_db.volunteer_shifts.clear()
        report_in_db.volunteer_shifts.add(vol_shift_in_db)
        report_in_db.confirm_status = 1
        report_in_db.save()

        self.assertEqual(len(Report.objects.all()), 1)

        report_in_db = Report.objects.get(Q(volunteer_shifts=vol_shift_in_db))
        # Verify correctness
        self.assertEqual(
            report_in_db.volunteer_shifts.all()[0].shift.start_time,
            report.volunteer_shifts.all()[0].shift.start_time
        )
        self.assertEqual(
            report_in_db.volunteer_shifts.all()[0].shift.end_time,
            report.volunteer_shifts.all()[0].shift.end_time
        )
        self.assertEqual(report_in_db.volunteer.first_name, 'Prince')
        self.assertEqual(report_in_db.volunteer.last_name, 'Vegeta')
        self.assertEqual(report_in_db.confirm_status, 1)
        self.assertEqual(
            report_in_db.volunteer_shifts.all()[0].report_status,
            True
        )

    def test_model_delete(self):
        shift = self.create_shift()
        volunteer = self.create_volunteer()

        report = self.create_report(volunteer, shift)

        # Check db instance creation
        self.assertEqual(len(Report.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        vol_shift_in_db = VolunteerShift.objects.get(Q(shift=shift_in_db))
        report_in_db = Report.objects.get(Q(volunteer_shifts=vol_shift_in_db))
        # Verify correctness
        self.assertEqual(
            report_in_db.volunteer_shifts.all()[0].shift.start_time,
            report.volunteer_shifts.all()[0].shift.start_time
        )
        self.assertEqual(
            report_in_db.volunteer_shifts.all()[0].shift.end_time,
            report.volunteer_shifts.all()[0].shift.end_time
        )
        self.assertEqual(
            report_in_db.volunteer_shifts.all()[0].report_status,
            report.volunteer_shifts.all()[0].report_status
        )
        self.assertEqual(
            report_in_db.volunteer.first_name,
            report.volunteer.first_name
        )
        self.assertEqual(
            report_in_db.volunteer.last_name,
            report.volunteer.last_name
        )
        self.assertEqual(report_in_db.confirm_status, report.confirm_status)

        report_in_db.delete()
        # Check no instance in db
        self.assertEqual(len(Report.objects.all()), 0)

    def test_model_representation(self):
        shift = self.create_shift()
        volunteer = self.create_volunteer()

        self.create_report(volunteer, shift)

        # Check db instance creation
        self.assertEqual(len(Report.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        vol_shift_in_db = VolunteerShift.objects.get(Q(shift=shift_in_db))
        report_in_db = Report.objects.get(Q(volunteer_shifts=vol_shift_in_db))

        # Check correctness
        self.assertEqual(str(report_in_db), 'Report object')
