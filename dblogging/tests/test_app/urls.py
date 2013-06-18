from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dblogging.tests.test_app.views',
    url(r'^test/$', 'test', name='dblogging_test'),
    url(r'^test_redirect/$', 'test_redirect', name='dblogging_test_redirect'),
)
