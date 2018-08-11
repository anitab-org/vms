# standard library
import datetime
import unittest
from datetime import date, timedelta

# Django
from django.core.exceptions import ObjectDoesNotExist

# local Django
from shift.models import VolunteerShift
from shift.services import (add_shift_hours, cancel_shift_registration,
                            calculate_total_report_hours, calculate_duration,
                            clear_shift_hours, delete_shift, edit_shift_hours,
                            generate_report, get_shifts_with_open_slots,
                            get_future_shifts_by_volunteer_id, get_shift_by_id,
                            get_shifts_by_job_id, get_shifts_ordered_by_date,
                            get_shift_slots_remaining, send_reminder,
                            get_unlogged_shifts_by_volunteer_id,
                            get_volunteer_shift_by_id, get_volunteer_shifts,
                            get_volunteer_shifts_with_hours,
                            get_volunteers_by_shift_id, register,
                            get_logged_volunteers_by_shift_id, is_signed_up,
                            get_all_volunteer_shifts_with_hours,
                            get_shifts_with_open_slots_for_volunteer,
                            get_report_by_id)
from shift.utils import (create_report_with_details, create_event_with_details,
                         create_organization_with_details, clear_objects,
                         create_job_with_details, get_report_list,
                         create_shift_with_details,
                         create_volunteer_with_details,
                         register_event_utility, register_job_utility,
                         register_shift_utility, set_shift_location,
                         log_hours_with_details, get_country_by_name,
                         get_state_by_name, get_city_by_name)


def setUpModule():
    """
    - Creates objects which can be reused by multiple test classes
    - Creates shifts with limited slots and with multiple slots for use
    """

    global e1
    global j1, j2
    global s1, s2, s3

    event_1 = {
        'name': "Open Source Event",
        'start_date': "2012-9-1",
        'end_date': "2012-11-23",
        'description': 'event-description',
        'address': 'event-address',
        'venue': 'event-venue'
    }
    e1 = create_event_with_details(event_1)

    job_1 = {
        'name': "Software Developer",
        'start_date': "2012-10-22",
        'end_date': "2012-10-30",
        'description': "A software job",
        'event': e1
    }
    job_2 = {
        'name': "Systems Administrator",
        'start_date': "2012-9-1",
        'end_date': "2012-10-26",
        'description': "A systems administrator job",
        'event': e1
    }
    j1 = create_job_with_details(job_1)
    j2 = create_job_with_details(job_2)

    shift_1 = {
        'date': "2012-10-28",
        'start_time': "9:00",
        'end_time': "15:00",
        'max_volunteers': 1,
        'job': j1,
        'address': 'shift-address',
        'venue': 'shift-venue'
    }
    shift_2 = {
        'date': "2012-10-25",
        'start_time': "10:00",
        'end_time': "16:00",
        'max_volunteers': 2,
        'job': j1,
        'address': 'shift-address',
        'venue': 'shift-venue'
    }
    shift_3 = {
        'date': "2012-10-21",
        'start_time': "10:00",
        'end_time': "16:00",
        'max_volunteers': 4,
        'job': j2,
        'address': 'shift-address',
        'venue': 'shift-venue'
    }

    s1 = create_shift_with_details(shift_1)
    s2 = create_shift_with_details(shift_2)
    s3 = create_shift_with_details(shift_3)


def tearDownModule():
    # Destroys all objects created
    clear_objects()


