from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('process.views',
    url(r'^$', 'process', name='process'),
    )
