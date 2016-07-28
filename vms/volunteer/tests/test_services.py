import unittest
from organization.models import Organization
from volunteer.models import Volunteer
from shift.utils import create_volunteer_with_details, clear_objects

from volunteer.services import (delete_volunteer,
                                delete_volunteer_resume,
                                get_all_volunteers,
                                get_volunteer_by_id,
                                get_volunteer_resume_file_url,
                                get_volunteers_ordered_by_first_name,
                                has_resume_file,
                                search_volunteers)


class VolunteerMethodTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        volunteer_1 = ['Yoshi',"Yoshi","Turtle","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","yoshi@nintendo.com"]
        volunteer_2 = ['John',"John","Doe","7 Alpine Street","Maplegrove","Wyoming","USA","23454545","john@test.com"]
        volunteer_3 = ['Ash',"Ash","Doe","Pallet Town","Kanto","Gameboy","Japan","23454545","ash@pikachu.com"]

        cls.v1 = create_volunteer_with_details(volunteer_1)
        cls.v2 = create_volunteer_with_details(volunteer_2)
        cls.v3 = create_volunteer_with_details(volunteer_3)

    @classmethod
    def tearDownClass(cls):
        # Destroys all objects created
        clear_objects()

    def test_delete_volunteer_resume(self):
        """ Tests delete_volunteer_resume(volunteer_id) """

        self.v1.resume_file="MyResume.pdf"
        self.v1.save()

        self.assertTrue(delete_volunteer_resume(self.v1.id))
        self.assertFalse(delete_volunteer(100))

    def test_get_all_volunteers(self):
        # Tests get_all_volunteers()
        vol_list = get_all_volunteers()

        # test typical cases
        self.assertIsNotNone(vol_list)
        self.assertTrue(len(vol_list), 3)
        self.assertIn(self.v1, vol_list)
        self.assertIn(self.v2, vol_list)
        self.assertIn(self.v3, vol_list)

    def test_get_volunteer_by_id(self):

        # test typical cases
        self.assertIsNotNone(get_volunteer_by_id(self.v1.id))
        self.assertIsNotNone(get_volunteer_by_id(self.v2.id))
        self.assertIsNotNone(get_volunteer_by_id(self.v3.id))

        self.assertEqual(get_volunteer_by_id(self.v1.id), self.v1)
        self.assertEqual(get_volunteer_by_id(self.v2.id), self.v2)
        self.assertEqual(get_volunteer_by_id(self.v3.id), self.v3)

        # test non-existant cases
        self.assertIsNone(get_volunteer_by_id(100))
        self.assertIsNone(get_volunteer_by_id(200))
        self.assertIsNone(get_volunteer_by_id(300))
        self.assertIsNone(get_volunteer_by_id(400))

        self.assertNotEqual(get_volunteer_by_id(100), self.v1)
        self.assertNotEqual(get_volunteer_by_id(200), self.v1)
        self.assertNotEqual(get_volunteer_by_id(300), self.v2)
        self.assertNotEqual(get_volunteer_by_id(400), self.v2)

    def test_get_volunteer_resume_file_url(self):

        self.v1.resume_file="MyResume.pdf"
        self.v1.save()

        # test typical cases
        self.assertIsNotNone(get_volunteer_resume_file_url(self.v1.id))
        self.assertEqual(
            get_volunteer_resume_file_url(self.v1.id),
            self.v1.resume_file.url
            )

        # test non-existant cases
        self.assertNotEqual(get_volunteer_resume_file_url(self.v1.id),
                            "resumes/DifferentResume.pdf"
                            )
        self.assertNotEqual(get_volunteer_resume_file_url(self.v1.id),
                            "resumes/AnotherResume.pdf"
                            )

    def test_get_volunteers_ordered_by_first_name(self):

        # test typical cases
        volunteer_list = get_volunteers_ordered_by_first_name()
        self.assertIsNotNone(volunteer_list)
        self.assertIn(self.v1, volunteer_list)
        self.assertIn(self.v2, volunteer_list)
        self.assertIn(self.v3, volunteer_list)
        self.assertEqual(len(volunteer_list), 3)

        # test if in correct order
        self.assertEqual(volunteer_list[0], self.v3)
        self.assertEqual(volunteer_list[1], self.v2)
        self.assertEqual(volunteer_list[2], self.v1)

    def test_has_resume_file(self):

        self.v1.resume_file="MyResume.pdf"
        self.v3.resume_file=""
        self.v1.save()
        self.v3.save()

        # test typical cases
        self.assertTrue(has_resume_file(self.v1.id))

        # test non-existant cases
        self.assertFalse(has_resume_file(self.v2.id))
        self.assertFalse(has_resume_file(self.v3.id))

    def test_search_volunteers(self):

        o1 = Organization(name="Apple")
        o2 = Organization(name="Google")

        o1.save()
        o2.save()

        self.v1.organization=o1
        self.v2.organization=o2
        self.v3.unlisted_organization="Government of Canada"

        self.v1.save()
        self.v2.save()
        self.v3.save()

        # if no search parameters are given,
        # it returns all volunteers
        search_list = search_volunteers("", "", "", "", "", "")
        self.assertNotEqual(search_list, False)
        self.assertEqual(len(search_list), 3)
        self.assertIn(self.v1, search_list)
        self.assertIn(self.v2, search_list)
        self.assertIn(self.v3, search_list)

        search_list = search_volunteers(None, None, None, None, None, None)
        self.assertNotEqual(search_list, False)
        self.assertEqual(len(search_list), 3)
        self.assertIn(self.v1, search_list)
        self.assertIn(self.v2, search_list)
        self.assertIn(self.v3, search_list)

        # test exact search
        search_list = search_volunteers(
                                        "Yoshi",
                                        "Turtle",
                                        "Nintendo Land",
                                        "Nintendo State",
                                        "Nintendo Nation",
                                        "Apple"
                                        )
        self.assertNotEqual(search_list, False)
        self.assertEqual(len(search_list), 1)
        self.assertIn(self.v1, search_list)
        self.assertNotIn(self.v2, search_list)
        self.assertNotIn(self.v3, search_list)

        # test partial search
        search_list = search_volunteers("Yoshi", None, None, None, None, None)
        self.assertNotEqual(search_list, False)
        self.assertEqual(len(search_list), 1)
        self.assertIn(self.v1, search_list)
        self.assertNotIn(self.v2, search_list)
        self.assertNotIn(self.v3, search_list)

        search_list = search_volunteers(None, "Doe", None, None, None, None)
        self.assertNotEqual(search_list, False)
        self.assertEqual(len(search_list), 2)
        self.assertIn(self.v3, search_list)
        self.assertIn(self.v2, search_list)

        # test no search matches
        search_list = search_volunteers(
                                        "Billy",
                                        "Doe",
                                        "Montreal",
                                        "Quebec",
                                        "Canada",
                                        "Ubisoft"
                                        )
        self.assertEqual(len(search_list), 0)
        self.assertNotIn(self.v1, search_list)
        self.assertNotIn(self.v2, search_list)
        self.assertNotIn(self.v3, search_list)

class DeleteVolunteerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        volunteer_1 = ['Margaret',"Yoshi","Turtle","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","yoshi1@nintendo.com"]
        volunteer_2 = ['Miu',"John","Doe","7 Alpine Street","Maplegrove","Wyoming","USA","23454545","john1@test.com"]
        volunteer_3 = ['Brock',"Ash","Ketchum","Pallet Town","Kanto","Gameboy","Japan","23454545","ash1@pikachu.com"]

        cls.v1 = create_volunteer_with_details(volunteer_1)
        cls.v2 = create_volunteer_with_details(volunteer_2)
        cls.v3 = create_volunteer_with_details(volunteer_3)

    def test_delete_volunteer(self):

        self.assertTrue(delete_volunteer(self.v1.id))
        self.assertTrue(delete_volunteer(self.v2.id))
        self.assertTrue(delete_volunteer(self.v3.id))
        self.assertFalse(delete_volunteer(100))
        self.assertFalse(delete_volunteer(200))
        self.assertFalse(delete_volunteer(300))
