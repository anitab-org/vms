from django.test import TestCase
from django.contrib.auth.models import User
import datetime
from datetime import date

from event.models import Event
from job.models import Job
from shift.services import register
from shift.models import Shift
from volunteer.models import Volunteer
from job.services import (
                            delete_job,
                            check_edit_job,
                            get_job_by_id,
                            get_jobs_by_event_id,
                            get_jobs_ordered_by_title,
                            remove_empty_jobs_for_volunteer
                            )


class JobMethodTests(TestCase):

    def test_delete_job(self):
        """ Test delete_job(job_id) """

        e1 = Event(
                name="Software Conference",
                start_date="2012-10-22",
                end_date="2012-10-25"
                )

        e1.save()

        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )

        j2 = Job(
                name="Systems Administrator",
                start_date="2012-9-1",
                end_date="2012-10-26",
                description="A systems administrator job",
                event=e1
                )

        j3 = Job(
                name="Project Manager",
                start_date="2012-1-2",
                end_date="2012-2-2",
                description="A management job",
                event=e1
                )

        j1.save()
        j2.save()
        j3.save()

        # test typical cases
        self.assertTrue(delete_job(j1.id))
        self.assertTrue(delete_job(j2.id))
        self.assertTrue(delete_job(j3.id))
        self.assertFalse(delete_job(100))
        self.assertFalse(delete_job(200))
        self.assertFalse(delete_job(300))

    def test_check_edit_job(self):

        e1 = Event(
                name="Open Source Event",
                start_date="2012-10-3",
                end_date="2012-10-24"
                )

        e1.save()

        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )

        j2 = Job(
                name="Systems Administrator",
                start_date="2012-10-8",
                end_date="2012-10-16",
                description="A systems administrator job",
                event=e1
                )

        j1.save()
        j2.save()

        s1 = Shift(
                date="2012-10-23",
                start_time="1:00",
                end_time="3:00",
                max_volunteers=5,
                job=j1
                )

        s2 = Shift(
                date="2012-10-25",
                start_time="2:00",
                end_time="4:00",
                max_volunteers=5,
                job=j1
                )

        s1.save()
        s2.save()

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

        e1 = Event(
                name="Software Conference",
                start_date="2012-10-22",
                end_date="2012-10-25"
                )

        e1.save()

        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )

        j2 = Job(
                name="Systems Administrator",
                start_date="2012-9-1",
                end_date="2012-10-26",
                description="A systems administrator job",
                event=e1
                )

        j3 = Job(
                name="Project Manager",
                start_date="2012-1-2",
                end_date="2012-2-2",
                description="A management job",
                event=e1
                )

        j1.save()
        j2.save()
        j3.save()

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

        e1 = Event(
                name="Software Conference",
                start_date="2012-10-22",
                end_date="2012-10-25"
                )

        e1.save()

        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )

        j2 = Job(
                name="Systems Administrator",
                start_date="2012-9-1",
                end_date="2012-10-26",
                description="A systems administrator job",
                event=e1
                )

        j3 = Job(
                name="Project Manager",
                start_date="2012-1-2",
                end_date="2012-2-2",
                description="A management job",
                event=e1
                )

        j1.save()
        j2.save()
        j3.save()

        # test typical case
        job_list = get_jobs_by_event_id(e1.id)
        self.assertIsNotNone(job_list)
        self.assertNotEqual(job_list, False)
        self.assertEqual(len(job_list), 3)
        self.assertIn(j1, job_list)
        self.assertIn(j2, job_list)
        self.assertIn(j3, job_list)

    def test_get_jobs_ordered_by_title(self):

        e1 = Event(
                name="Software Conference",
                start_date="2012-10-22",
                end_date="2012-10-25"
                )

        e1.save()

        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )

        j2 = Job(
                name="Systems Administrator",
                start_date="2012-9-1",
                end_date="2012-10-26",
                description="A systems administrator job",
                event=e1
                )

        j3 = Job(
                name="Project Manager",
                start_date="2012-1-2",
                end_date="2012-2-2",
                description="A management job",
                event=e1
                )

        j1.save()
        j2.save()
        j3.save()

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

    def test_remove_empty_jobs_for_volunteer(self):

        e1 = Event(
                name="Software Conference",
                start_date="2012-10-22",
                end_date="2012-10-25"
                )

        e1.save()
        
        #Job with shift that has slots available
        j1 = Job(
                name="Software Developer",
                start_date="2012-10-22",
                end_date="2012-10-23",
                description="A software job",
                event=e1
                )
        
        #Job with shift volunteer will have already signed up for  
        j2 = Job(
                name="Systems Administrator",
                start_date="2012-9-1",
                end_date="2012-10-26",
                description="A systems administrator job",
                event=e1
                )

        #Job with shift that has no available slots
        j3 = Job(
                name="Project Manager",
                start_date="2012-1-2",
                end_date="2012-2-2",
                description="A management job",
                event=e1
                )

        #Job with no shifts
        j4 = Job(
                name="Information Technologist",
                start_date="2012-11-2",
                end_date="2012-12-2",
                description="An IT job",
                event=e1
                )

        j1.save()
        j2.save()
        j3.save()
        j4.save()
        
        s1 = Shift(
                date="2012-10-23",
                start_time="9:00",
                end_time="3:00",
                max_volunteers=5,
                job=j1
                )

        s2 = Shift(
                date="2012-10-23",
                start_time="10:00",
                end_time="4:00",
                max_volunteers=5,
                job=j2
                )

        s3 = Shift(
                date="2012-10-23",
                start_time="12:00",
                end_time="6:00",
                max_volunteers=0,
                job=j3
                )

        s1.save()
        s2.save()
        s3.save()
        
        u1 = User.objects.create_user('Yoshi')
        
        v1 = Volunteer(
                    first_name="Yoshi",
                    last_name="Turtle",
                    address="Mario Land",
                    city="Nintendo Land",
                    state="Nintendo State",
                    country="Nintendo Nation",
                    phone_number="2374983247",
                    email="yoshi@nintendo.com",
                    user=u1
                    )

        v1.save()
        
        register(v1.id, s2.id)
        
        job_list = [j1, j2, j3, j4]
        job_list = remove_empty_jobs_for_volunteer(job_list, v1.id)

        #Only open and non empty jobs should be left
        self.assertIn(j1, job_list)
        self.assertNotIn(j2, job_list)
        self.assertNotIn(j3, job_list)
        self.assertNotIn(j4, job_list)
            
            
