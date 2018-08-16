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
    """
    Contains database tests for
    - event create with valid and invalid values.
    - event edit with valid and invalid values.
    - event delete.
    - event mode representation.
    """

    def setUp(self):
        """
        Method consists of statements to be executed before
        start of each test.
        """
        pass

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

    def test_valid_model_create(self):
        """
        Database test for model creation with valid values.
        """
        event = {
            'name': 'event-name',
            'start_date': '2050-05-24',
            'end_date': '2050-05-28',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }
        create_event_with_details(event)

        # Check database for instance creation
        self.assertNotEqual(len(Event.objects.all()), 0)

        event_in_db = Event.objects.get(Q(name='event-name'))
        # Verify correctness
        self.assertEqual(event_in_db.name, event['name'])
        self.assertEqual(str(event_in_db.start_date), event['start_date'])
        self.assertEqual(str(event_in_db.end_date), event['end_date'])
        self.assertEqual(event_in_db.description, event['description'])
        self.assertEqual(event_in_db.address, event['address'])
        self.assertEqual(event_in_db.venue, event['venue'])

    def test_invalid_name_in_model_create(self):
        """
        Database test for model creation with invalid name.
        """
        event_data = {
            'name': 'event~name',
            'start_date': '2050-05-21',
            'end_date': '2050-05-28',
            'description': 'event-description',
            'address': 'event-address',
            'venue': 'event-venue'
        }
        event = create_event_with_details(event_data)

        self.assertRaisesRegexp(
            ValidationError,
            EventsPage.ENTER_VALID_VALUE,
            event.full_clean
        )

    # def test_invalid_start_date_in_model_create(self):
    #     """
    #      Database test for model creation with invalid start date.
    #     """
    #     This test need to be uncommented after clean method
    #     is defined for model.
    #     event_data = {
    #         'name': 'event-name',
    #         'start_date': '2013-05-21',
    #         'end_date': '2050-05-24',
    #         'description': 'event-description',
    #         'address': 'event-address',
    #         'venue': 'event-venue'
    #     }
    #     event = create_event_with_details(event_data)
    #     self.assertRaisesRegexp(
    #         ValidationError,
    #         EventsPage.ENTER_VALID_VALUE,
    #         event.full_clean
    # )

    # def test_invalid_end_date_in_model_create(self):
    #     """
    #      Database test for model creation with invalid end date.
    #     """
    #     This test need to be uncommented after clean method
    #     is defined for model.
    #     event_data = {
    #          'name': 'event-name',
    #          'start_date': '2050-05-21',
    #          'end_date': '2013-05-24',
    #          'description': 'event-description',
    #          'address': 'event-address',
    #          'venue': 'event-venue'
    #     }
    #     event = create_event_with_details(event_data)
    #     self.assertRaisesRegexp(
    #         ValidationError,
    #         EventsPage.ENTER_VALID_VALUE,
    #         event.full_clean
    #     )

    def test_model_edit_with_valid_values(self):
        """
        Database test for model edit with valid values.
        """
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
        """
        Database test for model edit with invalid values.
        """
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
        """
        Database test for model deletion.
        """
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
        """
        Database test for model representation.
        """
        EventModelTests.create_event()

        # Check db for instance creation
        self.assertEqual(len(Event.objects.all()), 1)

        event_in_db = Event.objects.get(Q(name='event-name'))

        # Check __str__
        self.assertEqual(str(event_in_db), event_in_db.name)
