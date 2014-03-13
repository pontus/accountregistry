from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',

                       url(r'^$', 'register.views.index'),
                       url(r'^request$', 'register.views.request', name="requestpage"),
                       url(r'^request/done$', 'register.views.request_sent'),
                       url(r'^logout$', 'register.views.logout_view'),
                       url(r'^login/.*$', 'register.views.login_view', name="login-parameter"),
                       url(r'^login$', 'register.views.login_view', name="login-none"),
                       url(r'^admin$', 'register.views.admin_view', name="admin"),
                       url(r'^admin/done$', 'register.views.admin_sent'),
)
