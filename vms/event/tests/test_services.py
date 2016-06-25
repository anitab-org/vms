from django.test import TestCase
import datetime
from datetime import date

from shift.services import register
from job.services import create_job_with_details
from shift.services import create_shift_with_details
from volunteer.services import create_volunteer_with_details
from event.services import (
        event_not_empty,
        delete_event,
        check_edit_event,
        get_event_by_id,
        get_events_ordered_by_name,
        get_events_by_date,
        get_event_by_shift_id,
        get_signed_up_events_for_volunteer,
        remove_empty_events_for_volunteer,
        create_event_with_details      
        )

class EventMethodTests(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_event_not_empty(self):
        """ Test event_not_empty(event_id) """

        event_1 = ["Open Source Event","2012-10-22","2012-10-23"]
        event_2 = ["Python Event","2013-11-12","2013-11-13"]
        event_3 = ["Django Event","2015-07-07","2015-07-08"]

        e1 = create_event_with_details(event_1)
        e2 = create_event_with_details(event_2)
        e3 = create_event_with_details(event_3)

        self.assertTrue(event_not_empty(e1.id))
        self.assertTrue(event_not_empty(e2.id))
        self.assertTrue(event_not_empty(e3.id))
        self.assertFalse(event_not_empty(100))
        self.assertFalse(event_not_empty(200))
        self.assertFalse(event_not_empty(300))

    def test_delete_event(self):
        """ Test delete_event(event_id) """

        event_1 = ["Open Source Event","2012-10-22","2012-10-23"]
        event_2 = ["Python Event","2013-11-12","2013-11-13"]
        event_3 = ["Django Event","2015-07-07","2015-07-08"]

        e1 = create_event_with_details(event_1)
        e2 = create_event_with_details(event_2)
        e3 = create_event_with_details(event_3)

        self.assertTrue(delete_event(e1.id))
        self.assertTrue(delete_event(e2.id))
        self.assertTrue(delete_event(e3.id))
        self.assertFalse(delete_event(100))
        self.assertFalse(delete_event(200))
        self.assertFalse(delete_event(300))

    def test_get_event_by_id(self):
        """ Test get_event_by_id(event_id) """

        event_1 = ["Open Source Event","2012-10-22","2012-10-23"]
        event_2 = ["Python Event","2013-11-12","2013-11-13"]
        event_3 = ["Django Event","2015-07-07","2015-07-08"]

        e1 = create_event_with_details(event_1)
        e2 = create_event_with_details(event_2)
        e3 = create_event_with_details(event_3)

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

        event_1 = ["Open Source Event","2012-10-22","2012-10-23"]
        event_2 = ["Python Event","2013-11-12","2013-11-13"]
        event_3 = ["Django Event","2015-07-02","2015-07-03"]
        event_4 = ["Systers Event","2015-07-25","2015-08-08"]
        event_5 = ["Anita Borg Event","2015-07-07","2015-07-08"]

        e1 = create_event_with_details(event_1)
        e2 = create_event_with_details(event_2)
        e3 = create_event_with_details(event_3)
        e4 = create_event_with_details(event_4)
        e5 = create_event_with_details(event_5)

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

        event_1 = ["Open Source Event","2012-10-22","2012-10-23"]
        event_2 = ["Python Event","2013-11-12","2013-11-13"]
        event_3 = ["Django Event","2015-07-07","2015-07-08"]
        event_4 = ["Systers Event","2015-07-07","2015-07-08"]
        event_5 = ["Anita Borg Event","2015-07-07","2015-07-08"]

        e1 = create_event_with_details(event_1)
        e2 = create_event_with_details(event_2)
        e3 = create_event_with_details(event_3)
        e4 = create_event_with_details(event_4)
        e5 = create_event_with_details(event_5)

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

    def test_get_event_by_shift_id(self):

        event_1 = ["Open Source Event","2012-10-22","2012-10-23"]
        e1 = create_event_with_details(event_1)

        job_1 = ["Software Developer","2012-10-22","2012-10-23","A software job",e1]
        job_2 = ["Systems Administrator","2012-9-1","2012-10-26","A systems administrator job",e1]

        j1 = create_job_with_details(job_1)
        j2 = create_job_with_details(job_2)

        shift_1 = ["2012-10-23","9:00","3:00",1,j1]
        shift_2 = ["2012-10-23","10:00","4:00",2,j1]
        shift_3 = ["2012-10-23","12:00","6:00",4,j2]

        s1 = create_shift_with_details(shift_1)
        s2 = create_shift_with_details(shift_2)
        s3 = create_shift_with_details(shift_3)

        self.assertIsNotNone(get_event_by_shift_id(s1.id))
        self.assertIsNotNone(get_event_by_shift_id(s2.id))
        self.assertIsNotNone(get_event_by_shift_id(s3.id))

    def test_check_edit_event(self):

        event_1 = ["Open Source Event","2012-10-3","2012-10-24"]
        event_2 = ["Python Event","2013-11-3","2013-11-15"]

        e1 = create_event_with_details(event_1)
        e2 = create_event_with_details(event_2)

        job_1 = ["Software Developer","2012-10-22","2012-10-23","A software job",e1]
        job_2 = ["Systems Administrator","2012-10-8","2012-10-16","A systems administrator job",e1]

        j1 = create_job_with_details(job_1)
        j2 = create_job_with_details(job_2)

        # test typical cases

        start_date1 = datetime.date(2012, 10, 8)
        start_date2 = datetime.date(2012, 10, 7)
        start_date3 = datetime.date(2012, 10, 15)
        start_date4 = datetime.date(2013, 10, 8)
        start_date5 = datetime.date(2015, 11, 4)
        start_date6 = datetime.date(2013, 11, 1)
        start_date7 = datetime.date(2012, 10, 7)
        stop_date1 = datetime.date(2012, 10, 23)
        stop_date2 = datetime.date(2012, 10, 22)
        stop_date3 = datetime.date(2012, 10, 26)
        stop_date4 = datetime.date(2013, 10, 23)
        stop_date5 = datetime.date(2015, 11, 6)
        stop_date6 = datetime.date(2013, 11, 7)
        stop_date7 = datetime.date(2013, 10, 22)

        out1 = check_edit_event(e1.id, start_date1, stop_date1)
        out2 = check_edit_event(e1.id, start_date2, stop_date2)
        out3 = check_edit_event(e1.id, start_date3, stop_date3)
        out4 = check_edit_event(e1.id, start_date4, stop_date4)
        out5 = check_edit_event(e2.id, start_date5, stop_date5)
        out6 = check_edit_event(100, start_date6, stop_date6)
        out7 = check_edit_event(e1.id, start_date7, stop_date7)

        self.assertTrue(out1['result'])
        self.assertFalse(out2['result'])
        self.assertFalse(out3['result'])
        self.assertFalse(out4['result'])
        self.assertTrue(out5['result'])
        self.assertFalse(out6['result'])
        self.assertTrue(out7['result'])

    def test_get_signed_up_events_for_volunteer(self):

        # creating events, jobs and shifts for volunteer registration
        event_1 = ["django Event","2015-10-22","2015-10-25"]
        event_2 = ["Python Event","2015-11-11","2015-11-23"]

        e1 = create_event_with_details(event_1)
        e2 = create_event_with_details(event_2)

        job_1 = ["Software Developer","2012-10-22","2012-10-23","A software job",e1]
        job_2 = ["Systems Administrator","2015-11-12","2015-11-15","A systems administrator job",e2]

        j1 = create_job_with_details(job_1)
        j2 = create_job_with_details(job_2)

        shift_1 = ["2015-10-23","3:00","9:00",1,j1]
        shift_2 = ["2015-10-23","4:00","11:00",2,j1]
        shift_3 = ["2015-11-13","6:00","12:00",4,j2]

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

        # volunteer 1 registers for 3 shifts belonging to two events - registers for s3 first to check if sorting is successful
        register(v1.id, s3.id)
        register(v1.id, s2.id)
        register(v1.id, s1.id)

        # volunteer 2 registers for 2 shifts, where s1 has no available slots
        register(v2.id, s1.id)
        register(v2.id, s3.id)

        event_list_for_vol_1 = get_signed_up_events_for_volunteer(v1.id)
        event_list_for_vol_2 = get_signed_up_events_for_volunteer(v2.id)
        event_list_for_vol_3 = get_signed_up_events_for_volunteer(v3.id)

        # tests for returned events, their order and duplication for volunteer 1
        self.assertEqual(len(event_list_for_vol_1), 2)
        self.assertIn(e1.name, event_list_for_vol_1)
        self.assertIn(e2.name, event_list_for_vol_1)
        self.assertEqual(event_list_for_vol_1[0], e1.name)
        self.assertEqual(event_list_for_vol_1[1], e2.name)

        # tests for returned events for volunteer 2
        self.assertEqual(len(event_list_for_vol_2), 1)
        self.assertIn(e2.name, event_list_for_vol_2)
        self.assertNotIn(e1.name, event_list_for_vol_2)

        # test for returned events for unregistered volunteer 3
        self.assertEqual(len(event_list_for_vol_3), 0)

    def test_remove_empty_events_for_volunteer(self):

        #Event with job that has shift with open slots
        event_1 = ["Open Source Event","2012-10-22","2012-10-23"]

        #Event with job and shift that volunteer already signed up for
        event_2 = ["Python Event","2013-11-12","2013-11-13"]

        #Event with job and shift that have no slots remaining
        event_3 = ["Django Event","2015-07-07","2015-07-08"]

        #Event with job that has no shifts
        event_4 = ["Systers Event","2015-07-07","2015-07-08"]

        #Event with no jobs
        event_5 = ["Anita Borg Event","2015-07-07","2015-07-08"]

        e1 = create_event_with_details(event_1)
        e2 = create_event_with_details(event_2)
        e3 = create_event_with_details(event_3)
        e4 = create_event_with_details(event_4)
        e5 = create_event_with_details(event_5)

        #Job with shift that has slots available
        job_1 = ["Software Developer","2012-10-22","2012-10-23","A software job",e1]

        #Job with shift volunteer will have already signed up for
        job_2 = ["Systems Administrator","2012-9-1","2012-10-26","A systems administrator job",e2]

        #Job with shift that has no available slots
        job_3 = ["Project Manager","2012-1-2","2012-2-2","A management job",e3]

        #Job with no shifts
        job_4 = ["Information Technologist","2012-11-2","2012-12-2","An IT job",e4]

        j1 = create_job_with_details(job_1)
        j2 = create_job_with_details(job_2)
        j3 = create_job_with_details(job_3)
        j4 = create_job_with_details(job_4)

        shift_1 = ["2012-10-23","9:00","3:00",5,j1]
        shift_2 = ["2012-10-23","10:00","4:00",5,j2]
        shift_3 = ["2012-10-23","12:00","6:00",0,j3]

        s1 = create_shift_with_details(shift_1)
        s2 = create_shift_with_details(shift_2)
        s3 = create_shift_with_details(shift_3)

        # creating volunteer
        volunteer_1 = ['Yoshi',"Yoshi","Turtle","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","yoshi@nintendo.com"]
        v1 = create_volunteer_with_details(volunteer_1)
        
        register(v1.id, s2.id)
        
        event_list = [e1, e2, e3, e4, e5]
        event_list = remove_empty_events_for_volunteer(event_list, v1.id)

        #Only events with jobs that have open slots should remain
        self.assertIn(e1, event_list)
        self.assertNotIn(e2, event_list)
        self.assertNotIn(e3, event_list)
        self.assertNotIn(e4, event_list)
        self.assertNotIn(e5, event_list)
