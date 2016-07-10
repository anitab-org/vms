import datetime
from datetime import date, timedelta
from django.core.exceptions import ObjectDoesNotExist
import unittest

from shift.models import VolunteerShift
from shift.utils import *

from shift.services import (
            add_shift_hours,
            calculate_duration,
            calculate_total_report_hours,
            cancel_shift_registration,
            clear_shift_hours, delete_shift,
            edit_shift_hours, generate_report,
            get_all_volunteer_shifts_with_hours,
            get_shift_by_id, get_shifts_by_job_id,
            get_shifts_ordered_by_date,
            get_shift_slots_remaining,
            get_shifts_with_open_slots,
            get_unlogged_shifts_by_volunteer_id,
            get_volunteer_shift_by_id,
            get_volunteer_shifts_with_hours,
            get_volunteers_by_shift_id,
            get_logged_volunteers_by_shift_id,
            is_signed_up,
            register,
            send_reminder
            )

def setUpModule():

    global e1
    global j1,j2
    global s1,s2,s3

    event_1 = ["Open Source Event","2012-9-1","2012-11-23"]
    e1 = create_event_with_details(event_1)

    job_1 = ["Software Developer","2012-10-22","2012-10-30","A software job",e1]
    job_2 = ["Systems Administrator","2012-9-1","2012-10-26","A systems administrator job",e1]
    j1 = create_job_with_details(job_1)
    j2 = create_job_with_details(job_2)

    shift_1 = ["2012-10-28","9:00","15:00",1,j1]
    shift_2 = ["2012-10-25","10:00","16:00",2,j1]
    shift_3 = ["2012-10-22","10:00","16:00",4,j2]

    s1 = create_shift_with_details(shift_1)
    s2 = create_shift_with_details(shift_2)
    s3 = create_shift_with_details(shift_3)

def tearDownModule():
    clear_objects()

