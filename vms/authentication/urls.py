# Django
from django.conf.urls import url
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView)

# local Django
from authentication import views
from authentication.views import anonymous_required
from authentication.forms import EmailValidationOnForgotPassword

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$',
        anonymous_required(
            LoginView.as_view(
                template_name='authentication/login.html'
            )
        ),
        name='login_process'),
    url(r'^logout/$',
        LogoutView.as_view(template_name='home/home.html'),
        name='logout_process'),
    url(r'^password_reset/$',
        PasswordResetView.as_view(
            success_url='done/',
            form_class=EmailValidationOnForgotPassword
        ),
        name='password_reset'),
    url(r'^password_reset/done/$',
        PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(
            success_url='/authentication/reset/complete/'
        ),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
        ),
    url(r'^change-password/$',
        PasswordChangeView.as_view(success_url='done/'),
        name='password_change'),
    url(r'^change-password/done/$',
        PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html'
        ),
        name='password_change_done'),
]

