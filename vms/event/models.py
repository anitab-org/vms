# Django
from django.core.validators import RegexValidator
from cities_light.models import City, Country, Region
from django.db import models


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=75,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\.)|(,)|(\-)|(!)|(\')]+$',
            ),
        ],
    )
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

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

    def __str__(self):
        return str(self.name)
