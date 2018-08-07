# Django
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError

from administrator.models import Administrator
from volunteer.models import Volunteer


class AuthenticationForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        """
        informs user that his email is invalid during Password Reset

        :return: email of user
        :raises: ValidationError
        """
        email = self.cleaned_data['email']
        if not (
            Administrator.objects.filter(email__iexact=email).exists() or
            Volunteer.objects.filter(email__iexact=email).exists()
        ):
            raise ValidationError(
                "There is no user registered with "
                "the specified email address!"
            )
        return email
