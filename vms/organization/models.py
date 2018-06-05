# Django
from django.core.validators import RegexValidator
from django.db import models


class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        unique=True,
        max_length=75,
        validators=[
            RegexValidator(r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\-)|(:)|(\')]+$', ),
        ],
    )

    def __str__(self):
        return self.name

    @staticmethod
    def create_multiple_organizations(n):
        org_name = 'org-{0}'
        org_list = list()
        for i in range(1, n+1):
            org_list.append(Organization.objects.create(name=org_name.format(str(i))))
        return org_list
