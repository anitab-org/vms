from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

from organization.models import Organization


class Administrator(models.Model):
    first_name = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)|(\-)]+$',
            ),
        ],
    )
    last_name = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)|(\-)]+$',
            ),
        ],
    )
    address = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\-)]+$',
            ),
        ],
    )
    city = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)|(\-)]+$',
            ),
        ],
    )
    state = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)|(\-)]+$',
            ),
        ],
    )
    country = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)|(\-)]+$',
            ),
        ],
    )
    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            ),
        ],
    )
    unlisted_organization = models.CharField(
        blank=True,
        max_length=75,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\-)|(:)]+$',
            ),
        ],
    )
    # Organization to Volunteer is a one-to-many relationship
    organization = models.ForeignKey(Organization, null=True)
    # EmailField automatically checks if email address is a valid format
    email = models.EmailField(max_length=45, unique=True)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.username
