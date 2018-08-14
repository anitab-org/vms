# standard library
import unittest

# local Django
from organization.models import Organization
from organization.services import (get_organization_by_id,
                                   delete_organization,
                                   get_organization_by_name,
                                   get_organizations_ordered_by_name)
from shift.utils import (get_country_by_name, get_city_by_name,
                         get_state_by_name, clear_objects,
                         create_volunteer_with_details)


class OrganizationMethodTests(unittest.TestCase):
    @classmethod
    def setup_test_data(cls):
        cls.o1 = Organization(name="Google")
        cls.o2 = Organization(name="Yahoo")
        cls.o3 = Organization(name="Ubisoft")

        cls.o1.save()
        cls.o2.save()
        cls.o3.save()

    @classmethod
    def setUpClass(cls):
        cls.setup_test_data()

    @classmethod
    def tearDownClass(cls):
        # Destroys all objects created
        clear_objects()

    def test_get_organization_by_id(self):

        # test typical cases
        self.assertIsNotNone(get_organization_by_id(self.o1.id))
        self.assertIsNotNone(get_organization_by_id(self.o2.id))
        self.assertIsNotNone(get_organization_by_id(self.o3.id))

        self.assertEqual(get_organization_by_id(self.o1.id), self.o1)
        self.assertEqual(get_organization_by_id(self.o2.id), self.o2)
        self.assertEqual(get_organization_by_id(self.o3.id), self.o3)

        self.assertIsNone(get_organization_by_id(1000))
        self.assertIsNone(get_organization_by_id(2000))
        self.assertIsNone(get_organization_by_id(3000))

        self.assertNotEqual(get_organization_by_id(1000), self.o1)
        self.assertNotEqual(get_organization_by_id(2000), self.o1)
        self.assertNotEqual(get_organization_by_id(3000), self.o1)

        self.assertNotEqual(get_organization_by_id(1000), self.o2)
        self.assertNotEqual(get_organization_by_id(2000), self.o2)
        self.assertNotEqual(get_organization_by_id(3000), self.o2)

        self.assertNotEqual(get_organization_by_id(1000), self.o3)
        self.assertNotEqual(get_organization_by_id(2000), self.o3)
        self.assertNotEqual(get_organization_by_id(3000), self.o3)

    def test_get_organization_by_name(self):

        # test typical cases
        self.assertIsNotNone(get_organization_by_name(self.o1.name))
        self.assertIsNotNone(get_organization_by_name(self.o2.name))
        self.assertIsNotNone(get_organization_by_name(self.o3.name))

        self.assertEqual(get_organization_by_name(self.o1.name), self.o1)
        self.assertEqual(get_organization_by_name(self.o2.name), self.o2)
        self.assertEqual(get_organization_by_name(self.o3.name), self.o3)

        self.assertIsNone(get_organization_by_name("Apple"))
        self.assertIsNone(get_organization_by_name("IBM"))
        self.assertIsNone(get_organization_by_name("Cisco"))

        self.assertNotEqual(get_organization_by_name("Apple"), self.o1)
        self.assertNotEqual(get_organization_by_name("IBM"), self.o1)
        self.assertNotEqual(get_organization_by_name("Cisco"), self.o1)

        self.assertNotEqual(get_organization_by_name("Apple"), self.o2)
        self.assertNotEqual(get_organization_by_name("IBM"), self.o2)
        self.assertNotEqual(get_organization_by_name("Cisco"), self.o2)

        self.assertNotEqual(get_organization_by_name("Apple"), self.o3)
        self.assertNotEqual(get_organization_by_name("IBM"), self.o3)
        self.assertNotEqual(get_organization_by_name("Cisco"), self.o3)

    def test_get_organizations_ordered_by_name(self):

        # test typical cases
        organization_list = get_organizations_ordered_by_name()
        self.assertIsNotNone(organization_list)
        self.assertIn(self.o1, organization_list)
        self.assertIn(self.o2, organization_list)
        self.assertIn(self.o3, organization_list)
        self.assertEqual(len(organization_list), 3)

        # test order
        self.assertEqual(organization_list[0], self.o1)
        self.assertEqual(organization_list[1], self.o3)
        self.assertEqual(organization_list[2], self.o2)


class DeleteOrganizationTests(unittest.TestCase):
    @classmethod
    def setup_test_data(cls):
        cls.o1 = Organization(name="Google")
        cls.o2 = Organization(name="Yahoo")

        cls.o1.save()
        cls.o2.save()
        city_name = 'Bothell'
        state_name = 'Washington'
        country_name = 'United States'
        country = get_country_by_name(country_name)
        state = get_state_by_name(state_name)
        city = get_city_by_name(city_name)
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
        cls.v1 = create_volunteer_with_details(volunteer_1, cls.o2)

    @classmethod
    def setUpClass(cls):
        cls.setup_test_data()

    @classmethod
    def tearDownClass(cls):
        clear_objects()

    def test_delete_organization(self):
        self.assertTrue(delete_organization(self.o1.id))
        self.assertFalse(delete_organization(self.o2.id))
        self.assertFalse(delete_organization(1000))
