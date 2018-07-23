# Django
# from django.db import Model
from django import forms
from django.forms import ModelForm

# local Django
from shift.models import Shift, EditRequest


class HoursForm(forms.Form):
    start_time = forms.TimeField()
    end_time = forms.TimeField()


class ShiftForm(ModelForm):
    class Meta:
        model = Shift
        fields = [
            'date', 'start_time', 'end_time', 'max_volunteers', 'country',
            'state', 'city', 'address', 'venue'
        ]


class EditForm(ModelForm):
    class Meta:
        model = EditRequest
        fields = [
           'start_time', 'end_time'
              ]
# we don't check that start_time > end_time because we could
# start at 11pm and end at 1am and this test would fail

