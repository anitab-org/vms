#Django
from django.conf.urls import patterns, url

# local Django
from administrator import views
from administrator.views import *

urlpatterns = patterns('',
                       url(r'^report/$', GenerateReportView.as_view(), name='report'),
                       url(r'^settings/$', views.settings, name='settings'),
                       )
