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
from event.services import (
        event_not_empty,
        delete_event,
        check_edit_event,
        get_event_by_id,
        get_events_ordered_by_name,
        get_events_by_date,
        get_event_by_shift_id,
        get_signed_up_events_for_volunteer,
        remove_empty_events_for_volunteer    
        )

def setUpModule():
    """
    Creates events, jobs and shifts which can be reused by multiple test classes
    """

    global e1,e2,e3,e4,e5
    global j1,j2,j3,j4,j5
    global s1,s2,s3,s4

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

    job_1 = ["Software Developer","2012-10-22","2012-10-23","A software job",e1]
    job_2 = ["Systems Administrator","2013-11-12","2013-11-13","A systems administrator job",e2]
    job_3 = ["Backend Dev","2012-10-8","2012-10-16","A java developer job",e4]
    job_4 = ["Instructor","2012-10-22","2012-10-23","",e4]
    job_5 = ["Instructor","2012-10-22","2012-10-23","",e3]

    j1 = create_job_with_details(job_1)
    j2 = create_job_with_details(job_2)
    j3 = create_job_with_details(job_3)
    j4 = create_job_with_details(job_4)
    j5 = create_job_with_details(job_5)

    # shifts with limited, plenty and no slots
    shift_1 = ["2012-10-23","9:00","15:00",1,j1]
    shift_2 = ["2012-10-23","10:00","16:00",2,j1]
    shift_3 = ["2013-11-12","12:00","18:00",4,j2]
    shift_4 = ["2013-10-23","10:00","18:00",1,j4]

    s1 = create_shift_with_details(shift_1)
    s2 = create_shift_with_details(shift_2)
    s3 = create_shift_with_details(shift_3)
    s4 = create_shift_with_details(shift_4)

def tearDownModule():
    # Destroys all objects created
    clear_objects()

class EventTests(unittest.TestCase):
    '''
    Contains tests which require only event objects
    '''

    @classmethod
    def setup_test_data(cls):
        cls.e1 = e1
        cls.e2 = e2
        cls.e3 = e3
        cls.e4 = e4
        cls.e5 = e5

    @classmethod
    def setUpClass(cls):
        cls.setup_test_data()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_event_not_empty(self):
        """ Test event_not_empty(event_id) """

        self.assertTrue(event_not_empty(self.e1.id))
        self.assertFalse(event_not_empty(100))

    def test_get_event_by_id(self):
        """ Test get_event_by_id(event_id) """

        # test typical cases
        self.assertIsNotNone(get_event_by_id(self.e2.id))
        self.assertEqual(get_event_by_id(self.e2.id), self.e2)

        self.assertIsNone(get_event_by_id(100))

    def test_get_events_by_date(self):
        """ Test get_events_by_date(start_date, end_date) """

        # test typical cases
        event_list = get_events_by_date('2015-07-01','2015-08-01')
        self.assertIsNotNone(event_list)
        
        self.assertIn(self.e3, event_list)
        self.assertIn(self.e4, event_list)
        self.assertIn(self.e5, event_list)
        self.assertEqual(len(event_list), 3)
        
        # test order
        self.assertEqual(event_list[0], self.e3)
        self.assertEqual(event_list[1], self.e5)
        self.assertEqual(event_list[2], self.e4)

    def test_get_events_ordered_by_name(self):
        """ Test get_events_ordered_by_name() """

        # test typical cases
        event_list = get_events_ordered_by_name()
        self.assertIsNotNone(event_list)
        self.assertIn(self.e1, event_list)
        self.assertIn(self.e2, event_list)
        self.assertIn(self.e3, event_list)
        self.assertIn(self.e4, event_list)
        self.assertIn(self.e5, event_list)
        self.assertEqual(len(event_list), 5)

        # test order
        self.assertEqual(event_list[0], self.e5)
        self.assertEqual(event_list[1], self.e3)
        self.assertEqual(event_list[2], self.e1)
        self.assertEqual(event_list[3], self.e2)
        self.assertEqual(event_list[4], self.e4)

class EventWithJobTests(unittest.TestCase):
    '''
    Contains tests which require jobs and shifts
    '''

    @classmethod
    def setup_test_data(cls):
        cls.e4 = e4
        cls.e5 = e5
        cls.s1 = s1
        cls.s2 = s2

    @classmethod
    def setUpClass(cls):
        cls.setup_test_data()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_event_by_shift_id(self):
        """ Uses shifts s1 """
        self.assertIsNotNone(get_event_by_shift_id(self.s1.id))
        self.assertEqual(get_event_by_shift_id(self.s1.id), e1)
        self.assertIsNone(get_event_by_shift_id(200))

    def test_check_edit_event(self):
        """ Uses events e4 and e5 """

        # test typical cases
        start_date1 = datetime.date(2012, 10, 8)
        start_date2 = datetime.date(2012, 10, 7)
        start_date3 = datetime.date(2012, 10, 15)
        start_date4 = datetime.date(2013, 10, 8)
        stop_date1 = datetime.date(2012, 10, 23)
        stop_date2 = datetime.date(2012, 10, 22)
        stop_date3 = datetime.date(2012, 10, 26)
        stop_date4 = datetime.date(2013, 10, 23)

        # edit with valid date
        out1 = check_edit_event(self.e4.id, start_date1, stop_date1)

        # edit with one job outside date range
        out2 = check_edit_event(self.e4.id, start_date2, stop_date2)
        out3 = check_edit_event(self.e4.id, start_date3, stop_date3)
        # edit with both jobs outside
        out4 = check_edit_event(self.e4.id, start_date4, stop_date4)

        # check for event with no jobs
        out5 = check_edit_event(self.e5.id, start_date1, stop_date1)
        # check for non existing event
        out6 = check_edit_event(100, start_date1, stop_date1)

        self.assertTrue(out1['result'])
        self.assertFalse(out2['result'])
        self.assertFalse(out3['result'])
        self.assertFalse(out4['result'])
        self.assertTrue(out5['result'])
        self.assertFalse(out6['result'])

        self.assertEqual(out1['invalid_count'], 0)
        self.assertEqual(out2['invalid_count'], 1)
        self.assertEqual(out4['invalid_count'], 2)

        self.assertIn(j4.name,out2['invalid_jobs'])
        self.assertIn(j4.name,out4['invalid_jobs'])
        self.assertIn(j3.name,out4['invalid_jobs'])

class DeleteEventTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        event_1 = ["Open Source Event","2012-10-22","2012-10-23"]
        cls.e1 = create_event_with_details(event_1)

        # event with associated job/shift
        cls.e2 = e2

    @classmethod
    def tearDownClass(cls):
        pass

    def test_delete_event(self):
        #Test delete_event(event_id)

        self.assertTrue(delete_event(self.e1.id))
        self.assertFalse(delete_event(self.e2.id))
        self.assertFalse(delete_event(100))

class EventWithVolunteerTest(unittest.TestCase):
    '''
    Contains tests which require only volunteer objects
    '''

    @classmethod
    def setup_test_data(cls):

        cls.e1 = e1
        cls.e2 = e2
        cls.e3 = e3
        cls.e4 = e4
        cls.e5 = e5

        cls.s1 = s1
        cls.s2 = s2
        cls.s3 = s3
        cls.s4 = s4

        volunteer_1 = ['Yoshi',"Yoshi","Turtle","Mario Land","Nintendo Land","Nintendo State","Nintendo Nation","2374983247","yoshi@nintendo.com"]
        volunteer_2 = ['John',"John","Doe","7 Alpine Street","Maplegrove","Wyoming","USA","23454545","john@test.com"]
        volunteer_3 = ['Ash',"Ash","Ketchum","Pallet Town","Kanto","Gameboy","Japan","23454545","ash@pikachu.com"]

        cls.v1 = create_volunteer_with_details(volunteer_1)
        cls.v2 = create_volunteer_with_details(volunteer_2)
        cls.v3 = create_volunteer_with_details(volunteer_3)

    @classmethod
    def setUpClass(cls):
        cls.setup_test_data()

    def test_remove_empty_events_for_volunteer(self):
        
        """
        Uses Events e1,e2,e3,e4,e5, shift s2 and volunteer v1 where
        with job that has shift with open slots - e2
        Event with job and shift that volunteer already signed up for - e1
        Event with job and shift that have no slots remaining - e4
        Event with job that has no shifts - e3
        Event with no jobs - e5
        """
        
        register(self.v1.id, self.s2.id)
        register(self.v2.id, self.s4.id)
        
        event_list = [self.e1, self.e2, self.e3, self.e4, self.e5]
        event_list = remove_empty_events_for_volunteer(event_list, self.v1.id)

        #Only events with jobs that have open slots should remain
        self.assertIn(self.e1, event_list)
        self.assertIn(self.e2, event_list)
        self.assertNotIn(self.e3, event_list)
        self.assertNotIn(self.e4, event_list)
        self.assertNotIn(self.e5, event_list)
        VolunteerShift.objects.all().delete()

    def test_get_signed_up_events_for_volunteer(self):
        """ Uses events e1,e2, volunteers v1,v2,v3 and shift s1,s2,s3"""

        # volunteer 1 registers for 3 shifts belonging to two events - registers for s3 first to check if sorting is successful
        register(self.v1.id, self.s3.id)
        register(self.v1.id, self.s2.id)
        register(self.v1.id, self.s1.id)

        # volunteer 2 registers for 2 shifts, where s1 has no available slots
        register(self.v2.id, self.s1.id)
        register(self.v2.id, self.s3.id)

        event_list_for_vol_1 = get_signed_up_events_for_volunteer(self.v1.id)
        event_list_for_vol_2 = get_signed_up_events_for_volunteer(self.v2.id)
        event_list_for_vol_3 = get_signed_up_events_for_volunteer(self.v3.id)

        # tests for returned events, their order and duplication for volunteer 1
        self.assertEqual(len(event_list_for_vol_1), 2)
        self.assertIn(self.e1.name, event_list_for_vol_1)
        self.assertIn(self.e2.name, event_list_for_vol_1)
        self.assertEqual(event_list_for_vol_1[0], self.e1.name)
        self.assertEqual(event_list_for_vol_1[1], self.e2.name)

        # tests for returned events for volunteer 2
        self.assertEqual(len(event_list_for_vol_2), 1)
        self.assertIn(self.e2.name, event_list_for_vol_2)
        self.assertNotIn(self.e1.name, event_list_for_vol_2)

        # test for returned events for unregistered volunteer 3
        self.assertEqual(len(event_list_for_vol_3), 0)
        VolunteerShift.objects.all().delete()
        