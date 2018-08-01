# Django
from django.conf.urls import url

# local Django
# from administrator.views import AdministratorSignUpView
# from registration import views
from registration.views import AdministratorSignupView, VolunteerSignupView, activate

urlpatterns = [
    url(r'^signup_administrator/$',
        AdministratorSignupView.as_view(),
        name='signup_administrator'),
    url(r'^signup_volunteer/$',
        VolunteerSignupView.as_view(),
        name='signup_volunteer'),
    url(r'^signup_volunteer/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate,
        name='activate'),
]

