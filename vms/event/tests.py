from django.test import TestCase

from event.models import Event
from job.models import Job
from shift.models import Shift
from event.services import (
        event_not_empty,
        delete_event,
        get_event_by_id,
        get_events_ordered_by_name,
        get_events_by_date,
        get_event_by_shift_id
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
