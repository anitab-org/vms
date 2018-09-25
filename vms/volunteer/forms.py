# Django
from django import forms

# local Django
from volunteer.models import Volunteer
from shift.models import Report


class ReportForm(forms.Form):
    event_name = forms.RegexField(
        regex=r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\.)|(,)|(\-)|(!)]+$',
        max_length=75,
        required=False)
    job_name = forms.RegexField(
        regex=r'^[(A-Z)|(a-z)|(\s)]+$', max_length=75, required=False)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    class Meta:
        model = Report


class SearchVolunteerForm(forms.Form):
    first_name = forms.RegexField(
        regex=r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', max_length=30, required=False)
    last_name = forms.RegexField(
        regex=r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', max_length=30, required=False)
    city = forms.RegexField(
        regex=r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', max_length=75, required=False)
    state = forms.RegexField(
        regex=r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', max_length=75, required=False)
    country = forms.RegexField(
        regex=r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', max_length=75, required=False)
    organization = forms.RegexField(
        regex=r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', max_length=75, required=False)
    event = forms.CharField(required=False)
    job = forms.CharField(required=False)


class VolunteerForm(forms.ModelForm):
    unlisted_organization = forms.RegexField(
        regex=r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\-)|(:)]+$',
        max_length=100,
        required=False
    )

    class Meta:
        model = Volunteer
        fields = [
            'first_name', 'last_name', 'address',
            'phone_number', 'email', 'websites',
            'description', 'resume', 'resume_file',
            'reminder_days'
        ]