class ShiftTests(unittest.TestCase):
    '''
    Contains tests which require 
    - only shift objects
    - no objects to be created
    '''

    @classmethod
    def setup_test_data(cls):

        cls.e1 = e1
        cls.j2 = j2
        cls.j1 = j1
        cls.s1 = s1
        cls.s2 = s2

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

        report_list,total_hours = get_report_list(duration_list, report_list, total_hours)

        self.assertEqual(
                        calculate_total_report_hours(report_list),
                        total_hours
                        )

        duration_list = [1.5, 1.34, 2.3, 9, 4.7]
        report_list = []
        total_hours = 0

        report_list,total_hours = get_report_list(duration_list, report_list, total_hours)

        self.assertEqual(
                        calculate_total_report_hours(report_list),
                        total_hours
                        )

        duration_list = [0.03, 0.023, 0.53, 0.863, 0.23, 0.57]
        report_list = []
        total_hours = 0

        report_list,total_hours = get_report_list(duration_list, report_list, total_hours)

        self.assertEqual(
                        calculate_total_report_hours(report_list),
                        total_hours
                        )

        duration_list = [12, 24, 23.5, 15.67, 22.453, 3.42]
        report_list = []
        total_hours = 0

        report_list,total_hours = get_report_list(duration_list, report_list, total_hours)

        self.assertEqual(
                        calculate_total_report_hours(report_list),
                        total_hours
                        )

        duration_list = [5]
        report_list = []
        total_hours = 0

        report_list,total_hours = get_report_list(duration_list, report_list, total_hours)

        self.assertEqual(
                        calculate_total_report_hours(report_list),
                        total_hours
                        )

        duration_list = [0, 0, 0, 0]
        report_list = []
        total_hours = 0

        report_list,total_hours = get_report_list(duration_list, report_list, total_hours)

        self.assertEqual(
                        calculate_total_report_hours(report_list),
                        total_hours
                        )

        duration_list = [0]
        report_list = []
        total_hours = 0

        report_list,total_hours = get_report_list(duration_list, report_list, total_hours)

        self.assertEqual(
                        calculate_total_report_hours(report_list),
                        total_hours
                        )

    def test_calculate_duration(self):

        start_time = datetime.time(hour=1, minute=0)
        end_time = datetime.time(hour=2, minute=0)
        delta_time_hours = 1
        self.assertEqual(
                        calculate_duration(start_time, end_time),
                        delta_time_hours
                        )

        start_time = datetime.time(hour=1, minute=45)
        end_time = datetime.time(hour=2, minute=0)
        delta_time_hours = 0.25
        self.assertEqual(
                        calculate_duration(start_time, end_time),
                        delta_time_hours
                        )

        start_time = datetime.time(hour=1, minute=0)
        end_time = datetime.time(hour=2, minute=30)
        delta_time_hours = 1.5
        self.assertEqual(
                        calculate_duration(start_time, end_time),
                        delta_time_hours
                        )

        start_time = datetime.time(hour=1, minute=0)
        end_time = datetime.time(hour=1, minute=45)
        delta_time_hours = 0.75
        self.assertEqual(
                        calculate_duration(start_time, end_time),
                        delta_time_hours
                        )

        start_time = datetime.time(hour=1, minute=0)
        end_time = datetime.time(hour=13, minute=0)
        delta_time_hours = 12
        self.assertEqual(
                        calculate_duration(start_time, end_time),
                        delta_time_hours
                        )

        start_time = datetime.time(hour=1, minute=0)
        end_time = datetime.time(hour=5, minute=45)
        delta_time_hours = 4.75
        self.assertEqual(
                        calculate_duration(start_time, end_time),
                        delta_time_hours
                        )

        start_time = datetime.time(hour=1, minute=0)
        end_time = datetime.time(hour=1, minute=0)
        delta_time_hours = 0
        self.assertEqual(
                        calculate_duration(start_time, end_time),
                        delta_time_hours
                        )

        start_time = datetime.time(hour=1, minute=0)
        end_time = datetime.time(hour=23, minute=0)
        delta_time_hours = 22
        self.assertEqual(
                        calculate_duration(start_time, end_time),
                        delta_time_hours
                        )

        start_time = datetime.time(hour=22, minute=0)
        end_time = datetime.time(hour=1, minute=0)
        delta_time_hours = 3
        self.assertEqual(
                        calculate_duration(start_time, end_time),
                        delta_time_hours
                        )

        start_time = datetime.time(hour=13, minute=0)
        end_time = datetime.time(hour=1, minute=0)
        delta_time_hours = 12
        self.assertEqual(
                        calculate_duration(start_time, end_time),
                        delta_time_hours
                        )

        start_time = datetime.time(hour=0, minute=0)
        end_time = datetime.time(hour=23, minute=0)
        delta_time_hours = 23
        self.assertEqual(
                        calculate_duration(start_time, end_time),
                        delta_time_hours
                        )

        start_time = datetime.time(hour=23, minute=0)
        end_time = datetime.time(hour=0, minute=0)
        delta_time_hours = 1
        self.assertEqual(
                        calculate_duration(start_time, end_time),
                        delta_time_hours
                        )

    def test_get_shift_by_id(self):

        # test typical cases
        self.assertIsNotNone(get_shift_by_id(self.s1.id))
        self.assertIsNotNone(get_shift_by_id(self.s2.id))

        self.assertEqual(get_shift_by_id(self.s1.id), self.s1)
        self.assertEqual(get_shift_by_id(self.s2.id), self.s2)

        # test non-existant cases
        self.assertIsNone(get_shift_by_id(100))
        self.assertIsNone(get_shift_by_id(200))
        self.assertIsNone(get_shift_by_id(300))
        self.assertIsNone(get_shift_by_id(400))

        self.assertNotEqual(get_shift_by_id(100), self.s1)
        self.assertNotEqual(get_shift_by_id(100), self.s2)
        self.assertNotEqual(get_shift_by_id(200), self.s1)
        self.assertNotEqual(get_shift_by_id(200), self.s2)
        self.assertNotEqual(get_shift_by_id(300), self.s1)
        self.assertNotEqual(get_shift_by_id(300), self.s2)

    def test_get_shifts_by_job_id(self):
        """ Test get_shifts_by_job_id(j_id) """

        self.assertIsNotNone(get_shifts_by_job_id(j1.id))

    def test_get_shifts_ordered_by_date(self):

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

    @classmethod
    def setup_test_data(cls):

        cls.e1 = e1
        cls.j1 = j1
        cls.j2 = j2
        cls.s1 = s1
        cls.s2 = s2
        cls.s3 = s3

        volunteer_1 = ['Yoshi',"Yoshi","Turtle","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","yoshi@nintendo.com"]
        volunteer_2 = ['John',"John","Doe","7 Alpine Street","Maplegrove","Wyoming","USA","23454545","john@test.com"]
        volunteer_3 = ['Ash',"Ash","Ketchum","Pallet Town","Kanto","Gameboy","Japan","23454545","ash@pikachu.com"]

        cls.v1 = create_volunteer_with_details(volunteer_1)
        cls.v2 = create_volunteer_with_details(volunteer_2)
        cls.v3 = create_volunteer_with_details(volunteer_3)

    @classmethod
    def setUpClass(cls):
        cls.setup_test_data()

    def test_add_shift_hours(self):

        # register will return an exception on error
        # (such as when invalid parameters are passed)
        # if an exception does get raised, this test will automatically fail
        register(self.v1.id, self.s1.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=self.v1.id,
                                                        shift_id=self.s1.id
                                                        ))

        register(self.v1.id, self.s2.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=self.v1.id,
                                                        shift_id=self.s2.id
                                                        ))

        register(self.v1.id, self.s3.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=self.v1.id,
                                                        shift_id=self.s3.id
                                                        ))

        start_time = datetime.time(hour=9, minute=0)
        end_time = datetime.time(hour=10, minute=0)
        add_shift_hours(self.v1.id, self.s1.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=self.v1.id,
                                                    shift_id=self.s1.id
                                                    )
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        start_time = datetime.time(hour=10, minute=0)
        end_time = datetime.time(hour=12, minute=0)
        add_shift_hours(self.v1.id, self.s2.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=self.v1.id,
                                                    shift_id=self.s2.id
                                                    )
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        start_time = datetime.time(hour=5, minute=0)
        end_time = datetime.time(hour=6, minute=0)
        add_shift_hours(self.v1.id, self.s3.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=self.v1.id,
                                                    shift_id=self.s3.id
                                                    )
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        # remove all registered volunteers
        VolunteerShift.objects.all().delete()

    def test_cancel_shift_registration(self):

        # test cases when try to cancel when they aren't signed up for a shift
        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(self.v1.id, self.s1.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(self.v1.id, self.s1.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(self.v1.id, self.s2.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(self.v1.id, self.s3.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(self.v2.id, self.s1.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(self.v2.id, self.s2.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(self.v2.id, self.s3.id)

        # register volunteers to shifts
        register(self.v1.id, self.s1.id)
        register(self.v1.id, self.s2.id)
        register(self.v1.id, self.s3.id)
        register(self.v2.id, self.s1.id)
        register(self.v2.id, self.s2.id)
        register(self.v2.id, self.s3.id)

        # test typical cases
        cancel_shift_registration(self.v1.id, self.s1.id)
        cancel_shift_registration(self.v1.id, self.s2.id)
        cancel_shift_registration(self.v1.id, self.s3.id)
        # cancel_shift_registration(v2.id, s1.id)
        # why is this throwing ObjectDoesNotExist?
        cancel_shift_registration(self.v2.id, self.s2.id)
        cancel_shift_registration(self.v2.id, self.s3.id)

        # remove all registered volunteers
        VolunteerShift.objects.all().delete()

    def test_clear_shift_hours(self):

        register(self.v1.id, self.s1.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=self.v1.id,
                                                        shift_id=self.s1.id
                                                        ))

        register(self.v1.id, self.s2.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=self.v1.id,
                                                        shift_id=self.s2.id
                                                        ))

        register(self.v1.id, self.s3.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=self.v1.id,
                                                        shift_id=self.s3.id
                                                        ))

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
                                                    volunteer_id=self.v1.id,
                                                    shift_id=self.s1.id
                                                    )
        self.assertIsNone(volunteer_shift.start_time)
        self.assertIsNone(volunteer_shift.end_time)

        clear_shift_hours(self.v1.id, self.s2.id)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=self.v1.id,
                                                    shift_id=self.s2.id
                                                    )
        self.assertIsNone(volunteer_shift.start_time)
        self.assertIsNone(volunteer_shift.end_time)

        clear_shift_hours(self.v1.id, self.s3.id)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=self.v1.id,
                                                    shift_id=self.s3.id
                                                    )
        self.assertIsNone(volunteer_shift.start_time)
        self.assertIsNone(volunteer_shift.end_time)

        # remove all registered volunteers
        VolunteerShift.objects.all().delete()

    def test_edit_shift_hours(self):

        register(self.v1.id, self.s1.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=self.v1.id,
                                                        shift_id=self.s1.id
                                                        ))

        start_time = datetime.time(hour=9, minute=0)
        end_time = datetime.time(hour=10, minute=0)
        add_shift_hours(self.v1.id, self.s1.id, start_time, end_time)

        start_time = datetime.time(hour=10, minute=0)
        end_time = datetime.time(hour=11, minute=0)
        edit_shift_hours(self.v1.id, self.s1.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=self.v1.id,
                                                    shift_id=self.s1.id
                                                    )
        self.assertIsNotNone(volunteer_shift.start_time)
        self.assertIsNotNone(volunteer_shift.end_time)
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        start_time = datetime.time(hour=1, minute=0)
        end_time = datetime.time(hour=4, minute=0)
        edit_shift_hours(self.v1.id, self.s1.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=self.v1.id,
                                                    shift_id=self.s1.id
                                                    )
        self.assertIsNotNone(volunteer_shift.start_time)
        self.assertIsNotNone(volunteer_shift.end_time)
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        start_time = datetime.time(hour=4, minute=15)
        end_time = datetime.time(hour=12, minute=35)
        edit_shift_hours(self.v1.id, self.s1.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=self.v1.id,
                                                    shift_id=self.s1.id
                                                    )
        self.assertIsNotNone(volunteer_shift.start_time)
        self.assertIsNotNone(volunteer_shift.end_time)
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        start_time = datetime.time(hour=2, minute=5)
        end_time = datetime.time(hour=4, minute=15)
        edit_shift_hours(self.v1.id, self.s1.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=self.v1.id,
                                                    shift_id=self.s1.id
                                                    )
        self.assertIsNotNone(volunteer_shift.start_time)
        self.assertIsNotNone(volunteer_shift.end_time)
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        start_time = datetime.time(hour=5, minute=0)
        end_time = datetime.time(hour=5, minute=30)
        edit_shift_hours(self.v1.id, self.s1.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=self.v1.id,
                                                    shift_id=self.s1.id
                                                    )
        self.assertIsNotNone(volunteer_shift.start_time)
        self.assertIsNotNone(volunteer_shift.end_time)
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        # remove all registered volunteers
        VolunteerShift.objects.all().delete()

    def test_generate_report(self):
        # Tests test_generate_report(volunteer_shift_list) 

        shift_list = [self.s1, self.s2, self.s3]

        self.assertIsNotNone(shift_list)
        self.assertNotEqual(shift_list, False)
        self.assertEqual(len(shift_list), 3)
        self.assertIn(self.s1, shift_list)
        self.assertIn(self.s2, shift_list)
        self.assertIn(self.s3, shift_list)

        # register will return an exception on error
        # (such as when invalid parameters are passed)
        # if an exception does get raised, this test will automatically fail
        register(self.v1.id, self.s1.id)
        volunteer_shift_1 = VolunteerShift.objects.get(
                                volunteer_id=self.v1.id,
                                shift_id=self.s1.id
                                )
        self.assertIsNotNone(volunteer_shift_1)

        register(self.v1.id, self.s2.id)
        volunteer_shift_2 = VolunteerShift.objects.get(
                                    volunteer_id=self.v1.id,
                                    shift_id=self.s2.id
                                    )
        self.assertIsNotNone(volunteer_shift_2)

        register(self.v1.id, self.s3.id)
        volunteer_shift_3 = VolunteerShift.objects.get(
                                    volunteer_id=self.v1.id,
                                    shift_id=self.s3.id
                                    )
        self.assertIsNotNone(volunteer_shift_3)

        volunteer_shift_list = [
                                volunteer_shift_1,
                                volunteer_shift_2,
                                volunteer_shift_3
                                ]

        self.assertIsNotNone(generate_report(volunteer_shift_list))

        # remove all registered volunteers
        VolunteerShift.objects.all().delete()

    def test_get_all_volunteer_shifts_with_hours(self):
        #  Test get_all_volunteer_shifts_with_hours() 

        self.assertIsNotNone(get_all_volunteer_shifts_with_hours())

    def test_get_shift_slots_remaining(self):
        # Test get_shift_slots_remaining(s_id)

        self.assertIsNotNone(get_shift_slots_remaining(self.s1.id))
        self.assertIsNotNone(get_shift_slots_remaining(self.s2.id))
        self.assertIsNotNone(get_shift_slots_remaining(self.s3.id))

    def test_get_shifts_with_open_slots(self):
        # Test get_shifts_with_open_slots(j_id) 

        self.assertIsNotNone(get_shifts_with_open_slots(self.j1.id))
        self.assertIsNotNone(get_shifts_with_open_slots(self.j2.id))

    def test_get_unlogged_shifts_by_volunteer_id(self):

        # sign up
        register(self.v1.id, self.s1.id)
        register(self.v1.id, self.s2.id)
        register(self.v1.id, self.s3.id)

        # test typical case
        shift_list = get_unlogged_shifts_by_volunteer_id(self.v1.id)
        self.assertIsNotNone(shift_list)
        self.assertNotEqual(shift_list, False)
        self.assertEqual(len(shift_list), 3)
        self.assertIn(self.s1, shift_list)
        self.assertIn(self.s2, shift_list)
        self.assertIn(self.s3, shift_list)

        # remove all registered volunteers
        VolunteerShift.objects.all().delete()

    def test_get_volunteer_shift_by_id(self):

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
                                                    volunteer_id=self.v1.id,
                                                    shift_id=self.s1.id
                                                    ))
        self.assertEqual(
                        get_volunteer_shift_by_id(self.v1.id, self.s2.id),
                        VolunteerShift.objects.get(
                            volunteer_id=self.v1.id,
                            shift_id=self.s2.id
                            )
                        )
        self.assertEqual(
                        get_volunteer_shift_by_id(self.v1.id, self.s3.id),
                        VolunteerShift.objects.get(
                            volunteer_id=self.v1.id,
                            shift_id=self.s3.id
                            )
                        )

        # self.assertEqual(get_volunteer_shift_by_id(v2.id, s1.id),
        # VolunteerShift.objects.get(volunteer_id=v2.id, shift_id=s1.id))
        # why does this throw DoesNotExist?
        self.assertEqual(
                        get_volunteer_shift_by_id(self.v2.id, self.s2.id),
                        VolunteerShift.objects.get(
                            volunteer_id=self.v2.id,
                            shift_id=self.s2.id
                            )
                        )
        self.assertEqual(
                        get_volunteer_shift_by_id(self.v2.id, self.s3.id),
                        VolunteerShift.objects.get(
                            volunteer_id=self.v2.id,
                            shift_id=self.s3.id
                            )
                        )

        # remove all registered volunteers
        VolunteerShift.objects.all().delete()

    def test_get_volunteer_shifts_with_hours(self):
         # Test  get_volunteer_shifts_with_hours(v_id) 

        self.assertIsNotNone(get_volunteer_shifts_with_hours(self.v1))
        self.assertIsNotNone(get_volunteer_shifts_with_hours(self.v2))

        # remove all registered volunteers
        VolunteerShift.objects.all().delete()

    def test_get_volunteers_by_shift_id(self):

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

        #test order
        self.assertEqual(volunteer_list_for_shift_3[0], self.v3)
        self.assertEqual(volunteer_list_for_shift_3[1], self.v2)
        self.assertEqual(volunteer_list_for_shift_3[2], self.v1)

        # remove all registered volunteers
        VolunteerShift.objects.all().delete()

    def test_get_logged_volunteers_by_shift_id(self):

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
        logged_volunteer_list_for_shift = get_logged_volunteers_by_shift_id(self.s3.id)

        # test typical case and order
        self.assertEqual(len(logged_volunteer_list_for_shift), 2)
        self.assertEqual(logged_volunteer_list_for_shift[0].volunteer, self.v3)
        self.assertEqual(logged_volunteer_list_for_shift[1].volunteer, self.v1)

        # remove all registered volunteers
        VolunteerShift.objects.all().delete()

    def test_is_signed_up(self):

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

        # remove all registered volunteers
        VolunteerShift.objects.all().delete()

    def test_register(self):

        ERROR_CODE_ALREADY_SIGNED_UP = "ERROR_CODE_ALREADY_SIGNED_UP"
        ERROR_CODE_NO_SLOTS_REMAINING = "ERROR_CODE_NO_SLOTS_REMAINING"

        # test typical cases
        register(self.v1.id, self.s1.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=self.v1.id,
                                                        shift_id=self.s1.id
                                                        ))

        register(self.v1.id, self.s2.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=self.v1.id,
                                                        shift_id=self.s2.id
                                                        ))

        register(self.v1.id, self.s3.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=self.v1.id,
                                                        shift_id=self.s3.id
                                                        ))

        # test cases where volunteer tries to sign up for a shift
        # they are already signed up for
        self.assertEqual(register(self.v1.id, self.s1.id), ERROR_CODE_ALREADY_SIGNED_UP)
        self.assertEqual(register(self.v1.id, self.s2.id), ERROR_CODE_ALREADY_SIGNED_UP)
        self.assertEqual(register(self.v1.id, self.s3.id), ERROR_CODE_ALREADY_SIGNED_UP)

        # test case where more than one volunteer signs up for the same shift
        # v2 can't sign up for s1 because there are no slots remaining
        self.assertEqual(register(self.v2.id, self.s1.id), ERROR_CODE_NO_SLOTS_REMAINING)

        register(self.v2.id, self.s2.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=self.v2.id,
                                                        shift_id=self.s2.id
                                                        ))

        register(self.v2.id, self.s3.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=self.v2.id,
                                                        shift_id=self.s3.id
                                                        ))

        # test cases where a volunteer tries to sign up for a shift
        # they are already signed up for
        self.assertEqual(register(self.v2.id, self.s2.id), ERROR_CODE_ALREADY_SIGNED_UP)
        self.assertEqual(register(self.v2.id, self.s3.id), ERROR_CODE_ALREADY_SIGNED_UP)

        # remove all registered volunteers
        VolunteerShift.objects.all().delete()

