from django.core.validators import RegexValidator
from django.db import models

class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        unique=True,
        max_length=75,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\-)|(:)|(\')]+$',
            ),
        ],
    )
