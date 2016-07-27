import unittest
import datetime
from datetime import date

from shift.models import VolunteerShift
from shift.services import register
from shift.utils import (
        create_event_with_details,
        create_job_with_details,
        create_volunteer_with_details,
        create_shift_with_details,
        clear_objects
        )

from job.services import (
                            delete_job,
                            check_edit_job,
                            get_job_by_id,
                            get_jobs_by_event_id,
                            get_jobs_ordered_by_title,
                            get_signed_up_jobs_for_volunteer,
                            remove_empty_jobs_for_volunteer,
                            job_not_empty
                            )

def setUpModule():
    """
    - Creates objects which can be reused by multiple test classes
    - Creates jobs that can be used later for shift creation
    """

    global e1, e2, j1, j2, j3
    event_1 = ["Software Conference","2012-10-3","2012-11-25"]
    event_2 = ["Django Conference","2012-10-13","2012-11-25"]
    e1 = create_event_with_details(event_1)
    e2 = create_event_with_details(event_2)

    job_1 = ["Software Developer","2012-10-22","2012-10-25","A software job",e1]
    job_2 = ["Systems Administrator","2012-10-8","2012-10-16","A systems administrator job",e1]
    job_3 = ["Project Manager","2012-11-2","2012-11-12","A management job",e1]

    j1 = create_job_with_details(job_1)
    j2 = create_job_with_details(job_2)
    j3 = create_job_with_details(job_3)

def tearDownModule():
    # Destroys all objects created
    clear_objects()

class JobTests(unittest.TestCase):
    '''
    Contains tests which require only job objects, no shifts
    '''

    @classmethod
    def setup_test_data(cls):
        cls.e1 = e1
        cls.e2 = e2
        cls.j1 = j1
        cls.j2 = j2
        cls.j3 = j3

    @classmethod
    def setUpClass(cls):
        cls.setup_test_data()
        
    def test_get_job_by_id(self):
        """ Uses jobs j1,j2,j3 """

        # test typical cases
        self.assertIsNotNone(get_job_by_id(self.j1.id))
        self.assertIsNotNone(get_job_by_id(self.j2.id))
        self.assertIsNotNone(get_job_by_id(self.j3.id))

        self.assertEqual(get_job_by_id(self.j1.id), self.j1)
        self.assertEqual(get_job_by_id(self.j2.id), self.j2)
        self.assertEqual(get_job_by_id(self.j3.id), self.j3)

        # test non-existant cases
        self.assertIsNone(get_job_by_id(100))
        self.assertIsNone(get_job_by_id(200))

    def test_job_not_empty(self):
        """ Test job_not_empty(j_id) 
        Uses jobs j1,j2 """
        self.assertTrue(job_not_empty(self.j1.id))
        self.assertTrue(job_not_empty(self.j2.id))
        self.assertFalse(job_not_empty(100))

    def test_get_jobs_by_event_id(self):
        """ Test get_jobs_by_event_id(e_id) 
        Uses jobs j1,j2,j3 and event e1, e2 """

        # test typical case
        job_list = get_jobs_by_event_id(self.e1.id)
        job_list_2 = get_jobs_by_event_id(self.e2.id)
        self.assertIsNotNone(job_list)
        self.assertNotEqual(job_list, False)
        self.assertEqual(len(job_list), 3)
        self.assertEqual(len(job_list_2), 0)
        self.assertIn(self.j1, job_list)
        self.assertIn(self.j2, job_list)
        self.assertIn(self.j3, job_list)

    def test_get_jobs_ordered_by_title(self):
        """ Uses jobs j1,j2,j3 """

        # test typical case
        job_list = get_jobs_ordered_by_title()
        self.assertIsNotNone(job_list)
        self.assertNotEqual(job_list, False)
        self.assertEqual(len(job_list), 3)
        self.assertIn(self.j1, job_list)
        self.assertIn(self.j2, job_list)
        self.assertIn(self.j3, job_list)

        # test order
        self.assertEqual(job_list[0].name, self.j3.name)
        self.assertEqual(job_list[1].name, self.j1.name)
        self.assertEqual(job_list[2].name, self.j2.name)

class DeleteJobTest(unittest.TestCase):

    @classmethod
    def setup_test_data(cls):
        event_1 = ["Software Conference","2012-10-3","2012-10-24"]
        cls.e1 = create_event_with_details(event_1)

        job_1 = ["Software Developer","2012-10-22","2012-10-23","A software job",e1]
        job_2 = ["Systems Administrator","2012-10-8","2012-10-16","A systems administrator job",e1]

        cls.j1 = create_job_with_details(job_1)
        cls.j2 = create_job_with_details(job_2)

        shift_1 = ["2012-10-23","1:00","3:00",1,cls.j1]
        cls.s1 = create_shift_with_details(shift_1)

    @classmethod
    def setUpClass(cls):
        cls.setup_test_data()

    @classmethod
    def tearDownClass(cls):
        cls.s1.delete()
        cls.j1.delete()

    def test_delete_job(self):
        """ Test delete_job(job_id) """

        # test typical cases
        self.assertFalse(delete_job(self.j1.id))
        self.assertTrue(delete_job(self.j2.id))
        self.assertFalse(delete_job(100))
        self.assertFalse(delete_job(200))

