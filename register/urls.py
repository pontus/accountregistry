from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',

    url(r'^$', 'register.views.index'),
   url(r'^request$', 'register.views.request'),
   url(r'^request/done$', 'register.views.request_sent'),
   url(r'^logout$', 'register.views.logout_view'),

)
