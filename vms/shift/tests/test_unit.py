# third party

# Django
from django.db.models import Q
from django.test.testcases import TestCase

# local Django
from shift.models import Shift, VolunteerShift
from shift.utils import create_event_with_details, create_job_with_details, create_shift_with_details, \
    create_volunteer_with_details, register_volunteer_for_shift_utility
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
        event = ['event-name', '2050-05-24', '2050-05-28']
        created_event = create_event_with_details(event)
        return created_event

    def create_job(self):
        """
        Utility function to create a valid job.
        :return: Job type object
        """
        job = ['job-name', '2050-05-24', '2050-05-28', 'job-description', self.event]
        created_job = create_job_with_details(job)
        return created_job

    def create_valid_shift(self):
        """
        Utility function to create a valid shift.
        :return: Shift type object
        """
        shift = ['2050-05-24', '09:00:00', '12:00:00', '10', self.job]
        created_shift = create_shift_with_details(shift)
        return created_shift

    def create_invalid_shift(self):
        """
        Utility function to create an invalid shift.
        :return: Shift type object
        """
        shift = ['2050-05-29', '12:00:00', '09:00:00', '10', self.job]
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
        event = ['event-name', '2050-05-24', '2050-05-28']
        created_event = create_event_with_details(event)
        return created_event

    def create_job(self):
        """
        Utility function to create a valid job.
        :return: Job type object
        """
        job = ['job-name', '2050-05-24', '2050-05-28', 'job-description', self.event]
        created_job = create_job_with_details(job)
        return created_job

    def create_shift(self):
        """
        Utility function to create a valid shift.
        :return: Shift type object
        """
        shift = ['2050-05-24', '09:00:00', '12:00:00', '10', self.job]
        created_shift = create_shift_with_details(shift)
        return created_shift

    @staticmethod
    def create_valid_volunteer():
        """
        Utility function to create a valid volunteer.
        :return: Volunteer type object
        """
        vol = [
            "Goku", "Son", "Goku", "Kame House", "East District",
            "East District", "East District", "9999999999", "idonthave@gmail.com"
        ]
        return create_volunteer_with_details(vol)

    @staticmethod
    def create_invalid_volunteer():
        """
        Utility function to create an invalid volunteer.
        :return: Volunteer type object
        """
        vol = [
            "Goku~", "Son", "Goku", "Kame House", "East District",
            "East District", "East District", "9999999999", "idonthave@gmail.com"
        ]
        return create_volunteer_with_details(vol)

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
        self.assertEqual(str(vol_shift_in_db.shift.start_time), vol_shift.shift.start_time)
        self.assertEqual(str(vol_shift_in_db.shift.end_time), vol_shift.shift.end_time)
        self.assertEqual(vol_shift_in_db.volunteer.first_name, vol_shift.volunteer.first_name)
        self.assertEqual(vol_shift_in_db.volunteer.last_name, vol_shift.volunteer.last_name)

    def test_invalid_model_create(self):
        """
        Database test for model creation with invalid values.
        """
        shift = self.create_shift()
        volunteer = self.create_invalid_volunteer()

        vol_shift = self.create_volunteer_shift(shift, volunteer)

        # Can't check error until clean method defined in model
        # self.assertRaisesRegexp(ValidationError, BasePage.ENTER_VALID_VALUE, vol_shift.full_clean)

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
        self.assertEqual(str(vol_shift_in_db.shift.start_time), vol_shift.shift.start_time)
        self.assertEqual(str(vol_shift_in_db.shift.end_time), vol_shift.shift.end_time)
        self.assertEqual(vol_shift_in_db.volunteer.first_name, vol_shift.volunteer.first_name)
        self.assertEqual(vol_shift_in_db.volunteer.last_name, vol_shift.volunteer.last_name)

        volunteer_in_db.first_name = 'Prince'
        volunteer_in_db.last_name = 'Vegeta'
        volunteer_in_db.save()
        vol_shift_in_db.volunteer = volunteer_in_db
        vol_shift_in_db.save()

        # Check single instance
        self.assertEqual(len(VolunteerShift.objects.all()), 1)
        # Verify correctness
        vol_shift_in_db = VolunteerShift.objects.get(Q(shift=shift_in_db))
        # Verify correctness
        self.assertEqual(str(vol_shift_in_db.shift.date), vol_shift.shift.date)
        self.assertEqual(str(vol_shift_in_db.shift.start_time), vol_shift.shift.start_time)
        self.assertEqual(str(vol_shift_in_db.shift.end_time), vol_shift.shift.end_time)
        self.assertEqual(vol_shift_in_db.volunteer.first_name, 'Prince')
        self.assertEqual(vol_shift_in_db.volunteer.last_name, 'Vegeta')

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
        self.assertEqual(str(vol_shift_in_db.shift.start_time), vol_shift.shift.start_time)
        self.assertEqual(str(vol_shift_in_db.shift.end_time), vol_shift.shift.end_time)
        self.assertEqual(vol_shift_in_db.volunteer.first_name, vol_shift.volunteer.first_name)
        self.assertEqual(vol_shift_in_db.volunteer.last_name, vol_shift.volunteer.last_name)

        vol_shift_in_db.volunteer.first_name = 'Son~'

        # Can't check error until clean method defined in model
        # self.assertRaisesRegexp(ValidationError, BasePage.ENTER_VALID_VALUE, vol_shift_in_db.full_clean)

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
        self.assertEqual(str(vol_shift_in_db.shift.start_time), vol_shift.shift.start_time)
        self.assertEqual(str(vol_shift_in_db.shift.end_time), vol_shift.shift.end_time)
        self.assertEqual(str(vol_shift_in_db.shift.max_volunteers), vol_shift.shift.max_volunteers)
        self.assertEqual(vol_shift_in_db.volunteer.first_name, vol_shift.volunteer.first_name)
        self.assertEqual(vol_shift_in_db.volunteer.last_name, vol_shift.volunteer.last_name)
        self.assertEqual(vol_shift_in_db.volunteer.email, vol_shift.volunteer.email)
        self.assertEqual(vol_shift_in_db.volunteer.phone_number, vol_shift.volunteer.phone_number)

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