class JobWithShiftTests(unittest.TestCase):
    '''
    Contains tests which require shift objects
    '''

    @classmethod
    def setup_test_data(cls):
        cls.e1 = e1
        cls.j1 = j1
        cls.j3 = j3

        # job with no shifts
        cls.j2 = j2

        # job with shift which has no slot
        job_4 = ["Information Technologist","2012-11-2","2012-12-2","An IT job",e1]
        cls.j4 = create_job_with_details(job_4)
        
        shift_1 = ["2012-10-23","1:00","3:00",1,cls.j1]
        shift_2 = ["2012-10-25","2:00","4:00",2,cls.j1]
        shift_3 = ["2012-10-24","12:00","18:00",4,cls.j3]

        # shift with no slots
        shift_4 = ["2012-11-7","12:00","18:00",1,cls.j4]

        cls.s1 = create_shift_with_details(shift_1)
        cls.s2 = create_shift_with_details(shift_2)
        cls.s3 = create_shift_with_details(shift_3)
        cls.s4 = create_shift_with_details(shift_4)

        # creating volunteers who would register for the shifts
        volunteer_1 = ['Yoshi',"Yoshi","Turtle","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","yoshi@nintendo.com"]
        volunteer_2 = ['John',"John","Doe","7 Alpine Street","Maplegrove","Wyoming","USA","23454545","john@test.com"]
        volunteer_3 = ['Ash',"Ash","Ketchum","Pallet Town","Kanto","Gameboy","Japan","23454545","ash@pikachu.com"]

        cls.v1 = create_volunteer_with_details(volunteer_1)
        cls.v2 = create_volunteer_with_details(volunteer_2)
        cls.v3 = create_volunteer_with_details(volunteer_3)

    @classmethod
    def setUpClass(cls):
        cls.setup_test_data()

    def tearDown(self):
        # Delete all registered shifts
        VolunteerShift.objects.all().delete()

    def test_check_edit_job(self):
        """ Uses jobs j1,j2 """

        # test typical cases
        start_date1 = datetime.date(2012, 10, 23)
        start_date2 = datetime.date(2012, 10, 25)
        start_date3 = datetime.date(2012, 10, 2)
        start_date4 = datetime.date(2013, 10, 8)
        stop_date1 = datetime.date(2012, 10, 28)
        stop_date2 = datetime.date(2012, 10, 29)
        stop_date3 = datetime.date(2012, 10, 24)
        stop_date4 = datetime.date(2013, 10, 20)

        out1 = check_edit_job(self.j1.id, start_date1, stop_date1)
        out2 = check_edit_job(self.j1.id, start_date2, stop_date2)
        out3 = check_edit_job(self.j1.id, start_date3, stop_date3)
        out4 = check_edit_job(self.j1.id, start_date4, stop_date4)
        out5 = check_edit_job(self.j2.id, start_date1, stop_date1)
        out6 = check_edit_job(100, start_date1, stop_date1)

        self.assertTrue(out1['result'])
        self.assertFalse(out2['result'])
        self.assertFalse(out3['result'])
        self.assertFalse(out4['result'])
        self.assertTrue(out5['result'])
        self.assertFalse(out6['result'])

        self.assertEqual(out1['invalid_count'], 0)
        self.assertEqual(out2['invalid_count'], 1)
        self.assertEqual(out4['invalid_count'], 2)
        self.assertEqual(out5['invalid_count'], 0)

    def test_get_signed_up_jobs_for_volunteer(self):
        """ Uses jobs j1,j3, shifts s1,s2,s3 and volunteers v1,v2"""

        # volunteer 1 registers for 3 shifts belonging to two jobs - registers for s1 first to check if sorting is successful
        register(self.v1.id, self.s1.id)
        register(self.v1.id, self.s3.id)
        register(self.v1.id, self.s2.id)
        
        # volunteer 2 registers for 2 shifts, where s1 has no available slots
        register(self.v2.id, self.s1.id)
        register(self.v2.id, self.s3.id)

        job_list_for_vol_1 = get_signed_up_jobs_for_volunteer(self.v1.id)
        job_list_for_vol_2 = get_signed_up_jobs_for_volunteer(self.v2.id)
        job_list_for_vol_3 = get_signed_up_jobs_for_volunteer(self.v3.id)

        # tests for returned jobs, their order and duplication for volunteer 1
        self.assertEqual(len(job_list_for_vol_1), 2)
        self.assertIn(self.j1.name, job_list_for_vol_1)
        self.assertIn(self.j3.name, job_list_for_vol_1)
        self.assertEqual(job_list_for_vol_1[0], self.j3.name)
        self.assertEqual(job_list_for_vol_1[1], self.j1.name)

        # tests for returned jobs for volunteer 2
        self.assertEqual(len(job_list_for_vol_2), 1)
        self.assertIn(self.j3.name, job_list_for_vol_2)
        self.assertNotIn(self.j1.name, job_list_for_vol_2)

        # test for returned jobs for unregistered volunteer 3
        self.assertEqual(len(job_list_for_vol_3), 0)

    def test_remove_empty_jobs_for_volunteer(self):
        """ Uses jobs j1,j2,j3,j4, shift s3 and volunteer v1 """
        
        # volunteer registers for a shift with multiple slots
        register(self.v1.id, self.s3.id)
        register(self.v2.id, self.s4.id)
        
        job_list = [self.j1, self.j2, self.j3, self.j4]
        job_list = remove_empty_jobs_for_volunteer(job_list, self.v1.id)

        #Only open and non empty jobs should be left
        self.assertIn(self.j1, job_list)
        self.assertNotIn(self.j2, job_list)
        self.assertNotIn(self.j3, job_list)
        self.assertNotIn(self.j4, job_list)
        