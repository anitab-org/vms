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
        checks = dict()
        # check if it contains a lowercase digit
        checks['lower'] = any(char.islower() for char in password)
        # check if it contains a digit
        checks['digit'] = any(char.isdigit() for char in password)
        # check if its length<=6
        checks['size'] = 6 <= len(password)
        # check if it has special characters
        y = '[~!@#$%^&*()_+{}":;\']+$'
        checks['special'] = set(y).intersection(password)
        if all(checks.values()):
            return password
        else:
            raise ValidationError(
                "Password must have at least 6 characters, one "
                "lowercase letter, one "
                "special character and one digit.")

    class Meta:
        model = User
        fields = ('username', 'password')

