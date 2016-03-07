from django.test import TestCase
from django.contrib.auth.models import User
import datetime
from datetime import date

from event.models import Event
from job.models import Job
from shift.services import register
from shift.models import Shift
from volunteer.models import Volunteer
from event.services import (
        event_not_empty,
        delete_event,
        check_edit_event,
        get_event_by_id,
        get_events_ordered_by_name,
        get_events_by_date,
        get_event_by_shift_id,
        remove_empty_events_for_volunteer
        )


class EventMethodTests(TestCase):

    def test_event_not_empty(self):
        """ Test event_not_empty(event_id) """
        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )
        e2 = Event(
                name="Python Event",
                start_date="2013-11-12",
                end_date="2013-11-13"
                )
        e3 = Event(
                name="Django Event",
                start_date="2015-07-07",
                end_date="2015-07-08"
                )

        e1.save()
        e2.save()
        e3.save()

        self.assertTrue(event_not_empty(e1.id))
        self.assertTrue(event_not_empty(e2.id))
        self.assertTrue(event_not_empty(e3.id))
        self.assertFalse(event_not_empty(100))
        self.assertFalse(event_not_empty(200))
        self.assertFalse(event_not_empty(300))

    def test_get_event_by_shift_id(self):
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
        
        self.assertIsNotNone(get_event_by_shift_id(s1.id))
        self.assertIsNotNone(get_event_by_shift_id(s2.id))
        self.assertIsNotNone(get_event_by_shift_id(s3.id))


    def test_delete_event(self):
        """ Test delete_event(event_id) """

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )
        e2 = Event(
                name="Python Event",
                start_date="2013-11-12",
                end_date="2013-11-13"
                )
        e3 = Event(
                name="Django Event",
                start_date="2015-07-07",
                end_date="2015-07-08"
                )

        e1.save()
        e2.save()
        e3.save()

        self.assertTrue(delete_event(e1.id))
        self.assertTrue(delete_event(e2.id))
        self.assertTrue(delete_event(e3.id))
        self.assertFalse(delete_event(100))
        self.assertFalse(delete_event(200))
        self.assertFalse(delete_event(300))


    def test_check_edit_event(self):

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-3",
                end_date="2012-10-24"
                )

        e2 = Event(
                name="Python Event",
                start_date="2013-11-3",
                end_date="2013-11-15"
                )

        e1.save()
        e2.save()

        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )

        j2 = Job(
                name="Systems Administrator",
                start_date="2012-10-8",
                end_date="2012-10-16",
                description="A systems administrator job",
                event=e1
                )

        j1.save()
        j2.save()

        # test typical cases

        start_date1 = datetime.date(2012, 10, 8)
        start_date2 = datetime.date(2012, 10, 7)
        start_date3 = datetime.date(2012, 10, 15)
        start_date4 = datetime.date(2013, 10, 8)
        start_date5 = datetime.date(2015, 11, 4)
        start_date6 = datetime.date(2013, 11, 1)
        start_date7 = datetime.date(2012, 10, 7)
        stop_date1 = datetime.date(2012, 10, 23)
        stop_date2 = datetime.date(2012, 10, 22)
        stop_date3 = datetime.date(2012, 10, 26)
        stop_date4 = datetime.date(2013, 10, 23)
        stop_date5 = datetime.date(2015, 11, 6)
        stop_date6 = datetime.date(2013, 11, 7)
        stop_date7 = datetime.date(2013, 10, 22)

        out1 = check_edit_event(e1.id, start_date1, stop_date1)
        out2 = check_edit_event(e1.id, start_date2, stop_date2)
        out3 = check_edit_event(e1.id, start_date3, stop_date3)
        out4 = check_edit_event(e1.id, start_date4, stop_date4)
        out5 = check_edit_event(e2.id, start_date5, stop_date5)
        out6 = check_edit_event(100, start_date6, stop_date6)
        out7 = check_edit_event(e1.id, start_date7, stop_date7)

        self.assertTrue(out1['result'])
        self.assertFalse(out2['result'])
        self.assertFalse(out3['result'])
        self.assertFalse(out4['result'])
        self.assertTrue(out5['result'])
        self.assertFalse(out6['result'])
        self.assertTrue(out7['result'])


    def test_get_event_by_id(self):
        """ Test get_event_by_id(event_id) """

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )
        e2 = Event(
                name="Python Event",
                start_date="2013-11-12",
                end_date="2013-11-13"
                )
        e3 = Event(
                name="Django Event",
                start_date="2015-07-07",
                end_date="2015-07-08"
                )

        e1.save()
        e2.save()
        e3.save()

        # test typical cases
        self.assertIsNotNone(get_event_by_id(e1.id))
        self.assertIsNotNone(get_event_by_id(e2.id))
        self.assertIsNotNone(get_event_by_id(e3.id))

        self.assertEqual(get_event_by_id(e1.id), e1)
        self.assertEqual(get_event_by_id(e2.id), e2)
        self.assertEqual(get_event_by_id(e3.id), e3)

        self.assertIsNone(get_event_by_id(100))
        self.assertIsNone(get_event_by_id(200))
        self.assertIsNone(get_event_by_id(300))

        self.assertNotEqual(get_event_by_id(100), e1)
        self.assertNotEqual(get_event_by_id(200), e1)
        self.assertNotEqual(get_event_by_id(300), e1)

        self.assertNotEqual(get_event_by_id(100), e2)
        self.assertNotEqual(get_event_by_id(200), e2)
        self.assertNotEqual(get_event_by_id(300), e2)

        self.assertNotEqual(get_event_by_id(100), e3)
        self.assertNotEqual(get_event_by_id(200), e3)
        self.assertNotEqual(get_event_by_id(300), e3)

    def test_get_events_by_date(self):
        """ Test get_events_by_date(start_date, end_date) """

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )
        e2 = Event(
                name="Python Event",
                start_date="2013-11-12",
                end_date="2013-11-13"
                )
        e3 = Event(
                name="Django Event",
                start_date="2015-07-02",
                end_date="2015-07-03"
                )
        e4 = Event(
                name="Systers Event",
                start_date="2015-07-25",
                end_date="2015-08-08"
                )
        e5 = Event(
                name="Anita Borg Event",
                start_date="2015-07-07",
                end_date="2015-07-08"
                )

        e1.save()
        e2.save()
        e3.save()
        e4.save()
        e5.save()

        # test typical cases
        event_list = get_events_by_date('2015-07-01','2015-08-01')
        self.assertIsNotNone(event_list)
        
        self.assertIn(e3, event_list)
        self.assertIn(e4, event_list)
        self.assertIn(e5, event_list)
        self.assertEqual(len(event_list), 3)
        
        # test order
        self.assertEqual(event_list[0], e3)
        self.assertEqual(event_list[1], e5)
        self.assertEqual(event_list[2], e4)

    def test_get_events_ordered_by_name(self):
        """ Test get_events_ordered_by_name() """

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )
        e2 = Event(
                name="Python Event",
                start_date="2013-11-12",
                end_date="2013-11-13"
                )
        e3 = Event(
                name="Django Event",
                start_date="2015-07-07",
                end_date="2015-07-08"
                )
        e4 = Event(
                name="Systers Event",
                start_date="2015-07-07",
                end_date="2015-07-08"
                )
        e5 = Event(
                name="Anita Borg Event",
                start_date="2015-07-07",
                end_date="2015-07-08"
                )

        e1.save()
        e2.save()
        e3.save()
        e4.save()
        e5.save()

        # test typical cases
        event_list = get_events_ordered_by_name()
        self.assertIsNotNone(event_list)
        self.assertIn(e1, event_list)
        self.assertIn(e2, event_list)
        self.assertIn(e3, event_list)
        self.assertIn(e4, event_list)
        self.assertIn(e5, event_list)
        self.assertEqual(len(event_list), 5)

        # test order
        self.assertEqual(event_list[0], e5)
        self.assertEqual(event_list[1], e3)
        self.assertEqual(event_list[2], e1)
        self.assertEqual(event_list[3], e2)
        self.assertEqual(event_list[4], e4)

    def test_remove_empty_events_for_volunteer(self):

        #Event with job that has shift with open slots
        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-22",
                end_date="2012-10-23"
                )
        
        #Event with job and shift that volunteer already signed up for
        e2 = Event(
                name="Python Event",
                start_date="2013-11-12",
                end_date="2013-11-13"
                )
        
        #Event with job and shift that have no slots remaining
        e3 = Event(
                name="Django Event",
                start_date="2015-07-07",
                end_date="2015-07-08"
                )

        #Event with job that has no shifts
        e4 = Event(
                name="Systers Event",
                start_date="2015-07-07",
                end_date="2015-07-08"
                )

        #Event with no jobs
        e5 = Event(
                name="Anita Borg Event",
                start_date="2015-07-07",
                end_date="2015-07-08"
                )

        e1.save()
        e2.save()
        e3.save()
        e4.save()
        e5.save()
        
        #Job with shift that has slots available
        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )
        
        #Job with shift volunteer will have already signed up for  
        j2 = Job(
                name="Systems Administrator",
                start_date="2012-9-1",
                end_date="2012-10-26",
                description="A systems administrator job",
                event=e2
                )

        #Job with shift that has no available slots
        j3 = Job(
                name="Project Manager",
                start_date="2012-1-2",
                end_date="2012-2-2",
                description="A management job",
                event=e3
                )

        #Job with no shifts
        j4 = Job(
                name="Information Technologist",
                start_date="2012-11-2",
                end_date="2012-12-2",
                description="An IT job",
                event=e4
                )

        j1.save()
        j2.save()
        j3.save()
        j4.save()
        
        s1 = Shift(
                date="2012-10-23",
                start_time="9:00",
                end_time="3:00",
                max_volunteers=5,
                job=j1
                )

        s2 = Shift(
                date="2012-10-23",
                start_time="10:00",
                end_time="4:00",
                max_volunteers=5,
                job=j2
                )

        s3 = Shift(
                date="2012-10-23",
                start_time="12:00",
                end_time="6:00",
                max_volunteers=0,
                job=j3
                )

        s1.save()
        s2.save()
        s3.save()
        
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
        
        register(v1.id, s2.id)
        
        event_list = [e1, e2, e3, e4, e5]
        event_list = remove_empty_events_for_volunteer(event_list, v1.id)

        #Only events with jobs that have open slots should remain
        self.assertIn(e1, event_list)
        self.assertNotIn(e2, event_list)
        self.assertNotIn(e3, event_list)
        self.assertNotIn(e4, event_list)
        self.assertNotIn(e5, event_list)
