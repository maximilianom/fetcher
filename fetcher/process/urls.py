from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('fetcher.process.views',
    url(r'^$', 'process', name='process'),
    url(r'^add_machine/$', 'add_machine', name="add"),
    url(r'^stop/$', 'stop', name="stop"),
    )
