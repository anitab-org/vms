# Django
from django.conf.urls import url

# local Django
from event import views
from event.views import EventCreateView, EventDeleteView, EventUpdateView

urlpatterns = [
    url(r'^create/$', EventCreateView.as_view(), name='create'),
    url(r'^delete/(?P<event_id>\d+)$',
        EventDeleteView.as_view(),
        name='delete'),
    url(r'^edit/(?P<event_id>\d+)$', EventUpdateView.as_view(), name='edit'),
    url(r'^list/$', views.list_events, name='list'),
    url(r'^list_sign_up/(?P<volunteer_id>\d+)$',
        views.list_sign_up,
        name='list_sign_up'),
]

