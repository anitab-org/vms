# Django
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from django.utils import timezone

# local Django
from job.models import Job
from volunteer.models import Volunteer
from cities_light.models import City, Country, Region


class Shift(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_volunteers = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(5000)])
    address = models.CharField(
        max_length=75,
        validators=[
            RegexValidator(r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\-)|(\')]+$', ),
        ],
        blank=True,
        null=True,
    )

    city = models.ForeignKey(City, null=True, blank=True)
    state = models.ForeignKey(Region, null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)
    venue = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(r'^[(A-Z)|(a-z)|(\s)|(\-)|(\')]+$', ),
        ],
        blank=True,
        null=True,
    )
    # Job to Shift is a one-to-many relationship
    job = models.ForeignKey(Job)
    # VolunteerShift is the intermediary model
    # for the many-to-many relationship between Volunteer and Shift
    volunteers = models.ManyToManyField(Volunteer, through='VolunteerShift')

    def __str__(self):
        return '{0} - {1}'.format(self.job.name, self.date)


class VolunteerShift(models.Model):
    # Volunteer  to VolunteerShift is a one-to-many relationship
    volunteer = models.ForeignKey(Volunteer)
    # Shift to VolunteerShift is a one-to-many relationship
    shift = models.ForeignKey(Shift)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    date_logged = models.DateTimeField(null=True, blank=True)
    edit_requested = models.BooleanField(default=False)
    # assigned_by_manager = models.BooleanField()
    STATUS_CHOICES = ((False, "Not reported"),
                      (True, "Reported"),)
    report_status = models.BooleanField(choices=STATUS_CHOICES, default=False)

    def __str__(self):
        return '{0} - {1}'.format(self.shift, self.volunteer.first_name)


class EditRequest(models.Model):
    volunteer_shift = models.ForeignKey(VolunteerShift)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return '{0} - {1}'.format(
            self.volunteer_shift.shift, self.volunteer_shift.volunteer
        )


class Report(models.Model):
    total_hrs = models.DecimalField(max_digits=20, decimal_places=2)
    volunteer_shifts = models.ManyToManyField(VolunteerShift)
    # confirm_status divides reports into three categories namely
    # pending:0, approved:1 and rejected:2
    confirm_status = models.IntegerField(default=0)
    date_submitted = models.DateField(default=timezone.now)
    volunteer = models.ForeignKey(Volunteer)

    def get_volunteer_shifts(self):
        return self.volunteer_shifts.all()

