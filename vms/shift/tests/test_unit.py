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

    def setUp(self):
        self.event = ShiftModelTests.create_event()
        self.job = self.create_job()

    def tearDown(self):
        pass

    @staticmethod
    def create_event():
        event = ['event-name', '2050-05-24', '2050-05-28']
        created_event = create_event_with_details(event)
        return created_event

    def create_job(self):
        job = ['job-name', '2050-05-24', '2050-05-28', 'job-description', self.event]
        created_job = create_job_with_details(job)
        return created_job

    def create_valid_shift(self):
        shift = ['2050-05-24', '09:00:00', '12:00:00', '10', self.job]
        created_shift = create_shift_with_details(shift)
        return created_shift

    def create_invalid_shift(self):
        shift = ['2050-05-29', '12:00:00', '09:00:00', '10', self.job]
        created_shift = create_shift_with_details(shift)
        return created_shift

    def test_valid_model_create(self):
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
        # Can't check unless a clean function is defined in forms.
        pass

    def test_model_edit_with_valid_values(self):
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
        shift = self.create_valid_shift()

        # Check database for shift creation
        self.assertEqual(len(Shift.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        # Check correctness
        self.assertEqual(str(shift_in_db), 'job-name - 2050-05-24')


class VolunteerShiftModelTests(TestCase):

    def setUp(self):
        self.event = self.create_event()
        self.job = self.create_job()

    def tearDown(self):
        pass

    @staticmethod
    def create_event():
        event = ['event-name', '2050-05-24', '2050-05-28']
        created_event = create_event_with_details(event)
        return created_event

    def create_job(self):
        job = ['job-name', '2050-05-24', '2050-05-28', 'job-description', self.event]
        created_job = create_job_with_details(job)
        return created_job

    def create_shift(self):
        shift = ['2050-05-24', '09:00:00', '12:00:00', '10', self.job]
        created_shift = create_shift_with_details(shift)
        return created_shift

    @staticmethod
    def create_valid_volunteer():
        vol = [
            "Goku", "Son", "Goku", "Kame House", "East District",
            "East District", "East District", "9999999999", "idonthave@gmail.com"
        ]
        return create_volunteer_with_details(vol)

    @staticmethod
    def create_invalid_volunteer():
        vol = [
            "Goku~", "Son", "Goku", "Kame House", "East District",
            "East District", "East District", "9999999999", "idonthave@gmail.com"
        ]
        return create_volunteer_with_details(vol)

    @staticmethod
    def create_volunteer_shift(shift, volunteer):
        vol_shift = register_volunteer_for_shift_utility(shift, volunteer)
        return vol_shift

    def test_valid_model_create(self):
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
        shift = self.create_shift()
        volunteer = self.create_invalid_volunteer()

        vol_shift = self.create_volunteer_shift(shift, volunteer)

        # Can't check error until clean method defined in model
        # self.assertRaisesRegexp(ValidationError, BasePage.ENTER_VALID_VALUE, vol_shift.full_clean)

    def test_model_edit_with_valid_values(self):
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
        shift = self.create_shift()
        volunteer = self.create_valid_volunteer()

        vol_shift = self.create_volunteer_shift(shift, volunteer)

        # Check db instance creation
        self.assertEqual(len(VolunteerShift.objects.all()), 1)

        shift_in_db = Shift.objects.get(Q(job=self.job))
        vol_shift_in_db = VolunteerShift.objects.get(Q(shift=shift_in_db))

        # Check correctness
        self.assertEqual(str(vol_shift_in_db), 'job-name - 2050-05-24 - Son')
