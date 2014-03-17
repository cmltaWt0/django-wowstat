from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'wowstat.views.dispatcher', name='default'),
)

