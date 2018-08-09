import re

# Django
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserForm(forms.ModelForm):
    # password not visible when user types it out
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean_password(self):
        password = self.cleaned_data['password']
        x = r'^(?=.*?[A-Z])'
        y = '[~!@#$%^&*()_+{}":;\']+$'
        z = r'^(?=.*?[0-9])'
        digit = re.match(z, password)
        special_char = set(y).intersection(password)
        uppercase = re.match(x, password)
        if digit and uppercase and special_char:
            return password
        else:
            raise ValidationError(
                "Password must have at least one uppercase letter, "
                "one special character and one digit.")


    class Meta:
        model = User
        fields = ('username', 'password')

