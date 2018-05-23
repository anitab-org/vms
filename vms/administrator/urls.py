# Django
from django.conf.urls import  url

# local Django
from administrator import views
from administrator.views import GenerateReportView, AdminUpdateView, ProfileView

urlpatterns = [
    url(r'^report/$', GenerateReportView.as_view(), name='report'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^edit/(?P<admin_id>\d+)$', AdminUpdateView.as_view(), name='edit'),
    url(r'^profile/(?P<admin_id>\d+)$', ProfileView.as_view(), name='profile'),
]

