from django.conf.urls import patterns, url
from job import views
from job.views import *

urlpatterns = patterns('',
    url(r'^create/$', CreateJobView.as_view(), name='create'),
    url(r'^delete/(?P<job_id>\d+)$', JobDeleteView.as_view(), name='delete'),
    url(r'^details/(?P<job_id>\d+)$', JobDetailView.as_view(), name='details'),
    url(r'^edit/(?P<job_id>\d+)$', JobUpdateView.as_view(), name='edit'),
    url(r'^list/$', JobListView.as_view(), name='list'),
    url(r'^list_sign_up/(?P<event_id>\d+)/(?P<volunteer_id>\d+)$', views.list_sign_up, name='list_sign_up'),
)
