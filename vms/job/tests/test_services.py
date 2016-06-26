from django.test import TestCase
import datetime
from datetime import date

from shift.services import register, create_shift_with_details
from volunteer.services import create_volunteer_with_details
from event.services import create_event_with_details
from job.services import (
                            delete_job,
                            check_edit_job,
                            get_job_by_id,
                            get_jobs_by_event_id,
                            get_jobs_ordered_by_title,
                            get_signed_up_jobs_for_volunteer,
                            remove_empty_jobs_for_volunteer,
                            create_job_with_details
                            )


class JobMethodTests(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_delete_job(self):
        """ Test delete_job(job_id) """

        event_1 = ["Software Conference","2012-10-22","2012-10-25"]
        e1 = create_event_with_details(event_1)

        job_1 = ["Software Developer","2012-10-22","2012-10-23","A software job",e1]
        job_2 = ["Systems Administrator","2012-9-1","2012-10-26","A systems administrator job",e1]
        job_3 = ["Project Manager","2012-1-2","2012-2-2","A management job",e1]

        j1 = create_job_with_details(job_1)
        j2 = create_job_with_details(job_2)
        j3 = create_job_with_details(job_3)

        # test typical cases
        self.assertTrue(delete_job(j1.id))
        self.assertTrue(delete_job(j2.id))
        self.assertTrue(delete_job(j3.id))
        self.assertFalse(delete_job(100))
        self.assertFalse(delete_job(200))
        self.assertFalse(delete_job(300))

    def test_check_edit_job(self):

        event_1 = ["Software Conference","2012-10-3","2012-10-24"]
        e1 = create_event_with_details(event_1)

        job_1 = ["Software Developer","2012-10-22","2012-10-23","A software job",e1]
        job_2 = ["Systems Administrator","2012-10-8","2012-10-16","A systems administrator job",e1]

        j1 = create_job_with_details(job_1)
        j2 = create_job_with_details(job_2)

        shift_1 = ["2012-10-23","1:00","3:00",5,j1]
        shift_2 = ["2012-10-25","2:00","4:00",5,j1]

        s1 = create_shift_with_details(shift_1)
        s2 = create_shift_with_details(shift_2)

        # test typical cases

        start_date1 = datetime.date(2012, 10, 23)
        start_date2 = datetime.date(2012, 10, 25)
        start_date3 = datetime.date(2012, 10, 2)
        start_date4 = datetime.date(2013, 10, 8)
        start_date5 = datetime.date(2015, 11, 4)
        start_date6 = datetime.date(2013, 11, 1)
        stop_date1 = datetime.date(2012, 10, 28)
        stop_date2 = datetime.date(2012, 10, 29)
        stop_date3 = datetime.date(2012, 10, 24)
        stop_date4 = datetime.date(2013, 10, 20)
        stop_date5 = datetime.date(2015, 11, 6)
        stop_date6 = datetime.date(2013, 11, 7)

        out1 = check_edit_job(j1.id, start_date1, stop_date1)
        out2 = check_edit_job(j1.id, start_date2, stop_date2)
        out3 = check_edit_job(j1.id, start_date3, stop_date3)
        out4 = check_edit_job(j1.id, start_date4, stop_date4)
        out5 = check_edit_job(j2.id, start_date5, stop_date5)
        out6 = check_edit_job(100, start_date6, stop_date6)

        self.assertTrue(out1['result'])
        self.assertFalse(out2['result'])
        self.assertFalse(out3['result'])
        self.assertFalse(out4['result'])
        self.assertTrue(out5['result'])
        self.assertFalse(out6['result'])

    def test_get_job_by_id(self):

        event_1 = ["Software Conference","2012-10-22","2012-10-25"]
        e1 = create_event_with_details(event_1)

        job_1 = ["Software Developer","2012-10-22","2012-10-23","A software job",e1]
        job_2 = ["Systems Administrator","2012-9-1","2012-10-26","A systems administrator job",e1]
        job_3 = ["Project Manager","2012-1-2","2012-2-2","A management job",e1]

        j1 = create_job_with_details(job_1)
        j2 = create_job_with_details(job_2)
        j3 = create_job_with_details(job_3)

        # test typical cases
        self.assertIsNotNone(get_job_by_id(j1.id))
        self.assertIsNotNone(get_job_by_id(j2.id))
        self.assertIsNotNone(get_job_by_id(j3.id))

        self.assertEqual(get_job_by_id(j1.id), j1)
        self.assertEqual(get_job_by_id(j2.id), j2)
        self.assertEqual(get_job_by_id(j3.id), j3)

        # test non-existant cases
        self.assertIsNone(get_job_by_id(100))
        self.assertIsNone(get_job_by_id(200))
        self.assertIsNone(get_job_by_id(300))
        self.assertIsNone(get_job_by_id(400))

        self.assertNotEqual(get_job_by_id(100), j1)
        self.assertNotEqual(get_job_by_id(100), j2)
        self.assertNotEqual(get_job_by_id(100), j3)
        self.assertNotEqual(get_job_by_id(200), j1)
        self.assertNotEqual(get_job_by_id(200), j2)
        self.assertNotEqual(get_job_by_id(200), j3)
        self.assertNotEqual(get_job_by_id(300), j1)
        self.assertNotEqual(get_job_by_id(300), j2)
        self.assertNotEqual(get_job_by_id(300), j3)

    def test_get_jobs_by_event_id(self):
        """ Test get_jobs_by_event_id(e_id) """

        event_1 = ["Software Conference","2012-10-22","2012-10-25"]
        e1 = create_event_with_details(event_1)

        job_1 = ["Software Developer","2012-10-22","2012-10-23","A software job",e1]
        job_2 = ["Systems Administrator","2012-9-1","2012-10-26","A systems administrator job",e1]
        job_3 = ["Project Manager","2012-1-2","2012-2-2","A management job",e1]

        j1 = create_job_with_details(job_1)
        j2 = create_job_with_details(job_2)
        j3 = create_job_with_details(job_3)

        # test typical case
        job_list = get_jobs_by_event_id(e1.id)
        self.assertIsNotNone(job_list)
        self.assertNotEqual(job_list, False)
        self.assertEqual(len(job_list), 3)
        self.assertIn(j1, job_list)
        self.assertIn(j2, job_list)
        self.assertIn(j3, job_list)

    def test_get_jobs_ordered_by_title(self):

        event_1 = ["Software Conference","2012-10-22","2012-10-25"]
        e1 = create_event_with_details(event_1)

        job_1 = ["Software Developer","2012-10-22","2012-10-23","A software job",e1]
        job_2 = ["Systems Administrator","2012-9-1","2012-10-26","A systems administrator job",e1]
        job_3 = ["Project Manager","2012-1-2","2012-2-2","A management job",e1]

        j1 = create_job_with_details(job_1)
        j2 = create_job_with_details(job_2)
        j3 = create_job_with_details(job_3)

        # test typical case
        job_list = get_jobs_ordered_by_title()
        self.assertIsNotNone(job_list)
        self.assertNotEqual(job_list, False)
        self.assertEqual(len(job_list), 3)
        self.assertIn(j1, job_list)
        self.assertIn(j2, job_list)
        self.assertIn(j3, job_list)

        # test order
        self.assertEqual(job_list[0].name, j3.name)
        self.assertEqual(job_list[1].name, j1.name)
        self.assertEqual(job_list[2].name, j2.name)

    def test_get_signed_up_jobs_for_volunteer(self):

        # creating events, jobs and shifts for volunteer registration
        event_1 = ["Software Conference","2012-10-22","2012-10-25"]
        e1 = create_event_with_details(event_1)

        job_1 = ["Software Developer","2012-10-22","2012-10-23","A software job",e1]
        job_2 = ["Systems Administrator","2012-9-1","2012-10-26","A systems administrator job",e1]

        j1 = create_job_with_details(job_1)
        j2 = create_job_with_details(job_2)

        shift_1 = ["2012-10-23","3:00","9:00",1,j1]
        shift_2 = ["2012-10-23","4:00","11:00",2,j1]
        shift_3 = ["2012-10-24","12:00","6:00",4,j2]

        s1 = create_shift_with_details(shift_1)
        s2 = create_shift_with_details(shift_2)
        s3 = create_shift_with_details(shift_3)

        # creating volunteers who would register for the shifts
        volunteer_1 = ['Yoshi',"Yoshi","Turtle","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","yoshi@nintendo.com"]
        volunteer_2 = ['John',"John","Doe","7 Alpine Street","Maplegrove","Wyoming","USA","23454545","john@test.com"]
        
        # volunteer who doesn't register for any shift
        volunteer_3 = ['Ash',"Ash","Ketchum","Pallet Town","Kanto","Gameboy","Japan","23454545","ash@pikachu.com"]

        v1 = create_volunteer_with_details(volunteer_1)
        v2 = create_volunteer_with_details(volunteer_2)
        v3 = create_volunteer_with_details(volunteer_3)

        # volunteer 1 registers for 3 shifts belonging to two jobs - registers for s3 first to check if sorting is successful
        register(v1.id, s3.id)
        register(v1.id, s2.id)
        register(v1.id, s1.id)
        
        # volunteer 2 registers for 2 shifts, where s1 has no available slots
        register(v2.id, s1.id)
        register(v2.id, s3.id)

        job_list_for_vol_1 = get_signed_up_jobs_for_volunteer(v1.id)
        job_list_for_vol_2 = get_signed_up_jobs_for_volunteer(v2.id)
        job_list_for_vol_3 = get_signed_up_jobs_for_volunteer(v3.id)

        # tests for returned jobs, their order and duplication for volunteer 1
        self.assertEqual(len(job_list_for_vol_1), 2)
        self.assertIn(j1.name, job_list_for_vol_1)
        self.assertIn(j2.name, job_list_for_vol_1)
        self.assertEqual(job_list_for_vol_1[0], j1.name)
        self.assertEqual(job_list_for_vol_1[1], j2.name)

        # tests for returned jobs for volunteer 2
        self.assertEqual(len(job_list_for_vol_2), 1)
        self.assertIn(j2.name, job_list_for_vol_2)
        self.assertNotIn(j1.name, job_list_for_vol_2)

        # test for returned jobs for unregistered volunteer 3
        self.assertEqual(len(job_list_for_vol_3), 0)

    def test_remove_empty_jobs_for_volunteer(self):

        event_1 = ["Software Conference","2012-10-22","2012-10-25"]
        e1 = create_event_with_details(event_1)

        #Job with shift that has slots available
        job_1 = ["Software Developer","2012-10-22","2012-10-23","A software job",e1]

        #Job with shift volunteer will have already signed up for
        job_2 = ["Systems Administrator","2012-9-1","2012-10-26","A systems administrator job",e1]

        #Job with shift that has no available slots
        job_3 = ["Project Manager","2012-1-2","2012-2-2","A management job",e1]

        #Job with no shifts
        job_4 = ["Information Technologist","2012-11-2","2012-12-2","An IT job",e1]

        j1 = create_job_with_details(job_1)
        j2 = create_job_with_details(job_2)
        j3 = create_job_with_details(job_3)
        j4 = create_job_with_details(job_3)
        
        shift_1 = ["2012-10-23","3:00","9:00",5,j1]
        shift_2 = ["2012-10-23","4:00","11:00",5,j2]
        shift_3 = ["2012-10-24","12:00","6:00",0,j3]

        s1 = create_shift_with_details(shift_1)
        s2 = create_shift_with_details(shift_2)
        s3 = create_shift_with_details(shift_3)
        
        volunteer_1 = ['Yoshi',"Yoshi","Turtle","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","yoshi@nintendo.com"]
        v1 = create_volunteer_with_details(volunteer_1)
        
        register(v1.id, s2.id)
        
        job_list = [j1, j2, j3, j4]
        job_list = remove_empty_jobs_for_volunteer(job_list, v1.id)

        #Only open and non empty jobs should be left
        self.assertIn(j1, job_list)
        self.assertNotIn(j2, job_list)
        self.assertNotIn(j3, job_list)
        self.assertNotIn(j4, job_list)
        