class ShiftReminderTest(unittest.TestCase):

    @classmethod
    def setup_test_data(cls):

        cls.e1 = e1
        cls.j1 = j1
        cls.j2 = j2

        shift_1 = ["2015-08-23","9:00","15:00",1,cls.j1]
        shift_2 = [date.today() + timedelta(7),"10:00","16:00",2,cls.j1] #one week date
        shift_3 = [date.today() + timedelta(1),"12:00","18:00",2,cls.j2] #tomorrow date

        cls.s1 = create_shift_with_details(shift_1)
        cls.s2 = create_shift_with_details(shift_2)
        cls.s3 = create_shift_with_details(shift_3)

        volunteer_1 = ['Jake',"Jake","Flamoy","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","jake@nintendo.com"]
        volunteer_2 = ['Dora',"Dorothy","Flamoy","7 Alpine Street","Maplegrove","Wyoming","USA","23454545","dora@test.com"]

        cls.v1 = create_volunteer_with_details(volunteer_1)
        cls.v2 = create_volunteer_with_details(volunteer_2)

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

        self.v1.reminder_days=1
        self.v2.reminder_days=7
        self.v1.save()
        self.v2.save()

        self.s1.address="Test address",
        self.s1.city="Atlanta",
        self.s1.state="Georgia",
        self.s1.country="USA",
        self.s1.venue="Near the south entrance"
        self.s1.save()

        self.s2.address="Test address",
        self.s2.city="Atlanta",
        self.s2.state="Georgia",
        self.s2.country="USA",
        self.s2.venue="Near the south entrance"
        self.s2.save()

        self.s3.address="Test address",
        self.s3.city="Atlanta",
        self.s3.state="Georgia",
        self.s3.country="USA",
        self.s3.venue="Near the south entrance"
        self.s3.save()

        # sign up
        register(self.v1.id, self.s1.id)
        register(self.v1.id, self.s2.id)
        register(self.v1.id, self.s3.id)
        register(self.v2.id, self.s1.id)
        register(self.v2.id, self.s2.id)
        register(self.v2.id, self.s3.id)

        # test typical case
        result = send_reminder()       
               
        self.assertEqual(result,2)

class DeleteShiftTest(unittest.TestCase):

    @classmethod
    def setup_test_data(cls):

        cls.e1 = e1
        cls.j1 = j1

        shift_1 = ["2012-10-28","9:00","15:00",1,cls.j1]
        shift_2 = ["2012-10-25","10:00","16:00",2,cls.j1]

        cls.s1 = create_shift_with_details(shift_1)
        cls.s2 = create_shift_with_details(shift_2)

        volunteer_1 = ['Aaron',"Aaron","Turtle","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","aaron@nintendo.com"]
        cls.v1 = create_volunteer_with_details(volunteer_1)

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
        self.assertFalse(delete_shift(100))

        register(self.v1.id, self.s2.id)
        self.assertFalse(delete_shift(self.s2.id))
