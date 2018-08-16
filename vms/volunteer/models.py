# Django
from django.contrib.auth.models import User
from django.core.validators import (RegexValidator, MaxValueValidator,
                                    MinValueValidator)
from django.db import models
from cities_light.models import City, Country, Region

# local Django
from organization.models import Organization


class Volunteer(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', ),
        ],
    )
    last_name = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', ),
        ],
    )
    address = models.CharField(
        max_length=75,
        validators=[
            RegexValidator(r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\-)|(\.)|(,)|(\:)]+$', ),
        ],
    )
    city = models.ForeignKey(City, null=True, blank=True)
    state = models.ForeignKey(Region, null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)
    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                r'^\s*(?:\+?(\d{1,3}))?([-. (]*(\d{3})[-. )]*)?'
                r'((\d{3})[-. ]*(\d{2,4})(?:[-.x ]*(\d+))?)\s*$',
                message="Please enter a valid phone number",
            ),
        ],
    )
    # Organization to Volunteer is a one-to-many relationship
    organization = models.ForeignKey(Organization, null=True)
    # EmailField automatically checks if email address is a valid format
    email = models.EmailField(max_length=45, unique=True)
    websites = models.TextField(
        blank=True,
        validators=[
            RegexValidator(
                r'^(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+'
                r'[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+'
                r'[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))'
                r'[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})+$',
            ),
        ],
    )
    description = models.TextField(
        blank=True,
        validators=[
            RegexValidator(r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\.)|(,)|(\-)|(!)]+$', ),
        ],
    )
    resume = models.TextField(
        blank=True,
        validators=[
            RegexValidator(r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\.)|(,)|(\-)|(!)]+$', ),
        ],
    )
    # all resumes are stored in /srv/vms/resume/
    resume_file = models.FileField(
        upload_to='vms/resume/', max_length=75, blank=True)
    reminder_days = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(50),
                    MinValueValidator(1)],
        blank=True)

    user = models.OneToOneField(User)

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

