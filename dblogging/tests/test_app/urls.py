from django.conf.urls import include, patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('dblogging.tests.test_app.views',
    url(r'^test/$', 'test', name='dblogging_test'),
    url(r'^test_redirect/$', 'test_redirect', name='dblogging_test_redirect'),
    (r'^admin/', include(admin.site.urls)),
)
