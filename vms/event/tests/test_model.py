# third party

# Django
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.test.testcases import TestCase

# local Django
from event.models import Event
from shift.utils import create_event_with_details
from pom.pages.eventsPage import EventsPage


class EventModelTests(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def create_event():
        event = ['event-name', '2050-05-24', '2050-05-28']
        created_event = create_event_with_details(event)
        return created_event

    def test_valid_model_create(self):
        event = ['event-name', '2050-05-24', '2050-05-28']
        create_event_with_details(event)

        # Check database for instance creation
        self.assertNotEqual(len(Event.objects.all()), 0)

        event_in_db = Event.objects.get(Q(name='event-name'))
        # Verify correctness
        self.assertEqual(event_in_db.name, event[0])
        self.assertEqual(str(event_in_db.start_date), event[1])
        self.assertEqual(str(event_in_db.end_date), event[2])

    def test_invalid_name_in_model_create(self):
        """
        Database test for model creation with invalid name.
        """
        event_data = ['event~name', '2050-05-21', '2050-05-24']
        event = create_event_with_details(event_data)
        self.assertRaisesRegexp(ValidationError, EventsPage.ENTER_VALID_VALUE, event.full_clean)

    # def test_invalid_start_date_in_model_create(self):
    #     """
    #      Database test for model creation with invalid start date.
    #     """
    #     This test need to be uncommented after clean method is defined for model.
    #     event_data = ['event-name', '2013-05-21', '2050-05-24']
    #     event = create_event_with_details(event_data)
    #     self.assertRaisesRegexp(ValidationError, EventsPage.ENTER_VALID_VALUE, event.full_clean)

    # def test_invalid_start_date_in_model_create(self):
    #     """
    #      Database test for model creation with invalid end date.
    #     """
    #     This test need to be uncommented after clean method is defined for model.
    #     event_data = ['event-name', '2050-05-21', '2013-05-24']
    #     event = create_event_with_details(event_data)
    #     self.assertRaisesRegexp(ValidationError, EventsPage.ENTER_VALID_VALUE, event.full_clean)

    def test_model_edit_with_valid_values(self):
        created_event = EventModelTests.create_event()

        # Check db for instance creation
        self.assertEqual(len(Event.objects.all()), 1)

        event_in_db = Event.objects.get(Q(name='event-name'))
        # Check if correct event retrieved
        self.assertEqual(event_in_db.name, created_event.name)

        # Edit job
        event_in_db.name = 'new-event-name'
        event_in_db.save()

        event_in_db = Event.objects.get(Q(name='new-event-name'))
        # Check if save is success
        self.assertEqual(event_in_db.name, 'new-event-name')
        self.assertEqual(len(Event.objects.all()), 1)

    def test_model_edit_with_invalid_values(self):
        created_event = EventModelTests.create_event()

        # Check db for instance creation
        self.assertEqual(len(Event.objects.all()), 1)

        event_in_db = Event.objects.get(Q(name='event-name'))
        # Check if correct event retrieved
        self.assertEqual(event_in_db.name, created_event.name)

        # Edit job
        event_in_db.name = 'new~event~name'
        event_in_db.save()

        self.assertRaisesRegexp(ValidationError,
                                EventsPage.ENTER_VALID_VALUE,
                                event_in_db.full_clean)

        # Check database for instance creation
        self.assertNotEqual(len(Event.objects.all()), 0)

    def test_model_delete(self):
        created_event = EventModelTests.create_event()

        # Check db for instance creation
        self.assertEqual(len(Event.objects.all()), 1)

        event_in_db = Event.objects.get(Q(name='event-name'))
        # Check if correct job retrieved
        self.assertEqual(event_in_db.name, created_event.name)

        # Delete job
        event_in_db.delete()

        # Check if delete is successful
        self.assertEqual(len(Event.objects.all()), 0)

    def test_model_representation(self):
        EventModelTests.create_event()

        # Check db for instance creation
        self.assertEqual(len(Event.objects.all()), 1)

        event_in_db = Event.objects.get(Q(name='event-name'))

        # Check __str__
        self.assertEqual(str(event_in_db), event_in_db.name)
