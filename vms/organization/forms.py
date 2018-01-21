# Django
from django.forms import ModelForm

# local Django
from organization.models import Organization


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = ['name']