class ShiftTests(unittest.TestCase):
    """
    Contains tests which require
    - only shift objects
    - no objects to be created
    """

    @classmethod
    def setup_test_data(cls):

        cls.e1 = e1
        cls.j2 = j2
        cls.j1 = j1
        cls.s1 = s1
        cls.s2 = s2
        cls.s3 = s3

    @classmethod
    def setUpClass(cls):
        cls.setup_test_data()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_calculate_total_report_hours(self):

        duration_list = [1, 1, 1, 1]
        report_list = []
        total_hours = 0

        report_list, total_hours = get_report_list(duration_list, report_list,
                                                   total_hours)

        self.assertEqual(
            calculate_total_report_hours(report_list), total_hours)

        duration_list = [0.03, 0.023, 0.53, 0.863, 0.23, 0.57]
        report_list = []
        total_hours = 0

        report_list, total_hours = get_report_list(duration_list, report_list,
                                                   total_hours)

        self.assertEqual(
            calculate_total_report_hours(report_list), total_hours)

        duration_list = [12, 24, 23.5, 15.67, 22.453, 3.42]
        report_list = []
        total_hours = 0

        report_list, total_hours = get_report_list(duration_list, report_list,
                                                   total_hours)

        self.assertEqual(
            calculate_total_report_hours(report_list), total_hours)

        duration_list = [5]
        report_list = []
        total_hours = 0

        report_list, total_hours = get_report_list(duration_list, report_list,
                                                   total_hours)

        self.assertEqual(
            calculate_total_report_hours(report_list), total_hours)

        duration_list = [0, 0, 0, 0]
        report_list = []
        total_hours = 0

        report_list, total_hours = get_report_list(duration_list, report_list,
                                                   total_hours)

        self.assertEqual(
            calculate_total_report_hours(report_list), total_hours)

    def test_calculate_duration(self):
        start_time = datetime.time(hour=1, minute=0)
        end_time = datetime.time(hour=2, minute=0)
        delta_time_hours = 1
        self.assertEqual(
            calculate_duration(start_time, end_time), delta_time_hours)

        start_time = datetime.time(hour=1, minute=45)
        end_time = datetime.time(hour=2, minute=0)
        delta_time_hours = 0.25
        self.assertEqual(
            calculate_duration(start_time, end_time), delta_time_hours)

        start_time = datetime.time(hour=1, minute=0)
        end_time = datetime.time(hour=13, minute=0)
        delta_time_hours = 12
        self.assertEqual(
            calculate_duration(start_time, end_time), delta_time_hours)

        start_time = datetime.time(hour=1, minute=0)
        end_time = datetime.time(hour=1, minute=0)
        delta_time_hours = 0
        self.assertEqual(
            calculate_duration(start_time, end_time), delta_time_hours)

        start_time = datetime.time(hour=22, minute=0)
        end_time = datetime.time(hour=1, minute=0)
        delta_time_hours = 3
        self.assertEqual(
            calculate_duration(start_time, end_time), delta_time_hours)

        start_time = datetime.time(hour=13, minute=0)
        end_time = datetime.time(hour=1, minute=0)
        delta_time_hours = 12
        self.assertEqual(
            calculate_duration(start_time, end_time), delta_time_hours)

    def test_get_shift_by_id(self):
        """ Uses shifts s1 and s2 """

        # test typical cases
        self.assertIsNotNone(get_shift_by_id(self.s1.id))
        self.assertIsNotNone(get_shift_by_id(self.s2.id))

        self.assertEqual(get_shift_by_id(self.s1.id), self.s1)
        self.assertEqual(get_shift_by_id(self.s2.id), self.s2)

        # test non-existant cases
        self.assertIsNone(get_shift_by_id(1000))
        self.assertIsNone(get_shift_by_id(2000))

    def test_get_shifts_by_job_id(self):
        """
        Test get_shifts_by_job_id(j_id)
        Uses job j1
        """
        job_1_shifts = get_shifts_by_job_id(j1.id)
        job_2_shifts = get_shifts_by_job_id(j2.id)

        self.assertIsNotNone(get_shifts_by_job_id(j1.id))
        self.assertIsNotNone(get_shifts_by_job_id(j2.id))

        self.assertEqual(len(job_1_shifts), 2)
        self.assertEqual(len(job_2_shifts), 1)

    def test_get_shifts_ordered_by_date(self):
        """ Uses shifts s1 and s2 """

        # test typical case
        shift_list = get_shifts_ordered_by_date(self.j1.id)
        self.assertIsNotNone(shift_list)
        self.assertNotEqual(shift_list, False)
        self.assertEqual(len(shift_list), 2)
        self.assertIn(self.s1, shift_list)
        self.assertIn(self.s2, shift_list)

        # test order
        self.assertEqual(shift_list[0], self.s2)
        self.assertEqual(shift_list[1], self.s1)


