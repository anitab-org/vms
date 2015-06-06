from django.test import TestCase
from event.models import Event
from event.services import *

class EventMethodTests(TestCase):

    def test_event_not_empty(self):
        e1 = Event(name = "Open Source Event",
                start_date = "2012-10-22",
                end_date = "2012-10-23")
        e2 = Event(name = "Python Event",
                start_date = "2013-11-12",
                end_date = "2013-11-13")
        e3 = Event(name = "Django Event",
                start_date = "2015-07-07",
                end_date = "2015-07-08")

        e1.save()
        e2.save()
        e3.save()
        
        self.assertTrue(event_not_empty(e1.id))
        self.assertTrue(event_not_empty(e2.id))
        self.assertTrue(event_not_empty(e3.id))
        self.assertFalse(event_not_empty(100))
        self.assertFalse(event_not_empty(200))
        self.assertFalse(event_not_empty(300))

    def test_delete_event(self):
	
        e1 = Event(name = "Open Source Event",
                start_date = "2012-10-22",
                end_date = "2012-10-23")
        e2 = Event(name = "Python Event",
                start_date = "2013-11-12",
                end_date = "2013-11-13")
        e3 = Event(name = "Django Event",
                start_date = "2015-07-07",
                end_date = "2015-07-08")

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

        e1 = Event(name = "Open Source Event",
                start_date = "2012-10-22",
                end_date = "2012-10-23")
        e2 = Event(name = "Python Event",
                start_date = "2013-11-12",
                end_date = "2013-11-13")
        e3 = Event(name = "Django Event",
                start_date = "2015-07-07",
                end_date = "2015-07-08")

        e1.save()
        e2.save()
        e3.save()

        #test typical cases
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
		
    def test_get_events_ordered_by_name(self):

        e1 = Event(name = "Open Source Event",
                start_date = "2012-10-22",
                end_date = "2012-10-23")
        e2 = Event(name = "Python Event",
                start_date = "2013-11-12",
                end_date = "2013-11-13")
        e3 = Event(name = "Django Event",
                start_date = "2015-07-07",
                end_date = "2015-07-08")
        e4 = Event(name = "Systers Event",
                start_date = "2015-07-07",
                end_date = "2015-07-08")
        e5 = Event(name = "Anita Borg Event",
                start_date = "2015-07-07",
                end_date = "2015-07-08")

        e1.save()
        e2.save()
        e3.save()
        e4.save()
        e5.save()

        #test typical cases
        event_list = get_events_ordered_by_name()
        self.assertIsNotNone(event_list)
        self.assertIn(e1, event_list)
        self.assertIn(e2, event_list)
        self.assertIn(e3, event_list)
        self.assertIn(e4, event_list)
        self.assertIn(e5, event_list)
        self.assertEqual(len(event_list), 5)

        #test order
        self.assertEqual(event_list[0], e5)
        self.assertEqual(event_list[1], e3)
        self.assertEqual(event_list[2], e1)
        self.assertEqual(event_list[3], e2)
        self.assertEqual(event_list[4], e4)