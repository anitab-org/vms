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

    # Shifts are bound to end on the same date so
    # end_time has to be greater than start_time
    def clean(self):
        cleaned_data = super(ShiftForm, self).clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time > end_time:
                msg = u"Start time must be before the end time"
                self._errors['start_time'] = self.error_class([msg])

        return self.cleaned_data


class EditForm(ModelForm):
    class Meta:
        model = EditRequest
        fields = [
            'start_time', 'end_time'
        ]

