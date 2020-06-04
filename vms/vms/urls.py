# Django
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = i18n_patterns(
    url(r'^$', RedirectView.as_view(url='home/')),
    url(r'^admin/', admin.site.urls),
    url(r'^administrator/',
        include('administrator.urls', namespace='administrator')),
    url(r'^authentication/',
        include('authentication.urls', namespace='authentication')),
    url(r'^home/', include('home.urls', namespace='home')),
    url(r'^event/', include('event.urls', namespace='event')),
    url(r'^job/', include('job.urls', namespace='job')),
    url(r'^organization/',
        include('organization.urls', namespace='organization')),
    url(r'^registration/',
        include('registration.urls', namespace='registration')),
    url(r'^shift/', include('shift.urls', namespace='shift')),
    url(r'^volunteer/', include('volunteer.urls', namespace='volunteer')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
