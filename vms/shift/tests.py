import datetime
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from event.models import Event
from job.models import Job
from shift.models import Shift, VolunteerShift
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
from volunteer.models import Volunteer


class ShiftMethodTests(TestCase):

    def test_send_reminder(self):
        

        u1 = User.objects.create_user('Marina')
        u2 = User.objects.create_user('Anna')

        v1 = Volunteer(
            first_name="Marina",
            last_name="Tsvetaeva",
            address="MyAddress",
            city="MyCity",
            state="MyState",
            country="MyCountry",
            phone_number="2374983247",
            email="email1@gmail.com",
            reminder_days=1,
            user=u1
            )

        
        
        v2 = Volunteer(
            first_name="Anna",
            last_name="Akhmatova",
            address="MyAddress",
            city="MyCity",
            state="MyState",
            country="MyCountry",
            phone_number="2374983247",
            email="email2@gmail.com",
            reminder_days=7,
            user=u2
            )
        v1.save()
        v2.save()

        e1 = Event(
                name="GHC 2015",
                start_date="2015-07-22",
                end_date="2015-08-23"
                )

        e1.save()

        j1 = Job(
            name="Volunteer Program Manager",
            start_date="2015-07-22",
            end_date="2015-08-23",
            description="Volunteer Program Manager",
            event=e1
            )

        j2 = Job(
            name="Volunteer Coordinator",
            start_date="2015-07-22",
            end_date="2015-08-23",
            description="Volunteer Coordinator",
            event=e1
            )

        j1.save()
        j2.save()

        s1 = Shift(
            date="2015-08-23",
            start_time="9:00",
            end_time="3:00",
            max_volunteers=1,
            address="Test address",
            city="Atlanta",
            state="Georgia",
            country="USA",
            venue="Near the south entrance",
            job=j1
            )

        s2 = Shift(
            date=date.today() + timedelta(7), #one week date
            start_time="10:00",
            end_time="4:00",
            max_volunteers=2,
            address="Test address",
            city="Atlanta",
            state="Georgia",
            country="USA",
            venue="Near the south entrance",
            job=j1
            )

        s3 = Shift(
            date=date.today() + timedelta(1), #tomorrow date
            start_time="12:00",
            end_time="6:00",
            max_volunteers=4,
            address="Test address",
            city="Atlanta",
            state="Georgia",
            country="USA",
            venue="Near the south entrance",
            job=j2
            )

        s1.save()
        s2.save()
        s3.save()

        # sign up
        register(v1.id, s1.id)
        register(v1.id, s2.id)
        register(v1.id, s3.id)
        register(v2.id, s1.id)
        register(v2.id, s2.id)
        register(v2.id, s3.id)

        # test typical case
        
        result = send_reminder()       
               
        self.assertEqual(result,2)
    

    def test_add_shift_hours(self):

        u1 = User.objects.create_user('Yoshi')

        v1 = Volunteer(
                    first_name="Yoshi",
                    last_name="Turtle",
                    address="Mario Land",
                    city="Nintendo Land",
                    state="Nintendo State",
                    country="Nintendo Nation",
                    phone_number="2374983247",
                    email="yoshi@nintendo.com",
                    user=u1
                    )

        v1.save()

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )

        e1.save()

        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )

        j2 = Job(
                name="Systems Administrator",
                start_date="2012-9-1",
                end_date="2012-10-26",
                description="A systems administrator job",
                event=e1
                )

        j1.save()
        j2.save()

        s1 = Shift(
                date="2012-10-23",
                start_time="9:00",
                end_time="3:00",
                max_volunteers=1,
                job=j1
                )

        s2 = Shift(
                date="2012-10-23",
                start_time="10:00",
                end_time="4:00",
                max_volunteers=2,
                job=j1
                )

        s3 = Shift(
                date="2012-10-23",
                start_time="12:00",
                end_time="6:00",
                max_volunteers=4,
                job=j2
                )

        s1.save()
        s2.save()
        s3.save()

        # register will return an exception on error
        # (such as when invalid parameters are passed)
        # if an exception does get raised, this test will automatically fail
        register(v1.id, s1.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=v1.id,
                                                        shift_id=s1.id
                                                        ))

        register(v1.id, s2.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=v1.id,
                                                        shift_id=s2.id
                                                        ))

        register(v1.id, s3.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=v1.id,
                                                        shift_id=s3.id
                                                        ))

        start_time = datetime.time(hour=9, minute=0)
        end_time = datetime.time(hour=10, minute=0)
        add_shift_hours(v1.id, s1.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=v1.id,
                                                    shift_id=s1.id
                                                    )
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        start_time = datetime.time(hour=10, minute=0)
        end_time = datetime.time(hour=12, minute=0)
        add_shift_hours(v1.id, s2.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=v1.id,
                                                    shift_id=s2.id
                                                    )
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        start_time = datetime.time(hour=5, minute=0)
        end_time = datetime.time(hour=6, minute=0)
        add_shift_hours(v1.id, s3.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=v1.id,
                                                    shift_id=s3.id
                                                    )
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

    def test_calculate_total_report_hours(self):

        duration_list = [1, 1, 1, 1]
        report_list = []
        total_hours = 0

        for duration in duration_list:
            total_hours += duration
            report = {}
            report["duration"] = duration
            report_list.append(report)

        self.assertEqual(
                        calculate_total_report_hours(report_list),
                        total_hours
                        )

        duration_list = [1.5, 1.34, 2.3, 9, 4.7]
        report_list = []
        total_hours = 0

        for duration in duration_list:
            total_hours += duration
            report = {}
            report["duration"] = duration
            report_list.append(report)

        self.assertEqual(
                        calculate_total_report_hours(report_list),
                        total_hours
                        )

        duration_list = [0.03, 0.023, 0.53, 0.863, 0.23, 0.57]
        report_list = []
        total_hours = 0

        for duration in duration_list:
            total_hours += duration
            report = {}
            report["duration"] = duration
            report_list.append(report)

        self.assertEqual(
                        calculate_total_report_hours(report_list),
                        total_hours
                        )

        duration_list = [12, 24, 23.5, 15.67, 22.453, 3.42]
        report_list = []
        total_hours = 0

        for duration in duration_list:
            total_hours += duration
            report = {}
            report["duration"] = duration
            report_list.append(report)

        self.assertEqual(
                        calculate_total_report_hours(report_list),
                        total_hours
                        )

        duration_list = [5]
        report_list = []
        total_hours = 0

        for duration in duration_list:
            total_hours += duration
            report = {}
            report["duration"] = duration
            report_list.append(report)

        self.assertEqual(
                        calculate_total_report_hours(report_list),
                        total_hours
                        )

        duration_list = [0, 0, 0, 0]
        report_list = []
        total_hours = 0

        for duration in duration_list:
            total_hours += duration
            report = {}
            report["duration"] = duration
            report_list.append(report)

        self.assertEqual(
                        calculate_total_report_hours(report_list),
                        total_hours
                        )

        duration_list = [0]
        report_list = []
        total_hours = 0

        for duration in duration_list:
            total_hours += duration
            report = {}
            report["duration"] = duration
            report_list.append(report)

        self.assertEqual(
                        calculate_total_report_hours(report_list),
                        total_hours
                        )

    def test_cancel_shift_registration(self):

        u1 = User.objects.create_user('Yoshi')
        u2 = User.objects.create_user('John')

        v1 = Volunteer(
                        first_name="Yoshi",
                        last_name="Turtle",
                        address="Mario Land",
                        city="Nintendo Land",
                        state="Nintendo State",
                        country="Nintendo Nation",
                        phone_number="2374983247",
                        email="yoshi@nintendo.com",
                        user=u1
                        )

        v2 = Volunteer(
                        first_name="John",
                        last_name="Doe",
                        address="7 Alpine Street",
                        city="Maplegrove",
                        state="Wyoming",
                        country="USA",
                        phone_number="23454545",
                        email="john@test.com",
                        user=u2
                        )

        v1.save()
        v2.save()

        e1 = Event(
                    name="Open Source Event",
                    start_date="2012-10-22",
                    end_date="2012-10-23"
                    )

        e1.save()

        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )

        j2 = Job(
                name="Systems Administrator",
                start_date="2012-9-1",
                end_date="2012-10-26",
                description="A systems administrator job",
                event=e1
                )

        j1.save()
        j2.save()

        s1 = Shift(
                date="2012-10-23",
                start_time="9:00",
                end_time="3:00",
                max_volunteers=1,
                job=j1
                )

        s2 = Shift(
                date="2012-10-23",
                start_time="10:00",
                end_time="4:00",
                max_volunteers=2,
                job=j1
                )

        s3 = Shift(
                date="2012-10-23",
                start_time="12:00",
                end_time="6:00",
                max_volunteers=4,
                job=j2
                )

        s1.save()
        s2.save()
        s3.save()

        # test cases when try to cancel when they aren't signed up for a shift
        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(v1.id, s1.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(v1.id, s1.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(v1.id, s2.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(v1.id, s3.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(v2.id, s1.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(v2.id, s2.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(v2.id, s3.id)

        # register volunteers to shifts
        register(v1.id, s1.id)
        register(v1.id, s2.id)
        register(v1.id, s3.id)
        register(v2.id, s1.id)
        register(v2.id, s2.id)
        register(v2.id, s3.id)

        # test typical cases
        cancel_shift_registration(v1.id, s1.id)
        cancel_shift_registration(v1.id, s2.id)
        cancel_shift_registration(v1.id, s3.id)
        # cancel_shift_registration(v2.id, s1.id)
        # why is this throwing ObjectDoesNotExist?
        cancel_shift_registration(v2.id, s2.id)
        cancel_shift_registration(v2.id, s3.id)

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

    def test_clear_shift_hours(self):

        u1 = User.objects.create_user('Yoshi')

        v1 = Volunteer(
                    first_name="Yoshi",
                    last_name="Turtle",
                    address="Mario Land",
                    city="Nintendo Land",
                    state="Nintendo State",
                    country="Nintendo Nation",
                    phone_number="2374983247",
                    email="yoshi@nintendo.com",
                    user=u1
                    )

        v1.save()

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )

        e1.save()

        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )

        j2 = Job(
                name="Systems Administrator",
                start_date="2012-9-1",
                end_date="2012-10-26",
                description="A systems administrator job",
                event=e1
                )

        j1.save()
        j2.save()

        s1 = Shift(
                date="2012-10-23",
                start_time="9:00",
                end_time="3:00",
                max_volunteers=1,
                job=j1
                )

        s2 = Shift(
                date="2012-10-23",
                start_time="10:00",
                end_time="4:00",
                max_volunteers=2,
                job=j1
                )

        s3 = Shift(
                date="2012-10-23",
                start_time="12:00",
                end_time="6:00",
                max_volunteers=4,
                job=j2
                )

        s1.save()
        s2.save()
        s3.save()

        register(v1.id, s1.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=v1.id,
                                                        shift_id=s1.id
                                                        ))

        register(v1.id, s2.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=v1.id,
                                                        shift_id=s2.id
                                                        ))

        register(v1.id, s3.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=v1.id,
                                                        shift_id=s3.id
                                                        ))

        start_time = datetime.time(hour=9, minute=0)
        end_time = datetime.time(hour=10, minute=0)
        add_shift_hours(v1.id, s1.id, start_time, end_time)

        start_time = datetime.time(hour=10, minute=0)
        end_time = datetime.time(hour=12, minute=0)
        add_shift_hours(v1.id, s2.id, start_time, end_time)

        start_time = datetime.time(hour=5, minute=0)
        end_time = datetime.time(hour=6, minute=0)
        add_shift_hours(v1.id, s3.id, start_time, end_time)

        clear_shift_hours(v1.id, s1.id)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=v1.id,
                                                    shift_id=s1.id
                                                    )
        self.assertIsNone(volunteer_shift.start_time)
        self.assertIsNone(volunteer_shift.end_time)

        clear_shift_hours(v1.id, s2.id)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=v1.id,
                                                    shift_id=s2.id
                                                    )
        self.assertIsNone(volunteer_shift.start_time)
        self.assertIsNone(volunteer_shift.end_time)

        clear_shift_hours(v1.id, s3.id)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=v1.id,
                                                    shift_id=s3.id
                                                    )
        self.assertIsNone(volunteer_shift.start_time)
        self.assertIsNone(volunteer_shift.end_time)

    def test_delete_shift(self):
        """ Test delete_shift(shift_id) """
        u1 = User.objects.create_user('Yoshi')

        v1 = Volunteer(
                    first_name="Yoshi",
                    last_name="Turtle",
                    address="Mario Land",
                    city="Nintendo Land",
                    state="Nintendo State",
                    country="Nintendo Nation",
                    phone_number="2374983247",
                    email="yoshi@nintendo.com",
                    user=u1
                    )

        v1.save()

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )

        e1.save()

        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )

        j1.save()

        s1 = Shift(
                date="2012-10-23",
                start_time="1:00",
                end_time="12:00",
                max_volunteers=1,
                job=j1
                )

        s2 = Shift(
                date="2011-11-11",
                start_time="11:00",
                end_time="12:00",
                max_volunteers=3,
                job=j1
                )

        s1.save()
        s2.save()

        self.assertTrue(delete_shift(s1.id))
        self.assertFalse(delete_shift(100))

        register(v1.id, s2.id)
        self.assertFalse(delete_shift(s2.id))


    def test_edit_shift_hours(self):
        u1 = User.objects.create_user('Yoshi')

        v1 = Volunteer(
                    first_name="Yoshi",
                    last_name="Turtle",
                    address="Mario Land",
                    city="Nintendo Land",
                    state="Nintendo State",
                    country="Nintendo Nation",
                    phone_number="2374983247",
                    email="yoshi@nintendo.com",
                    user=u1
                    )

        v1.save()

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )

        e1.save()

        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )

        j1.save()

        s1 = Shift(
                date="2012-10-23",
                start_time="1:00",
                end_time="12:00",
                max_volunteers=1,
                job=j1
                )

        s1.save()

        register(v1.id, s1.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=v1.id,
                                                        shift_id=s1.id
                                                        ))

        start_time = datetime.time(hour=9, minute=0)
        end_time = datetime.time(hour=10, minute=0)
        add_shift_hours(v1.id, s1.id, start_time, end_time)

        start_time = datetime.time(hour=10, minute=0)
        end_time = datetime.time(hour=11, minute=0)
        edit_shift_hours(v1.id, s1.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=v1.id,
                                                    shift_id=s1.id
                                                    )
        self.assertIsNotNone(volunteer_shift.start_time)
        self.assertIsNotNone(volunteer_shift.end_time)
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        start_time = datetime.time(hour=1, minute=0)
        end_time = datetime.time(hour=4, minute=0)
        edit_shift_hours(v1.id, s1.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=v1.id,
                                                    shift_id=s1.id
                                                    )
        self.assertIsNotNone(volunteer_shift.start_time)
        self.assertIsNotNone(volunteer_shift.end_time)
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        start_time = datetime.time(hour=4, minute=15)
        end_time = datetime.time(hour=12, minute=35)
        edit_shift_hours(v1.id, s1.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=v1.id,
                                                    shift_id=s1.id
                                                    )
        self.assertIsNotNone(volunteer_shift.start_time)
        self.assertIsNotNone(volunteer_shift.end_time)
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        start_time = datetime.time(hour=2, minute=5)
        end_time = datetime.time(hour=4, minute=15)
        edit_shift_hours(v1.id, s1.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=v1.id,
                                                    shift_id=s1.id
                                                    )
        self.assertIsNotNone(volunteer_shift.start_time)
        self.assertIsNotNone(volunteer_shift.end_time)
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

        start_time = datetime.time(hour=5, minute=0)
        end_time = datetime.time(hour=5, minute=30)
        edit_shift_hours(v1.id, s1.id, start_time, end_time)
        volunteer_shift = VolunteerShift.objects.get(
                                                    volunteer_id=v1.id,
                                                    shift_id=s1.id
                                                    )
        self.assertIsNotNone(volunteer_shift.start_time)
        self.assertIsNotNone(volunteer_shift.end_time)
        self.assertEqual(volunteer_shift.start_time, start_time)
        self.assertEqual(volunteer_shift.end_time, end_time)

    def test_generate_report(self):
        """ Tests test_generate_report(volunteer_shift_list) """
        u1 = User.objects.create_user('Yoshi')

        v1 = Volunteer(
                    first_name="Yoshi",
                    last_name="Turtle",
                    address="Mario Land",
                    city="Nintendo Land",
                    state="Nintendo State",
                    country="Nintendo Nation",
                    phone_number="2374983247",
                    email="yoshi@nintendo.com",
                    user=u1
                    )

        v1.save()

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )

        e1.save()

        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )

        j2 = Job(
                name="Systems Administrator",
                start_date="2012-9-1",
                end_date="2012-10-26",
                description="A systems administrator job",
                event=e1
                )

        j1.save()
        j2.save()

        s1 = Shift(
                date="2012-10-23",
                start_time="9:00",
                end_time="3:00",
                max_volunteers=1,
                job=j1
                )

        s2 = Shift(
                date="2012-10-23",
                start_time="10:00",
                end_time="4:00",
                max_volunteers=2,
                job=j1
                )

        s3 = Shift(
                date="2012-10-23",
                start_time="12:00",
                end_time="6:00",
                max_volunteers=4,
                job=j2
                )

        s1.save()
        s2.save()
        s3.save()

        shift_list = [s1, s2, s3]

        self.assertIsNotNone(shift_list)
        self.assertNotEqual(shift_list, False)
        self.assertEqual(len(shift_list), 3)
        self.assertIn(s1, shift_list)
        self.assertIn(s2, shift_list)
        self.assertIn(s3, shift_list)

        # register will return an exception on error
        # (such as when invalid parameters are passed)
        # if an exception does get raised, this test will automatically fail
        register(v1.id, s1.id)
        volunteer_shift_1 = VolunteerShift.objects.get(
                                volunteer_id=v1.id,
                                shift_id=s1.id
                                )
        self.assertIsNotNone(volunteer_shift_1)

        register(v1.id, s2.id)
        volunteer_shift_2 = VolunteerShift.objects.get(
                                    volunteer_id=v1.id,
                                    shift_id=s2.id
                                    )
        self.assertIsNotNone(volunteer_shift_2)

        register(v1.id, s3.id)
        volunteer_shift_3 = VolunteerShift.objects.get(
                                    volunteer_id=v1.id,
                                    shift_id=s3.id
                                    )
        self.assertIsNotNone(volunteer_shift_3)

        volunteer_shift_list = [
                                volunteer_shift_1,
                                volunteer_shift_2,
                                volunteer_shift_3
                                ]

        self.assertIsNotNone(generate_report(volunteer_shift_list))

    def test_get_all_volunteer_shifts_with_hours(self):
        """ Test get_all_volunteer_shifts_with_hours() """
        u1 = User.objects.create_user('Yoshi')

        v1 = Volunteer(
                    first_name="Yoshi",
                    last_name="Turtle",
                    address="Mario Land",
                    city="Nintendo Land",
                    state="Nintendo State",
                    country="Nintendo Nation",
                    phone_number="2374983247",
                    email="yoshi@nintendo.com",
                    user=u1
                    )

        v1.save()

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )

        e1.save()

        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )

        j2 = Job(
                name="Systems Administrator",
                start_date="2012-9-1",
                end_date="2012-10-26",
                description="A systems administrator job",
                event=e1
                )

        j1.save()
        j2.save()

        s1 = Shift(
                date="2012-10-23",
                start_time="9:00",
                end_time="3:00",
                max_volunteers=1,
                job=j1
                )

        s2 = Shift(
                date="2012-10-23",
                start_time="10:00",
                end_time="4:00",
                max_volunteers=2,
                job=j1
                )

        s3 = Shift(
                date="2012-10-23",
                start_time="12:00",
                end_time="6:00",
                max_volunteers=4,
                job=j2
                )

        s1.save()
        s2.save()
        s3.save()

        self.assertIsNotNone(get_all_volunteer_shifts_with_hours())

    def test_get_shift_by_id(self):

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )

        e1.save()

        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )

        j1.save()

        s1 = Shift(
                date="2012-10-23",
                start_time="9:00",
                end_time="3:00",
                max_volunteers=1,
                job=j1
                )

        s2 = Shift(
                date="2012-10-23",
                start_time="10:00",
                end_time="4:00",
                max_volunteers=2,
                job=j1
                )

        s3 = Shift(
                date="2012-10-23",
                start_time="12:00",
                end_time="6:00",
                max_volunteers=4,
                job=j1
                )

        s1.save()
        s2.save()
        s3.save()

        # test typical cases
        self.assertIsNotNone(get_shift_by_id(s1.id))
        self.assertIsNotNone(get_shift_by_id(s2.id))
        self.assertIsNotNone(get_shift_by_id(s3.id))

        self.assertEqual(get_shift_by_id(s1.id), s1)
        self.assertEqual(get_shift_by_id(s2.id), s2)
        self.assertEqual(get_shift_by_id(s3.id), s3)

        # test non-existant cases
        self.assertIsNone(get_shift_by_id(100))
        self.assertIsNone(get_shift_by_id(200))
        self.assertIsNone(get_shift_by_id(300))
        self.assertIsNone(get_shift_by_id(400))

        self.assertNotEqual(get_shift_by_id(100), s1)
        self.assertNotEqual(get_shift_by_id(100), s2)
        self.assertNotEqual(get_shift_by_id(100), s3)
        self.assertNotEqual(get_shift_by_id(200), s1)
        self.assertNotEqual(get_shift_by_id(200), s2)
        self.assertNotEqual(get_shift_by_id(200), s3)
        self.assertNotEqual(get_shift_by_id(300), s1)
        self.assertNotEqual(get_shift_by_id(300), s2)
        self.assertNotEqual(get_shift_by_id(300), s3)

    def test_get_shifts_by_job_id(self):
        """ Test get_shifts_by_job_id(j_id) """

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )

        e1.save()

        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )

        j1.save()

        s1 = Shift(
                date="2012-10-23",
                start_time="9:00",
                end_time="3:00",
                max_volunteers=1,
                job=j1
                )

        s2 = Shift(
                date="2012-10-23",
                start_time="10:00",
                end_time="4:00",
                max_volunteers=2,
                job=j1
                )

        s3 = Shift(
                date="2012-10-23",
                start_time="12:00",
                end_time="6:00",
                max_volunteers=4,
                job=j1
                )

        s1.save()
        s2.save()
        s3.save()

        self.assertIsNotNone(get_shifts_by_job_id(j1.id))

    def test_get_shifts_ordered_by_date(self):

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )

        e1.save()

        j1 = Job(
            name="Software Developer",
            start_date="2012-10-22",
            end_date="2012-10-23",
            description="A software job",
            event=e1
            )

        j1.save()

        s1 = Shift(
            date="2012-12-10",
            start_time="9:00",
            end_time="3:00",
            max_volunteers=1,
            job=j1
            )

        s2 = Shift(
            date="2012-6-25",
            start_time="10:00",
            end_time="4:00",
            max_volunteers=2,
            job=j1
            )

        s3 = Shift(
            date="2012-1-9",
            start_time="12:00",
            end_time="6:00",
            max_volunteers=4,
            job=j1
            )

        s1.save()
        s2.save()
        s3.save()

        # test typical case
        shift_list = get_shifts_ordered_by_date(j1.id)
        self.assertIsNotNone(shift_list)
        self.assertNotEqual(shift_list, False)
        self.assertEqual(len(shift_list), 3)
        self.assertIn(s1, shift_list)
        self.assertIn(s2, shift_list)
        self.assertIn(s3, shift_list)

        # test order
        self.assertEqual(shift_list[0], s3)
        self.assertEqual(shift_list[1], s2)
        self.assertEqual(shift_list[2], s1)

    def test_get_shift_slots_remaining(self):
        """ Test get_shift_slots_remaining(s_id) """

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )

        e1.save()

        j1 = Job(
            name="Software Developer",
            start_date="2012-10-22",
            end_date="2012-10-23",
            description="A software job",
            event=e1
            )

        j1.save()

        s1 = Shift(
            date="2012-12-10",
            start_time="9:00",
            end_time="3:00",
            max_volunteers=1,
            job=j1
            )

        s2 = Shift(
            date="2012-6-25",
            start_time="10:00",
            end_time="4:00",
            max_volunteers=2,
            job=j1
            )

        s3 = Shift(
            date="2012-1-9",
            start_time="12:00",
            end_time="6:00",
            max_volunteers=4,
            job=j1
            )

        s1.save()
        s2.save()
        s3.save()

        self.assertIsNotNone(get_shift_slots_remaining(s1.id))
        self.assertIsNotNone(get_shift_slots_remaining(s2.id))
        self.assertIsNotNone(get_shift_slots_remaining(s3.id))

    def test_get_shifts_with_open_slots(self):
        """ Test get_shifts_with_open_slots(j_id) """
        u1 = User.objects.create_user('Yoshi')

        v1 = Volunteer(
                    first_name="Yoshi",
                    last_name="Turtle",
                    address="Mario Land",
                    city="Nintendo Land",
                    state="Nintendo State",
                    country="Nintendo Nation",
                    phone_number="2374983247",
                    email="yoshi@nintendo.com",
                    user=u1
                    )

        v1.save()

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )

        e1.save()

        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )

        j2 = Job(
                name="Systems Administrator",
                start_date="2012-9-1",
                end_date="2012-10-26",
                description="A systems administrator job",
                event=e1
                )

        j1.save()
        j2.save()

        s1 = Shift(
                date="2012-10-23",
                start_time="9:00",
                end_time="3:00",
                max_volunteers=1,
                job=j1
                )

        s2 = Shift(
                date="2012-10-23",
                start_time="10:00",
                end_time="4:00",
                max_volunteers=2,
                job=j1
                )

        s3 = Shift(
                date="2012-10-23",
                start_time="12:00",
                end_time="6:00",
                max_volunteers=4,
                job=j2
                )

        s1.save()
        s2.save()
        s3.save()

        self.assertIsNotNone(get_shifts_with_open_slots(j1.id))
        self.assertIsNotNone(get_shifts_with_open_slots(j2.id))

    def test_get_unlogged_shifts_by_volunteer_id(self):

        u1 = User.objects.create_user('Yoshi')

        v1 = Volunteer(
            first_name="Yoshi",
            last_name="Turtle",
            address="Mario Land",
            city="Nintendo Land",
            state="Nintendo State",
            country="Nintendo Nation",
            phone_number="2374983247",
            email="yoshi@nintendo.com",
            user=u1
            )

        v1.save()

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )

        e1.save()

        j1 = Job(
            name="Software Developer",
            start_date="2012-10-22",
            end_date="2012-10-23",
            description="A software job",
            event=e1
            )

        j2 = Job(
            name="Systems Administrator",
            start_date="2012-9-1",
            end_date="2012-10-26",
            description="A systems administrator job",
            event=e1
            )

        j1.save()
        j2.save()

        s1 = Shift(
            date="2012-10-23",
            start_time="9:00",
            end_time="3:00",
            max_volunteers=1,
            job=j1
            )

        s2 = Shift(
            date="2012-10-23",
            start_time="10:00",
            end_time="4:00",
            max_volunteers=2,
            job=j1
            )

        s3 = Shift(
            date="2012-10-23",
            start_time="12:00",
            end_time="6:00",
            max_volunteers=4,
            job=j2
            )

        s1.save()
        s2.save()
        s3.save()

        # sign up
        register(v1.id, s1.id)
        register(v1.id, s2.id)
        register(v1.id, s3.id)

        # test typical case
        shift_list = get_unlogged_shifts_by_volunteer_id(v1.id)
        self.assertIsNotNone(shift_list)
        self.assertNotEqual(shift_list, False)
        self.assertEqual(len(shift_list), 3)
        self.assertIn(s1, shift_list)
        self.assertIn(s2, shift_list)
        self.assertIn(s3, shift_list)

    def test_get_volunteer_shift_by_id(self):

        u1 = User.objects.create_user('Yoshi')
        u2 = User.objects.create_user('John')

        v1 = Volunteer(
            first_name="Yoshi",
            last_name="Turtle",
            address="Mario Land",
            city="Nintendo Land",
            state="Nintendo State",
            country="Nintendo Nation",
            phone_number="2374983247",
            email="yoshi@nintendo.com",
            user=u1
            )

        v2 = Volunteer(
            first_name="John",
            last_name="Doe",
            address="7 Alpine Street",
            city="Maplegrove",
            state="Wyoming",
            country="USA",
            phone_number="23454545",
            email="john@test.com",
            user=u2
            )

        v1.save()
        v2.save()

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )

        e1.save()

        j1 = Job(
            name="Software Developer",
            start_date="2012-10-22",
            end_date="2012-10-23",
            description="A software job",
            event=e1
            )

        j2 = Job(
            name="Systems Administrator",
            start_date="2012-9-1",
            end_date="2012-10-26",
            description="A systems administrator job",
            event=e1
            )

        j1.save()
        j2.save()

        s1 = Shift(
            date="2012-10-23",
            start_time="9:00",
            end_time="3:00",
            max_volunteers=1,
            job=j1
            )

        s2 = Shift(
            date="2012-10-23",
            start_time="10:00",
            end_time="4:00",
            max_volunteers=2,
            job=j1
            )

        s3 = Shift(
            date="2012-10-23",
            start_time="12:00",
            end_time="6:00",
            max_volunteers=4,
            job=j2
            )

        s1.save()
        s2.save()
        s3.save()

        # test cases where signed up
        register(v1.id, s1.id)
        register(v1.id, s2.id)
        register(v1.id, s3.id)

        register(v2.id, s1.id)
        register(v2.id, s2.id)
        register(v2.id, s3.id)

        self.assertEqual(
                        get_volunteer_shift_by_id(v1.id, s1.id),
                        VolunteerShift.objects.get(
                                                    volunteer_id=v1.id,
                                                    shift_id=s1.id
                                                    ))
        self.assertEqual(
                        get_volunteer_shift_by_id(v1.id, s2.id),
                        VolunteerShift.objects.get(
                            volunteer_id=v1.id,
                            shift_id=s2.id
                            )
                        )
        self.assertEqual(
                        get_volunteer_shift_by_id(v1.id, s3.id),
                        VolunteerShift.objects.get(
                            volunteer_id=v1.id,
                            shift_id=s3.id
                            )
                        )

        # self.assertEqual(get_volunteer_shift_by_id(v2.id, s1.id),
        # VolunteerShift.objects.get(volunteer_id=v2.id, shift_id=s1.id))
        # why does this throw DoesNotExist?
        self.assertEqual(
                        get_volunteer_shift_by_id(v2.id, s2.id),
                        VolunteerShift.objects.get(
                            volunteer_id=v2.id,
                            shift_id=s2.id
                            )
                        )
        self.assertEqual(
                        get_volunteer_shift_by_id(v2.id, s3.id),
                        VolunteerShift.objects.get(
                            volunteer_id=v2.id,
                            shift_id=s3.id
                            )
                        )

    def test_get_volunteer_shifts_with_hours(self):
        """ Test  get_volunteer_shifts_with_hours(v_id) """
        u1 = User.objects.create_user('Yoshi')
        u2 = User.objects.create_user('John')

        v1 = Volunteer(
            first_name="Yoshi",
            last_name="Turtle",
            address="Mario Land",
            city="Nintendo Land",
            state="Nintendo State",
            country="Nintendo Nation",
            phone_number="2374983247",
            email="yoshi@nintendo.com",
            user=u1
            )

        v2 = Volunteer(
            first_name="John",
            last_name="Doe",
            address="7 Alpine Street",
            city="Maplegrove",
            state="Wyoming",
            country="USA",
            phone_number="23454545",
            email="john@test.com",
            user=u2
            )

        v1.save()
        v2.save()

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )

        e1.save()

        j1 = Job(
            name="Software Developer",
            start_date="2012-10-22",
            end_date="2012-10-23",
            description="A software job",
            event=e1
            )

        j2 = Job(
            name="Systems Administrator",
            start_date="2012-9-1",
            end_date="2012-10-26",
            description="A systems administrator job",
            event=e1
            )

        j1.save()
        j2.save()

        s1 = Shift(
            date="2012-10-23",
            start_time="9:00",
            end_time="3:00",
            max_volunteers=1,
            job=j1
            )

        s2 = Shift(
            date="2012-10-23",
            start_time="10:00",
            end_time="4:00",
            max_volunteers=2,
            job=j1
            )

        s3 = Shift(
            date="2012-10-23",
            start_time="12:00",
            end_time="6:00",
            max_volunteers=4,
            job=j2
            )

        s1.save()
        s2.save()
        s3.save()

        self.assertIsNotNone(get_volunteer_shifts_with_hours(v1))
        self.assertIsNotNone(get_volunteer_shifts_with_hours(v2))

    def test_get_volunteers_by_shift_id(self):

        u1 = User.objects.create_user('Yoshi')
        u2 = User.objects.create_user('John')
        u3 = User.objects.create_user('Ash')

        v1 = Volunteer(
            first_name="Yoshi",
            last_name="Turtle",
            address="Mario Land",
            city="Nintendo Land",
            state="Nintendo State",
            country="Nintendo Nation",
            phone_number="2374983247",
            email="yoshi@nintendo.com",
            user=u1
            )

        v2 = Volunteer(
            first_name="John",
            last_name="Doe",
            address="7 Alpine Street",
            city="Maplegrove",
            state="Wyoming",
            country="USA",
            phone_number="23454545",
            email="john@test.com",
            user=u2
            )

        v3 = Volunteer(
            first_name="Ash",
            last_name="Ketchum",
            address="Pallet Town",
            city="Kanto",
            state="Gameboy",
            country="Japan",
            phone_number="23454545",
            email="ash@pikachu.com",
            user=u3
            )

        v1.save()
        v2.save()
        v3.save()

        e1 = Event(
            name="Open Source Event",
            start_date="2015-10-22",
            end_date="2015-10-26"
            )

        e1.save()

        j1 = Job(
            name="Software Developer",
            start_date="2015-10-22",
            end_date="2015-10-24",
            description="A software job",
            event=e1
            )

        j1.save()

        # shift with limited slots
        s1 = Shift(
            date="2015-10-23",
            start_time="1:00",
            end_time="3:00",
            max_volunteers=1,
            job=j1
            )

        # shift with multiple volunteers
        s2 = Shift(
            date="2015-10-22",
            start_time="9:00",
            end_time="11:00",
            max_volunteers=4,
            job=j1
            )

        # shift with no volunteers
        s3 = Shift(
            date="2015-10-24",
            start_time="2:00",
            end_time="11:00",
            max_volunteers=4,
            job=j1
            )

        s1.save()
        s2.save()
        s3.save()

        # sign up
        register(v3.id, s1.id)
        register(v1.id, s1.id)
        register(v1.id, s2.id) 
        register(v3.id, s2.id)
        register(v2.id, s2.id)

        # get volunteer lists 
        volunteer_list_for_shift_1 = get_volunteers_by_shift_id(s1.id)
        volunteer_list_for_shift_2 = get_volunteers_by_shift_id(s2.id)
        volunteer_list_for_shift_3 = get_volunteers_by_shift_id(s3.id)

        # test typical case
        self.assertEqual(len(volunteer_list_for_shift_1), 1)
        self.assertEqual(len(volunteer_list_for_shift_2), 3)
        self.assertEqual(len(volunteer_list_for_shift_3), 0)

        self.assertIn(v3, volunteer_list_for_shift_1)
        self.assertNotIn(v1, volunteer_list_for_shift_1)
        self.assertIn(v1, volunteer_list_for_shift_2)
        self.assertIn(v2, volunteer_list_for_shift_2)
        self.assertIn(v3, volunteer_list_for_shift_2)

        #test order
        self.assertEqual(volunteer_list_for_shift_2[0], v3)
        self.assertEqual(volunteer_list_for_shift_2[1], v2)
        self.assertEqual(volunteer_list_for_shift_2[2], v1)

    def test_get_logged_volunteers_by_shift_id(self):

        u1 = User.objects.create_user('Yoshi')
        u2 = User.objects.create_user('John')
        u3 = User.objects.create_user('Ash')

        v1 = Volunteer(
            first_name="Yoshi",
            last_name="Turtle",
            address="Mario Land",
            city="Nintendo Land",
            state="Nintendo State",
            country="Nintendo Nation",
            phone_number="2374983247",
            email="yoshi@nintendo.com",
            user=u1
            )

        v2 = Volunteer(
            first_name="John",
            last_name="Doe",
            address="7 Alpine Street",
            city="Maplegrove",
            state="Wyoming",
            country="USA",
            phone_number="23454545",
            email="john@test.com",
            user=u2
            )

        v3 = Volunteer(
            first_name="Ash",
            last_name="Ketchum",
            address="Pallet Town",
            city="Kanto",
            state="Gameboy",
            country="Japan",
            phone_number="23454545",
            email="ash@pikachu.com",
            user=u3
            )

        v1.save()
        v2.save()
        v3.save()

        e1 = Event(
            name="Open Source Event",
            start_date="2015-10-22",
            end_date="2015-10-26"
            )

        e1.save()

        j1 = Job(
            name="Software Developer",
            start_date="2015-10-22",
            end_date="2015-10-24",
            description="A software job",
            event=e1
            )

        j1.save()

        s1 = Shift(
            date="2015-10-23",
            start_time="1:00",
            end_time="4:00",
            max_volunteers=5,
            job=j1
            )

        s1.save()

        # sign up
        register(v3.id, s1.id)
        register(v1.id, s1.id)
        register(v2.id, s1.id)

        start_time = datetime.time(hour=1, minute=0)
        end_time = datetime.time(hour=2, minute=0)
        add_shift_hours(v1.id, s1.id, start_time, end_time)

        start_time = datetime.time(hour=2, minute=0)
        end_time = datetime.time(hour=3, minute=0)
        add_shift_hours(v3.id, s1.id, start_time, end_time)

        # get volunteer list
        logged_volunteer_list_for_shift = get_logged_volunteers_by_shift_id(s1.id)

        # test typical case and order
        self.assertEqual(len(logged_volunteer_list_for_shift), 2)
        self.assertEqual(logged_volunteer_list_for_shift[0].volunteer, v3)
        self.assertEqual(logged_volunteer_list_for_shift[1].volunteer, v1)

    def test_is_signed_up(self):

        u1 = User.objects.create_user('Yoshi')
        u2 = User.objects.create_user('John')

        v1 = Volunteer(
            first_name="Yoshi",
            last_name="Turtle",
            address="Mario Land",
            city="Nintendo Land",
            state="Nintendo State",
            country="Nintendo Nation",
            phone_number="2374983247",
            email="yoshi@nintendo.com",
            user=u1
            )

        v2 = Volunteer(
            first_name="John",
            last_name="Doe",
            address="7 Alpine Street",
            city="Maplegrove",
            state="Wyoming",
            country="USA",
            phone_number="23454545",
            email="john@test.com",
            user=u2
            )

        v1.save()
        v2.save()

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )

        e1.save()

        j1 = Job(
            name="Software Developer",
            start_date="2012-10-22",
            end_date="2012-10-23",
            description="A software job",
            event=e1
            )

        j2 = Job(
            name="Systems Administrator",
            start_date="2012-9-1",
            end_date="2012-10-26",
            description="A systems administrator job",
            event=e1
            )

        j1.save()
        j2.save()

        s1 = Shift(
            date="2012-10-23",
            start_time="9:00",
            end_time="3:00",
            max_volunteers=1,
            job=j1
            )

        s2 = Shift(
            date="2012-10-23",
            start_time="10:00",
            end_time="4:00",
            max_volunteers=2,
            job=j1
            )

        s3 = Shift(
            date="2012-10-23",
            start_time="12:00",
            end_time="6:00",
            max_volunteers=4,
            job=j2
            )

        s1.save()
        s2.save()
        s3.save()

        # test cases where not signed up yet
        self.assertFalse(is_signed_up(v1.id, s1.id))
        self.assertFalse(is_signed_up(v1.id, s2.id))
        self.assertFalse(is_signed_up(v1.id, s3.id))

        # test cases where signed up
        register(v1.id, s1.id)
        register(v1.id, s2.id)
        register(v1.id, s3.id)

        self.assertTrue(is_signed_up(v1.id, s1.id))
        self.assertTrue(is_signed_up(v1.id, s2.id))
        self.assertTrue(is_signed_up(v1.id, s3.id))

        # test case where more than one volunteer signs up for the same shift
        self.assertFalse(is_signed_up(v2.id, s1.id))
        self.assertFalse(is_signed_up(v2.id, s2.id))
        self.assertFalse(is_signed_up(v2.id, s3.id))

        register(v2.id, s2.id)
        register(v2.id, s3.id)

        self.assertFalse(is_signed_up(v2.id, s1.id))
        self.assertTrue(is_signed_up(v2.id, s2.id))
        self.assertTrue(is_signed_up(v2.id, s3.id))

    def test_register(self):

        ERROR_CODE_ALREADY_SIGNED_UP = "ERROR_CODE_ALREADY_SIGNED_UP"
        ERROR_CODE_NO_SLOTS_REMAINING = "ERROR_CODE_NO_SLOTS_REMAINING"

        u1 = User.objects.create_user('Yoshi')
        u2 = User.objects.create_user('John')

        v1 = Volunteer(
                    first_name="Yoshi",
                    last_name="Turtle",
                    address="Mario Land",
                    city="Nintendo Land",
                    state="Nintendo State",
                    country="Nintendo Nation",
                    phone_number="2374983247",
                    email="yoshi@nintendo.com",
                    user=u1
                    )

        v2 = Volunteer(
                    first_name="John",
                    last_name="Doe",
                    address="7 Alpine Street",
                    city="Maplegrove",
                    state="Wyoming",
                    country="USA",
                    phone_number="23454545",
                    email="john@test.com",
                    user=u2
                    )

        v1.save()
        v2.save()

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )

        e1.save()

        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )

        j2 = Job(
                name="Systems Administrator",
                start_date="2012-9-1",
                end_date="2012-10-26",
                description="A systems administrator job",
                event=e1
                )

        j1.save()
        j2.save()

        s1 = Shift(
                date="2012-10-23",
                start_time="9:00",
                end_time="3:00",
                max_volunteers=1,
                job=j1
                )

        s2 = Shift(
                date="2012-10-23",
                start_time="10:00",
                end_time="4:00",
                max_volunteers=2,
                job=j1
                )

        s3 = Shift(
                date="2012-10-23",
                start_time="12:00",
                end_time="6:00",
                max_volunteers=4,
                job=j2
                )

        s1.save()
        s2.save()
        s3.save()

        # test typical cases
        register(v1.id, s1.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=v1.id,
                                                        shift_id=s1.id
                                                        ))

        register(v1.id, s2.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=v1.id,
                                                        shift_id=s2.id
                                                        ))

        register(v1.id, s3.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=v1.id,
                                                        shift_id=s3.id
                                                        ))

        # test cases where volunteer tries to sign up for a shift
        # they are already signed up for
        self.assertEqual(register(v1.id, s1.id), ERROR_CODE_ALREADY_SIGNED_UP)
        self.assertEqual(register(v1.id, s2.id), ERROR_CODE_ALREADY_SIGNED_UP)
        self.assertEqual(register(v1.id, s3.id), ERROR_CODE_ALREADY_SIGNED_UP)

        # test case where more than one volunteer signs up for the same shift
        # v2 can't sign up for s1 because there are no slots remaining
        self.assertEqual(register(v2.id, s1.id), ERROR_CODE_NO_SLOTS_REMAINING)

        register(v2.id, s2.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=v2.id,
                                                        shift_id=s2.id
                                                        ))

        register(v2.id, s3.id)
        self.assertIsNotNone(VolunteerShift.objects.get(
                                                        volunteer_id=v2.id,
                                                        shift_id=s3.id
                                                        ))

        # test cases where a volunteer tries to sign up for a shift
        # they are already signed up for
        self.assertEqual(register(v2.id, s2.id), ERROR_CODE_ALREADY_SIGNED_UP)
        self.assertEqual(register(v2.id, s3.id), ERROR_CODE_ALREADY_SIGNED_UP)
