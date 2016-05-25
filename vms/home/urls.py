from django.conf.urls import patterns, url
from home import views
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home/home.html'), name='index'),
)
