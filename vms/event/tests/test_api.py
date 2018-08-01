# third party
import json
from rest_framework.test import APITestCase

# Django
from django.test.testcases import TestCase
from django.urls import reverse

# local Django
from shift.utils import create_event_with_details


class ApiForVolaViewTestCase(APITestCase, TestCase):
    """
    Contains Tests for Vola API
    """

    def setUp(self):
        event = ['event', '2015-02-05', '2015-05-05', 'event-description']
        self.event_1 = create_event_with_details(event)
        self.event_1.city = 'city'
        self.event_1.state = 'state'
        self.event_1.country = 'country'
        self.event_1.address = 'address'
        self.event_1.venue = 'venue'
        self.event_1.save()
        self.expected_result_one = {'event_name': 'event',
                  'start_date': '2015-02-05',
                  'end_date': '2015-05-05',
                  'description': 'event-description',
                  'address': 'address',
                  'city': 'city',
                  'state': 'state',
                  'country': 'country',
                  'venue': 'venue'}

        event = ['eventq', '2050-02-05', '2050-05-05', 'eventq-description']
        self.event_2 = create_event_with_details(event)
        self.event_2.city = 'cityq'
        self.event_2.state = 'stateq'
        self.event_2.country = 'countryq'
        self.event_2.address = 'addressq'
        self.event_2.venue = 'venueq'
        self.event_2.save()
        self.expected_result_two = {'event_name': 'eventq',
                   'start_date': '2050-02-05',
                   'end_date': '2050-05-05',
                   'description': 'eventq-description',
                   'address': 'addressq',
                   'city': 'cityq',
                   'state': 'stateq',
                   'country': 'countryq',
                   'venue': 'venueq'}

    def test_api_for_vms_get(self):
        """Test GET request to provide data of all events"""
        url = reverse('event:vola_api')
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content), [self.expected_result_one, self.expected_result_two])

    def test_api_for_vms_post(self):
        """Test POST request to provide data of events after the specified date"""
        url = reverse('event:vola_api')
        data = {'date': '2018-06-13'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(json.loads(response.content), [self.expected_result_two])