class ShiftWithVolunteerTest(unittest.TestCase):
    """
    Contains tests which require volunteer object
    """

    @classmethod
    def setup_test_data(cls):

        cls.e1 = e1
        cls.j1 = j1
        cls.j2 = j2
        cls.s1 = s1
        cls.s2 = s2
        cls.s3 = s3

        country_name = 'United States'
        country = get_country_by_name(country_name)
        state_name = 'Washington'
        state = get_state_by_name(state_name)
        city_name = 'Bothell'
        city = get_city_by_name(city_name)
        # Create volunteers who will register for the shifts
        volunteer_1 = {
            'username': 'Yoshi',
            'first_name': "Yoshi",
            'last_name': "Turtle",
            'address': "Mario Land",
            'city': city,
            'state': state,
            'country': country,
            'phone_number': "2374983247",
            'email': "yoshi@nintendo.com"
        }
        volunteer_2 = {
            'username': 'John',
            'first_name': "John",
            'last_name': "Doe",
            'address': "7 Alpine Street",
            'city': city,
            'state': state,
            'country': country,
            'phone_number': "23454545",
            'email': "john@test.com"
        }
        volunteer_3 = {
            'username': 'Ash',
            'first_name': "Ash",
            'last_name': "Ketchum",
            'address': "Pallet Town",
            'city': city,
            'state': state,
            'country': country,
            'phone_number': "23454545",
            'email': "ash@pikachu.com"
        }

        org_name = 'Locale'
        cls.org_obj = create_organization_with_details(org_name)
        cls.v1 = create_volunteer_with_details(volunteer_1, cls.org_obj)
        cls.v2 = create_volunteer_with_details(volunteer_2, cls.org_obj)
        cls.v3 = create_volunteer_with_details(volunteer_3, cls.org_obj)

    @classmethod
    def setUpClass(cls):
        cls.setup_test_data()

    def tearDown(self):
        # remove all registered volunteers
        VolunteerShift.objects.all().delete()

    def test_get_report_by_id(self):
        start = datetime.time(hour=10, minute=0)
        end = datetime.time(hour=12, minute=0)
        logged_shift_1 = log_hours_with_details(self.v1, self.s1, start, end)
        r1 = create_report_with_details(self.v1, logged_shift_1)

        logged_shift_2 = log_hours_with_details(self.v2, self.s2, start, end)
        r2 = create_report_with_details(self.v2, logged_shift_2)

        self.assertIsNotNone(get_report_by_id(r1.id))
        self.assertIsNotNone(get_report_by_id(r2.id))

        self.assertEqual(get_report_by_id(r1.id), r1)
        self.assertEqual(get_report_by_id(r2.id), r2)

        # test non-existant cases
        self.assertIsNone(get_report_by_id(100))
        self.assertIsNone(get_report_by_id(200))

    def test_get_shifts_with_open_slots_for_volunteer(self):
        """ Uses volunteer v1, v2 """

        register(self.v1.id, self.s2.id)
        register(self.v2.id, self.s1.id)

        open_slots_1 = get_shifts_with_open_slots_for_volunteer(
            self.j1.id, self.v1.id)
        open_slots_2 = get_shifts_with_open_slots_for_volunteer(
            self.j2.id, self.v1.id)

        self.assertIsNotNone(open_slots_1)
        self.assertIsNotNone(open_slots_2)
        self.assertEqual(len(open_slots_1), 0)
        self.assertEqual(len(open_slots_2), 1)

        self.assertEqual(self.s3.id, open_slots_2[0]["id"])

    def test_get_volunteer_report(self):

        # register volunteer for 2 shifts, log hours for one
        register(self.v1.id, self.s1.id)
        register(self.v1.id, self.s3.id)

        start_time = datetime.time(hour=9, minute=0)
        end_time = datetime.time(hour=10, minute=0)
        add_shift_hours(self.v1.id, self.s1.id, start_time, end_time)

        volunteer_shift_list_1 = get_volunteer_shifts(
            self.v1.id, self.e1.name, self.j1.name,
            "2012-10-22", "2012-10-30"
        )
        report_1 = generate_report(volunteer_shift_list_1)

        volunteer_shift_list_2 = get_volunteer_shifts(
            self.v1.id, self.e1.name, self.j2.name,
            "2012-9-1", "2012-10-26"
        )
        report_2 = generate_report(volunteer_shift_list_2)

        # verify that report for logged shift appears
        self.assertEqual(len(report_1), 1)
        self.assertEqual(len(report_2), 0)
        self.assertEqual(self.e1.name, report_1[0]["event_name"])
        self.assertEqual(self.j1.name, report_1[0]["job_name"])

        # commented out due to bug #327
        # self.assertEqual(start_time, report_1[0]["logged_start_time"])
        # self.assertEqual(end_time, report_1[0]["logged_end_time"])
        # self.assertEqual(1.0, report_1[0]["duration"])

    def test_add_shift_hours(self):
        """ Uses shifts s1, s2, s3 and volunteers v1,v2,v3 """

        # register will return an exception on error
        # (such as when invalid parameters are passed)
        # if an exception does get raised, this test will automatically fail
        register(self.v1.id, self.s1.id)
        self.assertIsNotNone(
            VolunteerShift.objects.get(
                volunteer_id=self.v1.id, shift_id=self.s1.id))

        register(self.v1.id, self.s2.id)
        self.assertIsNotNone(
            VolunteerShift.objects.get(
                volunteer_id=self.v1.id, shift_id=self.s2.id))

        register(self.v1.id, self.s3.id)
        self.assertIsNotNone(
            VolunteerShift.objects.get(
                volunteer_id=self.v1.id, shift_id=self.s3.id))

        start_time = datetime.time(hour=9, minute=0)
        end_time = datetime.time(hour=10, minute=0)
        add_shift_hours(self.v1.id, self.s1.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
            volunteer_id=self.v1.id, shift_id=self.s1.id)
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        start_time = datetime.time(hour=10, minute=0)
        end_time = datetime.time(hour=12, minute=0)
        add_shift_hours(self.v1.id, self.s2.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
            volunteer_id=self.v1.id, shift_id=self.s2.id)
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        start_time = datetime.time(hour=5, minute=0)
        end_time = datetime.time(hour=6, minute=0)
        add_shift_hours(self.v1.id, self.s3.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
            volunteer_id=self.v1.id, shift_id=self.s3.id)
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

    def test_cancel_shift_registration(self):
        """ Uses shifts s1, s2, s3 and volunteers v1,v2 """

        # test cases when try to cancel when they aren't signed up for a shift
        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(self.v1.id, self.s1.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(self.v1.id, self.s2.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(self.v2.id, self.s1.id)

        # register volunteers to shifts
        register(self.v1.id, self.s1.id)
        register(self.v2.id, self.s1.id)
        register(self.v2.id, self.s2.id)

        # test typical cases
        cancel_shift_registration(self.v1.id, self.s1.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(self.v2.id, self.s1.id)

        cancel_shift_registration(self.v2.id, self.s2.id)

    def test_clear_shift_hours(self):
        """ Uses shifts s1, s2, s3 and volunteer v1 """

        register(self.v1.id, self.s1.id)
        self.assertIsNotNone(
            VolunteerShift.objects.get(
                volunteer_id=self.v1.id, shift_id=self.s1.id))

        register(self.v1.id, self.s2.id)
        self.assertIsNotNone(
            VolunteerShift.objects.get(
                volunteer_id=self.v1.id, shift_id=self.s2.id))

        register(self.v1.id, self.s3.id)
        self.assertIsNotNone(
            VolunteerShift.objects.get(
                volunteer_id=self.v1.id, shift_id=self.s3.id))

        start_time = datetime.time(hour=9, minute=0)
        end_time = datetime.time(hour=10, minute=0)
        add_shift_hours(self.v1.id, self.s1.id, start_time, end_time)

        start_time = datetime.time(hour=10, minute=0)
        end_time = datetime.time(hour=12, minute=0)
        add_shift_hours(self.v1.id, self.s2.id, start_time, end_time)

        start_time = datetime.time(hour=5, minute=0)
        end_time = datetime.time(hour=6, minute=0)
        add_shift_hours(self.v1.id, self.s3.id, start_time, end_time)

        clear_shift_hours(self.v1.id, self.s1.id)
        volunteer_shift = VolunteerShift.objects.get(
            volunteer_id=self.v1.id, shift_id=self.s1.id)
        self.assertIsNone(volunteer_shift.start_time)
        self.assertIsNone(volunteer_shift.end_time)

        clear_shift_hours(self.v1.id, self.s2.id)
        volunteer_shift = VolunteerShift.objects.get(
            volunteer_id=self.v1.id, shift_id=self.s2.id)
        self.assertIsNone(volunteer_shift.start_time)
        self.assertIsNone(volunteer_shift.end_time)

        clear_shift_hours(self.v1.id, self.s3.id)
        volunteer_shift = VolunteerShift.objects.get(
            volunteer_id=self.v1.id, shift_id=self.s3.id)
        self.assertIsNone(volunteer_shift.start_time)
        self.assertIsNone(volunteer_shift.end_time)

    def test_edit_shift_hours(self):
        """ Uses shift s1 and volunteer v1 """

        register(self.v1.id, self.s1.id)
        self.assertIsNotNone(
            VolunteerShift.objects.get(
                volunteer_id=self.v1.id, shift_id=self.s1.id))

        start_time = datetime.time(hour=9, minute=0)
        end_time = datetime.time(hour=10, minute=0)
        add_shift_hours(self.v1.id, self.s1.id, start_time, end_time)

        start_time = datetime.time(hour=10, minute=0)
        end_time = datetime.time(hour=11, minute=0)
        edit_shift_hours(self.v1.id, self.s1.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
            volunteer_id=self.v1.id, shift_id=self.s1.id)
        self.assertIsNotNone(volunteer_shift.start_time)
        self.assertIsNotNone(volunteer_shift.end_time)
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        start_time = datetime.time(hour=1, minute=0)
        end_time = datetime.time(hour=4, minute=0)
        edit_shift_hours(self.v1.id, self.s1.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
            volunteer_id=self.v1.id, shift_id=self.s1.id)
        self.assertIsNotNone(volunteer_shift.start_time)
        self.assertIsNotNone(volunteer_shift.end_time)
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        start_time = datetime.time(hour=4, minute=15)
        end_time = datetime.time(hour=12, minute=35)
        edit_shift_hours(self.v1.id, self.s1.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
            volunteer_id=self.v1.id, shift_id=self.s1.id)
        self.assertIsNotNone(volunteer_shift.start_time)
        self.assertIsNotNone(volunteer_shift.end_time)
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        start_time = datetime.time(hour=2, minute=5)
        end_time = datetime.time(hour=4, minute=15)
        edit_shift_hours(self.v1.id, self.s1.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
            volunteer_id=self.v1.id, shift_id=self.s1.id)
        self.assertIsNotNone(volunteer_shift.start_time)
        self.assertIsNotNone(volunteer_shift.end_time)
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        start_time = datetime.time(hour=5, minute=0)
        end_time = datetime.time(hour=5, minute=30)
        edit_shift_hours(self.v1.id, self.s1.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
            volunteer_id=self.v1.id, shift_id=self.s1.id)
        self.assertIsNotNone(volunteer_shift.start_time)
        self.assertIsNotNone(volunteer_shift.end_time)
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

    def test_generate_report(self):
        """ Uses shifts s1, s2 and volunteer v1
        Tests test_generate_report(volunteer_shift_list) """

        # register will return an exception on error
        # (such as when invalid parameters are passed)
        # if an exception does get raised, this test will automatically fail
        start_time = datetime.time(hour=9, minute=0)
        end_time = datetime.time(hour=10, minute=0)
        register(self.v1.id, self.s1.id)
        add_shift_hours(self.v1.id, self.s1.id, start_time, end_time)
        volunteer_shift_1 = VolunteerShift.objects.get(
            volunteer_id=self.v1.id, shift_id=self.s1.id)
        self.assertIsNotNone(volunteer_shift_1)

        register(self.v1.id, self.s2.id)
        add_shift_hours(self.v1.id, self.s2.id, start_time, end_time)
        volunteer_shift_2 = VolunteerShift.objects.get(
            volunteer_id=self.v1.id, shift_id=self.s2.id)
        self.assertIsNotNone(volunteer_shift_2)

        volunteer_shift_list = [volunteer_shift_1, volunteer_shift_2]

        reports = generate_report(volunteer_shift_list)
        self.assertEqual(len(reports), 2)
        self.assertIsNotNone(reports)

    def test_get_all_volunteer_shifts_with_hours(self):
        #  Test get_all_volunteer_shifts_with_hours()
        register(self.v1.id, self.s1.id)
        register(self.v2.id, self.s2.id)

        start_time = datetime.time(hour=9, minute=0)
        end_time = datetime.time(hour=10, minute=0)

        add_shift_hours(self.v1.id, self.s1.id, start_time, end_time)
        hours_list = get_all_volunteer_shifts_with_hours()

        self.assertEqual(len(hours_list), 1)
        self.assertEqual(self.v1.id, hours_list[0].volunteer_id)
        self.assertEqual(self.s1.id, hours_list[0].shift_id)

        self.assertIsNotNone(get_all_volunteer_shifts_with_hours())

    def test_get_shift_slots_remaining(self):
        """ Uses shifts s1, s2, s3
        Tests get_shift_slots_remaining(s_id) """

        register(self.v1.id, self.s1.id)
        register(self.v2.id, self.s3.id)
        register(self.v3.id, self.s3.id)

        slots_s1 = get_shift_slots_remaining(self.s1.id)
        slots_s2 = get_shift_slots_remaining(self.s2.id)
        slots_s3 = get_shift_slots_remaining(self.s3.id)

        self.assertIsNotNone(slots_s1)
        self.assertIsNotNone(slots_s2)
        self.assertIsNotNone(slots_s3)

        self.assertEqual(slots_s1, 0)
        self.assertEqual(slots_s2, 2)
        self.assertEqual(slots_s3, 2)

    def test_get_shifts_with_open_slots(self):
        """ Uses jobs j1, j2
        Tests get_shifts_with_open_slots(j_id) """

        register(self.v1.id, self.s1.id)
        register(self.v2.id, self.s3.id)

        shift_list_1 = get_shifts_with_open_slots(self.j1.id)
        shift_list_2 = get_shifts_with_open_slots(self.j2.id)

        self.assertIsNotNone(shift_list_1)
        self.assertIsNotNone(shift_list_2)
        self.assertEqual(len(shift_list_1), 1)
        self.assertEqual(len(shift_list_2), 1)

        self.assertNotEqual(self.s1.id, shift_list_1[0]["id"])
        self.assertEqual(self.s2.id, shift_list_1[0]["id"])
        self.assertEqual(self.s3.id, shift_list_2[0]["id"])

    def test_get_unlogged_shifts_by_volunteer_id(self):
        """ Uses shifts s1, s2 and volunteer v1 """

        # sign up
        register(self.v1.id, self.s1.id)
        register(self.v1.id, self.s2.id)

        start_time = datetime.time(hour=9, minute=0)
        end_time = datetime.time(hour=10, minute=0)

        add_shift_hours(self.v1.id, self.s1.id, start_time, end_time)

        # test typical case
        shift_list = get_unlogged_shifts_by_volunteer_id(self.v1.id)
        self.assertIsNotNone(shift_list)
        self.assertNotEqual(shift_list, False)
        self.assertEqual(len(shift_list), 1)
        self.assertNotIn(self.s1, shift_list)
        self.assertIn(self.s2, shift_list)
        self.assertNotIn(self.s3, shift_list)

    def test_get_future_shifts_by_volunteer_id(self):
        """ Uses shifts s2, s4 and volunteer v1 """
        register_event_utility()
        register_job_utility()
        s4 = register_shift_utility()
        # sign up
        register(self.v1.id, s4.id)
        register(self.v1.id, self.s2.id)
        start_time = datetime.time(hour=9, minute=0)
        end_time = datetime.time(hour=10, minute=0)
        # test typical case
        shift_list = get_future_shifts_by_volunteer_id(self.v1.id)
        self.assertIsNotNone(shift_list)
        self.assertNotEqual(shift_list, False)
        self.assertEqual(len(shift_list), 1)
        self.assertNotIn(self.s2, shift_list)
        self.assertIn(s4, shift_list)

    def test_get_volunteer_shift_by_id(self):
        """ Uses shifts s1,s2,s3 and volunteers v1,v2"""

        # test cases where signed up
        register(self.v1.id, self.s1.id)
        register(self.v1.id, self.s2.id)
        register(self.v1.id, self.s3.id)

        register(self.v2.id, self.s1.id)
        register(self.v2.id, self.s2.id)
        register(self.v2.id, self.s3.id)

        self.assertEqual(
            get_volunteer_shift_by_id(self.v1.id, self.s1.id),
            VolunteerShift.objects.get(
                volunteer_id=self.v1.id, shift_id=self.s1.id))
        self.assertEqual(
            get_volunteer_shift_by_id(self.v1.id, self.s2.id),
            VolunteerShift.objects.get(
                volunteer_id=self.v1.id, shift_id=self.s2.id))
        self.assertEqual(
            get_volunteer_shift_by_id(self.v1.id, self.s3.id),
            VolunteerShift.objects.get(
                volunteer_id=self.v1.id, shift_id=self.s3.id))

        # self.assertEqual(get_volunteer_shift_by_id(v2.id, s1.id),
        # VolunteerShift.objects.get(volunteer_id=v2.id, shift_id=s1.id))
        # why does this throw DoesNotExist?
        self.assertEqual(
            get_volunteer_shift_by_id(self.v2.id, self.s2.id),
            VolunteerShift.objects.get(
                volunteer_id=self.v2.id, shift_id=self.s2.id))
        self.assertEqual(
            get_volunteer_shift_by_id(self.v2.id, self.s3.id),
            VolunteerShift.objects.get(
                volunteer_id=self.v2.id, shift_id=self.s3.id))

    def test_get_volunteer_shifts_with_hours(self):
        """ Uses volunteers v1 and v2
        Test get_volunteer_shifts_with_hours(v_id) """

        register(self.v1.id, self.s1.id)
        register(self.v1.id, self.s2.id)

        start_time = datetime.time(hour=9, minute=0)
        end_time = datetime.time(hour=10, minute=0)

        add_shift_hours(self.v1.id, self.s1.id, start_time, end_time)

        v1_hours = get_volunteer_shifts_with_hours(self.v1)
        v2_hours = get_volunteer_shifts_with_hours(self.v2)

        self.assertIsNotNone(get_volunteer_shifts_with_hours(self.v1))
        self.assertIsNotNone(get_volunteer_shifts_with_hours(self.v2))

        self.assertEqual(len(v1_hours), 1)
        self.assertEqual(self.s1.id, v1_hours[0].shift_id)
        self.assertEqual(len(v2_hours), 0)

    def test_get_volunteers_by_shift_id(self):
        """ Uses volunteers v1,v2,v3 and shifts s1,s2,s3 """

        # sign up
        register(self.v3.id, self.s1.id)
        register(self.v1.id, self.s1.id)
        register(self.v1.id, self.s3.id)
        register(self.v3.id, self.s3.id)
        register(self.v2.id, self.s3.id)

        # get volunteer lists
        volunteer_list_for_shift_1 = get_volunteers_by_shift_id(self.s1.id)
        volunteer_list_for_shift_2 = get_volunteers_by_shift_id(self.s2.id)
        volunteer_list_for_shift_3 = get_volunteers_by_shift_id(self.s3.id)

        # test typical case
        self.assertEqual(len(volunteer_list_for_shift_1), 1)
        self.assertEqual(len(volunteer_list_for_shift_2), 0)
        self.assertEqual(len(volunteer_list_for_shift_3), 3)

        self.assertIn(self.v3, volunteer_list_for_shift_1)
        self.assertNotIn(self.v1, volunteer_list_for_shift_1)
        self.assertIn(self.v1, volunteer_list_for_shift_3)
        self.assertIn(self.v2, volunteer_list_for_shift_3)
        self.assertIn(self.v3, volunteer_list_for_shift_3)

        # test order
        self.assertEqual(volunteer_list_for_shift_3[0], self.v3)
        self.assertEqual(volunteer_list_for_shift_3[1], self.v2)
        self.assertEqual(volunteer_list_for_shift_3[2], self.v1)

    def test_get_logged_volunteers_by_shift_id(self):
        """ Uses volunteers v1,v2,v3 and shift s3 """

        # sign up
        register(self.v3.id, self.s3.id)
        register(self.v1.id, self.s3.id)
        register(self.v2.id, self.s3.id)

        start_time = datetime.time(hour=1, minute=0)
        end_time = datetime.time(hour=2, minute=0)
        add_shift_hours(self.v1.id, self.s3.id, start_time, end_time)

        start_time = datetime.time(hour=2, minute=0)
        end_time = datetime.time(hour=3, minute=0)
        add_shift_hours(self.v3.id, self.s3.id, start_time, end_time)

        # get volunteer list
        logged_volunteer_list_for_shift = get_logged_volunteers_by_shift_id(
            self.s3.id)

        # test typical case and order
        self.assertEqual(len(logged_volunteer_list_for_shift), 2)
        self.assertEqual(logged_volunteer_list_for_shift[0].volunteer, self.v3)
        self.assertEqual(logged_volunteer_list_for_shift[1].volunteer, self.v1)

    def test_is_signed_up(self):
        """ Uses volunteers v1,v2 and shifts s1,s2,s3 """

        # test cases where not signed up yet
        self.assertFalse(is_signed_up(self.v1.id, self.s1.id))
        self.assertFalse(is_signed_up(self.v1.id, self.s2.id))
        self.assertFalse(is_signed_up(self.v1.id, self.s3.id))

        # test cases where signed up
        register(self.v1.id, self.s1.id)
        register(self.v1.id, self.s2.id)
        register(self.v1.id, self.s3.id)

        self.assertTrue(is_signed_up(self.v1.id, self.s1.id))
        self.assertTrue(is_signed_up(self.v1.id, self.s2.id))
        self.assertTrue(is_signed_up(self.v1.id, self.s3.id))

        # test case where more than one volunteer signs up for the same shift
        self.assertFalse(is_signed_up(self.v2.id, self.s1.id))
        self.assertFalse(is_signed_up(self.v2.id, self.s2.id))
        self.assertFalse(is_signed_up(self.v2.id, self.s3.id))

        register(self.v2.id, self.s2.id)
        register(self.v2.id, self.s3.id)

        self.assertFalse(is_signed_up(self.v2.id, self.s1.id))
        self.assertTrue(is_signed_up(self.v2.id, self.s2.id))
        self.assertTrue(is_signed_up(self.v2.id, self.s3.id))

    def test_register(self):
        """ Uses volunteers v1,v2 and shifts s1,s2,s3 """

        ERROR_CODE_ALREADY_SIGNED_UP = "ERROR_CODE_ALREADY_SIGNED_UP"
        ERROR_CODE_NO_SLOTS_REMAINING = "ERROR_CODE_NO_SLOTS_REMAINING"

        # test typical cases
        register(self.v1.id, self.s1.id)
        self.assertIsNotNone(
            VolunteerShift.objects.get(
                volunteer_id=self.v1.id, shift_id=self.s1.id))

        register(self.v1.id, self.s2.id)
        self.assertIsNotNone(
            VolunteerShift.objects.get(
                volunteer_id=self.v1.id, shift_id=self.s2.id))

        register(self.v1.id, self.s3.id)
        self.assertIsNotNone(
            VolunteerShift.objects.get(
                volunteer_id=self.v1.id, shift_id=self.s3.id))

        # test cases where volunteer tries to sign up for a shift
        # they are already signed up for
        self.assertEqual(
            register(self.v1.id, self.s1.id), ERROR_CODE_ALREADY_SIGNED_UP)
        self.assertEqual(
            register(self.v1.id, self.s2.id), ERROR_CODE_ALREADY_SIGNED_UP)
        self.assertEqual(
            register(self.v1.id, self.s3.id), ERROR_CODE_ALREADY_SIGNED_UP)

        # test case where more than one volunteer signs up for the same shift
        # v2 can't sign up for s1 because there are no slots remaining
        self.assertEqual(
            register(self.v2.id, self.s1.id), ERROR_CODE_NO_SLOTS_REMAINING)

        register(self.v2.id, self.s2.id)
        self.assertIsNotNone(
            VolunteerShift.objects.get(
                volunteer_id=self.v2.id, shift_id=self.s2.id))

        register(self.v2.id, self.s3.id)
        self.assertIsNotNone(
            VolunteerShift.objects.get(
                volunteer_id=self.v2.id, shift_id=self.s3.id))

        # test cases where a volunteer tries to sign up for a shift
        # they are already signed up for
        self.assertEqual(
            register(self.v2.id, self.s2.id), ERROR_CODE_ALREADY_SIGNED_UP)
        self.assertEqual(
            register(self.v2.id, self.s3.id), ERROR_CODE_ALREADY_SIGNED_UP)


class ShiftReminderTest(unittest.TestCase):
    @classmethod
    def setup_test_data(cls):

        cls.e1 = e1
        cls.j1 = j1
        cls.j2 = j2

        shift_1 = {
            'date': "2015-08-23",
            'start_time': "9:00",
            'end_time': "15:00",
            'max_volunteers': 1,
            'job': cls.j1,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        shift_2 = {
            'date': date.today() + timedelta(7),  # one week ahead
            'start_time': "10:00",
            'end_time': "16:00",
            'max_volunteers': 2,
            'job': cls.j1,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        shift_3 = {
            'date': date.today() + timedelta(1),  # a day ahead
            'start_time': "12:00",
            'end_time': "18:00",
            'max_volunteers': 2,
            'job': cls.j2,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }

        cls.s1 = create_shift_with_details(shift_1)
        cls.s2 = create_shift_with_details(shift_2)
        cls.s3 = create_shift_with_details(shift_3)

        country_name = 'United States'
        country = get_country_by_name(country_name)
        state_name = 'Washington'
        state = get_state_by_name(state_name)
        city_name = 'Bothell'
        city = get_city_by_name(city_name)
        volunteer_1 = {
            'username': 'Jake',
            'first_name': "Jake",
            'last_name': "Flamoy",
            'address': "Mario Land",
            'city': city,
            'state': state,
            'country': country,
            'phone_number': "2374983247",
            'email': "jake@nintendo.com"
        }
        volunteer_2 = {
            'username': 'Dora',
            'first_name': "Dorothy",
            'last_name': "Flamoy",
            'address': "7 Alpine Street",
            'city': city,
            'state': state,
            'country': country,
            'phone_number': "23454545",
            'email': "dora@test.com"
        }

        org_name = 'Google'
        cls.org_obj = create_organization_with_details(org_name)
        cls.v1 = create_volunteer_with_details(volunteer_1, cls.org_obj)
        cls.v2 = create_volunteer_with_details(volunteer_2, cls.org_obj)

    @classmethod
    def setUpClass(cls):
        cls.setup_test_data()

    @classmethod
    def tearDownClass(cls):
        cls.s1.delete()
        cls.s2.delete()
        cls.s3.delete()

        # remove all registered volunteers
        VolunteerShift.objects.all().delete()

    def test_send_reminder(self):

        city_name = 'Roorkee'
        state_name = 'Uttarakhand'
        country_name = 'India'
        country = get_country_by_name(country_name)
        state = get_state_by_name(state_name)
        city = get_city_by_name(city_name)
        location = {
            'address': "Test address",
            'city': city,
            'state': state,
            'country': country,
            'venue': "Near the south entrance"
        }

        set_shift_location(self.s1, location)
        set_shift_location(self.s2, location)
        set_shift_location(self.s3, location)

        self.v1.reminder_days = 1
        self.v2.reminder_days = 7
        self.v1.save()
        self.v2.save()

        # sign up
        register(self.v1.id, self.s1.id)
        register(self.v1.id, self.s2.id)
        register(self.v1.id, self.s3.id)
        register(self.v2.id, self.s1.id)
        register(self.v2.id, self.s2.id)
        register(self.v2.id, self.s3.id)

        # test typical case
        result = send_reminder()

        self.assertEqual(result, 2)


class DeleteShiftTest(unittest.TestCase):
    @classmethod
    def setup_test_data(cls):

        cls.e1 = e1
        cls.j1 = j1

        shift_1 = {
            'date': "2012-10-28",
            'start_time': "9:00",
            'end_time': "15:00",
            'max_volunteers': 1,
            'job': cls.j1,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }
        shift_2 = {
            'date': "2012-10-25",
            'start_time': "10:00",
            'end_time': "16:00",
            'max_volunteers': 2,
            'job': cls.j1,
            'address': 'shift-address',
            'venue': 'shift-venue'
        }

        cls.s1 = create_shift_with_details(shift_1)
        cls.s2 = create_shift_with_details(shift_2)

        city_name = 'Roorkee'
        state_name = 'Uttarakhand'
        country_name = 'India'
        country = get_country_by_name(country_name)
        state = get_state_by_name(state_name)
        city = get_city_by_name(city_name)
        volunteer_1 = {
            'username': 'Aaron',
            'first_name': "Aaron",
            'last_name': "Turtle",
            'address': "Mario Land",
            'city': city,
            'state': state,
            'country': country,
            'phone_number': "2374983247",
            'email': "aaron@nintendo.com"
        }
        org_name = 'organization'
        cls.org_obj = create_organization_with_details(org_name)
        cls.v1 = create_volunteer_with_details(volunteer_1, cls.org_obj)

    @classmethod
    def setUpClass(cls):
        cls.setup_test_data()

    @classmethod
    def tearDownClass(cls):
        cls.s2.delete()

        # remove all registered volunteers
        VolunteerShift.objects.all().delete()

    def test_delete_shift(self):
        # Test delete_shift(shift_id)

        self.assertTrue(delete_shift(self.s1.id))
        self.assertFalse(delete_shift(1000))

        register(self.v1.id, self.s2.id)
        self.assertFalse(delete_shift(self.s2.id))

