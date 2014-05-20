from django.conf.urls import patterns, url
from wowstat.views import Dispatcher

urlpatterns = patterns('',
    url(r'^$', Dispatcher.as_view(), name='default'),
)

