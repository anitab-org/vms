# Django
from django.core.validators import RegexValidator
from django.db import models

# local Django
from event.models import Event


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event)
    name = models.CharField(
        max_length=75,
        validators=[
            RegexValidator(r'^[(A-Z)|(a-z)|(\s)|(\')]+$', ),
        ],
    )
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(
        blank=True,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\.)|(,)|(\-)|(!)|(\')]+$', ),
        ],
    )

    def __str__(self):
        return str(self.name)
