# Django
from django.conf.urls import patterns, url

# local Django
from administrator.views import *
from registration import views
from registration.views import *

urlpatterns = patterns('',
    url(r'^signup_administrator/$', AdministratorSignupView.as_view(), name='signup_administrator'),
    url(r'^signup_volunteer/$', VolunteerSignupView.as_view(), name='signup_volunteer'),
)
