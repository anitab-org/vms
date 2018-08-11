# Django
from django.forms import ModelForm
from django import forms

# local Django
from job.models import Job


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['name', 'start_date', 'end_date', 'description']

    def clean(self):

        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                msg = u"Start date must be before the end date"
                self._errors['start_date'] = self.error_class([msg])

        return self.cleaned_data


class SearchJobForm(forms.Form):
    name = forms.RegexField(
        regex=r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\.)|(,)|(\-)|(!)|(\')]+$',
        max_length=75,
        required=False
    )
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    city = forms.RegexField(
        regex=r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', max_length=75, required=False)
    state = forms.RegexField(
        regex=r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', max_length=50, required=False)
    country = forms.RegexField(
        regex=r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', max_length=75, required=False)
    event = forms.CharField(required=False)

