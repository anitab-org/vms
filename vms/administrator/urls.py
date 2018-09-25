# Django
from django.conf.urls import url

# local Django
from administrator import views
from administrator.views import AdminUpdateView, ProfileView, ReportListView

urlpatterns = [
    url(r'^report/$', ReportListView.as_view(), name='report'),
    url(
        r'^report/view/(?P<report_id>\d+)$',
        views.show_report,
        name='show_report'
    ),
    url(
        r'^report/approve/(?P<report_id>\d+)$',
        views.approve,
        name='approve_report'
    ),
    url(
        r'^report/reject/(?P<report_id>\d+)$',
        views.reject,
        name='reject_report'
    ),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^edit/(?P<admin_id>\d+)$', AdminUpdateView.as_view(), name='edit'),
    url(r'^profile/(?P<admin_id>\d+)$', ProfileView.as_view(), name='profile'),
]

