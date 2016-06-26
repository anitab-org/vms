from django.test import TestCase

from organization.models import Organization
from volunteer.models import Volunteer
from shift.services import create_shift_with_details
from event.services import create_event_with_details
from job.services import create_job_with_details
from volunteer.services import (delete_volunteer,
                                delete_volunteer_resume,
                                get_all_volunteers,
                                get_volunteer_by_id,
                                get_volunteer_resume_file_url,
                                get_volunteers_ordered_by_first_name,
                                has_resume_file,
                                search_volunteers,
                                create_volunteer_with_details)


class VolunteerMethodTests(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_delete_volunteer(self):

        volunteer_1 = ['Yoshi',"Yoshi","Turtle","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","yoshi@nintendo.com"]
        volunteer_2 = ['John',"John","Doe","7 Alpine Street","Maplegrove","Wyoming","USA","23454545","john@test.com"]
        volunteer_3 = ['Ash',"Ash","Ketchum","Pallet Town","Kanto","Gameboy","Japan","23454545","ash@pikachu.com"]

        v1 = create_volunteer_with_details(volunteer_1)
        v2 = create_volunteer_with_details(volunteer_2)
        v3 = create_volunteer_with_details(volunteer_3)

        self.assertTrue(delete_volunteer(v1.id))
        self.assertTrue(delete_volunteer(v2.id))
        self.assertTrue(delete_volunteer(v3.id))
        self.assertFalse(delete_volunteer(100))
        self.assertFalse(delete_volunteer(200))
        self.assertFalse(delete_volunteer(300))

    def test_delete_volunteer_resume(self):
        """ Tests delete_volunteer_resume(volunteer_id) """

        volunteer_1 = ['John',"John","Doe","7 Alpine Street","Maplegrove","Wyoming","USA","23454545","john@test.com"]
        v1 = create_volunteer_with_details(volunteer_1)
        v1.resume_file="MyResume.pdf"
        v1.save()

        self.assertTrue(delete_volunteer_resume(v1.id))
        self.assertFalse(delete_volunteer(100))

    def test_get_all_volunteers(self):
        # Tests get_all_volunteers()

        volunteer_1 = ['Yoshi',"Yoshi","Turtle","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","yoshi@nintendo.com"]
        volunteer_2 = ['John',"John","Doe","7 Alpine Street","Maplegrove","Wyoming","USA","23454545","john@test.com"]
        volunteer_3 = ['Ash',"Ash","Ketchum","Pallet Town","Kanto","Gameboy","Japan","23454545","ash@pikachu.com"]

        v1 = create_volunteer_with_details(volunteer_1)
        v2 = create_volunteer_with_details(volunteer_2)
        v3 = create_volunteer_with_details(volunteer_3)

        # test typical cases
        self.assertIsNotNone(get_all_volunteers())

    def test_get_volunteer_by_id(self):

        volunteer_1 = ['Yoshi',"Yoshi","Turtle","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","yoshi@nintendo.com"]
        volunteer_2 = ['John',"John","Doe","7 Alpine Street","Maplegrove","Wyoming","USA","23454545","john@test.com"]
        volunteer_3 = ['Ash',"Ash","Ketchum","Pallet Town","Kanto","Gameboy","Japan","23454545","ash@pikachu.com"]

        v1 = create_volunteer_with_details(volunteer_1)
        v2 = create_volunteer_with_details(volunteer_2)
        v3 = create_volunteer_with_details(volunteer_3)

        # test typical cases
        self.assertIsNotNone(get_volunteer_by_id(v1.id))
        self.assertIsNotNone(get_volunteer_by_id(v2.id))
        self.assertIsNotNone(get_volunteer_by_id(v3.id))

        self.assertEqual(get_volunteer_by_id(v1.id), v1)
        self.assertEqual(get_volunteer_by_id(v2.id), v2)
        self.assertEqual(get_volunteer_by_id(v3.id), v3)

        # test non-existant cases
        self.assertIsNone(get_volunteer_by_id(100))
        self.assertIsNone(get_volunteer_by_id(200))
        self.assertIsNone(get_volunteer_by_id(300))
        self.assertIsNone(get_volunteer_by_id(400))

        self.assertNotEqual(get_volunteer_by_id(100), v1)
        self.assertNotEqual(get_volunteer_by_id(200), v1)
        self.assertNotEqual(get_volunteer_by_id(300), v2)
        self.assertNotEqual(get_volunteer_by_id(400), v2)

    def test_get_volunteer_resume_file_url(self):

        volunteer_1 = ['Yoshi',"Yoshi","Turtle","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","yoshi@nintendo.com"]
        v1 = create_volunteer_with_details(volunteer_1)

        v1.resume_file="MyResume.pdf"
        v1.save()

        # test typical cases
        self.assertIsNotNone(get_volunteer_resume_file_url(v1.id))
        self.assertEqual(
            get_volunteer_resume_file_url(v1.id),
            v1.resume_file.url
            )

        # test non-existant cases
        self.assertNotEqual(get_volunteer_resume_file_url(v1.id),
                            "resumes/DifferentResume.pdf"
                            )
        self.assertNotEqual(get_volunteer_resume_file_url(v1.id),
                            "resumes/AnotherResume.pdf"
                            )

    def test_get_volunteers_ordered_by_first_name(self):

        volunteer_1 = ['Yoshi',"Yoshi","Turtle","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","yoshi@nintendo.com"]
        volunteer_2 = ['John',"John","Doe","7 Alpine Street","Maplegrove","Wyoming","USA","23454545","john@test.com"]
        volunteer_3 = ['Ash',"Ash","Ketchum","Pallet Town","Kanto","Gameboy","Japan","23454545","ash@pikachu.com"]

        v1 = create_volunteer_with_details(volunteer_1)
        v2 = create_volunteer_with_details(volunteer_2)
        v3 = create_volunteer_with_details(volunteer_3)

        # test typical cases
        volunteer_list = get_volunteers_ordered_by_first_name()
        self.assertIsNotNone(volunteer_list)
        self.assertIn(v1, volunteer_list)
        self.assertIn(v2, volunteer_list)
        self.assertIn(v3, volunteer_list)
        self.assertEqual(len(volunteer_list), 3)

        # test if in correct order
        self.assertEqual(volunteer_list[0], v3)
        self.assertEqual(volunteer_list[1], v2)
        self.assertEqual(volunteer_list[2], v1)

    def test_has_resume_file(self):

        volunteer_1 = ['Yoshi',"Yoshi","Turtle","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","yoshi@nintendo.com"]
        volunteer_2 = ['John',"John","Doe","7 Alpine Street","Maplegrove","Wyoming","USA","23454545","john@test.com"]
        volunteer_3 = ['Ash',"Ash","Ketchum","Pallet Town","Kanto","Gameboy","Japan","23454545","ash@pikachu.com"]

        v1 = create_volunteer_with_details(volunteer_1)
        v2 = create_volunteer_with_details(volunteer_2)
        v3 = create_volunteer_with_details(volunteer_3)

        v1.resume_file="MyResume.pdf"
        v3.resume_file=""
        v1.save()
        v3.save()

        # test typical cases
        self.assertTrue(has_resume_file(v1.id))

        # test non-existant cases
        self.assertFalse(has_resume_file(v2.id))
        self.assertFalse(has_resume_file(v3.id))

    def test_search_volunteers(self):

        o1 = Organization(name="Apple")
        o2 = Organization(name="Google")

        o1.save()
        o2.save()

        volunteer_1 = ['Yoshi',"Yoshi","Doe","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","yoshi@nintendo.com"]
        volunteer_2 = ['John',"John","Doe","7 Alpine Street","Maplegrove","Wyoming","USA","23454545","john@test.com"]
        volunteer_3 = ['Ash',"Ash","Ketchum","Pallet Town","Kanto","Gameboy","Japan","23454545","ash@pikachu.com"]

        v1 = create_volunteer_with_details(volunteer_1)
        v2 = create_volunteer_with_details(volunteer_2)
        v3 = create_volunteer_with_details(volunteer_3)

        v1.organization=o1
        v2.organization=o2
        v3.unlisted_organization="Government of Canada"

        v1.save()
        v2.save()
        v3.save()

        # if no search parameters are given,
        # it returns all volunteers
        search_list = search_volunteers("", "", "", "", "", "")
        self.assertNotEqual(search_list, False)
        self.assertEqual(len(search_list), 3)
        self.assertIn(v1, search_list)
        self.assertIn(v2, search_list)
        self.assertIn(v3, search_list)

        search_list = search_volunteers(None, None, None, None, None, None)
        self.assertNotEqual(search_list, False)
        self.assertEqual(len(search_list), 3)
        self.assertIn(v1, search_list)
        self.assertIn(v2, search_list)
        self.assertIn(v3, search_list)

        # test exact search
        search_list = search_volunteers(
                                        "Yoshi",
                                        "Doe",
                                        "Nintendo Land",
                                        "Nintendo State",
                                        "Nintendo Nation",
                                        "Apple"
                                        )
        self.assertNotEqual(search_list, False)
        self.assertEqual(len(search_list), 1)
        self.assertIn(v1, search_list)
        self.assertNotIn(v2, search_list)
        self.assertNotIn(v3, search_list)

        # test partial search
        search_list = search_volunteers("Yoshi", None, None, None, None, None)
        self.assertNotEqual(search_list, False)
        self.assertEqual(len(search_list), 1)
        self.assertIn(v1, search_list)
        self.assertNotIn(v2, search_list)
        self.assertNotIn(v3, search_list)

        search_list = search_volunteers(None, "Doe", None, None, None, None)
        self.assertNotEqual(search_list, False)
        self.assertEqual(len(search_list), 2)
        self.assertIn(v1, search_list)
        self.assertIn(v2, search_list)

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
        self.assertNotIn(v1, search_list)
        self.assertNotIn(v2, search_list)
        self.assertNotIn(v3, search_list)
