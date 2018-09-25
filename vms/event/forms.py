# Django
from django import forms
from django.forms import ModelForm

# local Django
from event.models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'name', 'description', 'start_date', 'end_date',
            'address', 'venue'
        ]

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                msg = u"Start date must be before the end date"
                self._errors['start_date'] = self.error_class([msg])

        return self.cleaned_data


class SearchEventForm(forms.Form):
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
    job = forms.CharField(required=False)

