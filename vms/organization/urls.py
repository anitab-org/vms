# Django
from django.conf.urls import url

# local Django
from organization.views import OrganizationCreateView, OrganizationDeleteView, OrganizationListView, OrganizationUpdateView

urlpatterns = [
    url(r'^create/$', OrganizationCreateView.as_view(), name='create'),
    url(r'^delete/(?P<organization_id>\d+)$',
        OrganizationDeleteView.as_view(),
        name='delete'),
    url(r'^edit/(?P<organization_id>\d+)$',
        OrganizationUpdateView.as_view(),
        name='edit'),
    url(r'^list/$', OrganizationListView.as_view(), name='list'),
]

