import datetime
import re

from django.core.urlresolvers import reverse

from dblogging.models import RequestLog
from dblogging.tests.helpers import TestCase
from dblogging.tests.helpers.factories import RequestLogF


class ConfTestCase(TestCase):
    urls = 'dblogging.tests.test_app.urls'

    @property
    def url(self):
        return reverse('dblogging_test')

    def test_DBLOGGING_ENABLED_False(self):
        with self.settings(DBLOGGING_ENABLED=False):
            self.client.get(self.url)
            self.assertEquals(0, RequestLog.objects.count())

    def test_DBLOGGING_SAVE_RESPONSE_BODY_False(self):
        with self.settings(DBLOGGING_SAVE_RESPONSE_BODY=False):
            response = self.client.get(self.url)
            self.assertLog(response_status_code=response.status_code, response_body=None)

    def test_DBLOGGING_SAVE_RESPONSE_BODY_numeric(self):
        with self.settings(DBLOGGING_SAVE_RESPONSE_BODY=4):
            response = self.client.get(self.url)
            self.assertLog(response_status_code=response.status_code, response_body='Samp')

    def test_DBLOGGING_SAVE_RESPONSE_BODY_numeric_without_body(self):
        with self.settings(DBLOGGING_SAVE_RESPONSE_BODY=4):
            response = self.client.get(reverse('dblogging_test_redirect'))
            self.assertLog(response_status_code=response.status_code, response_body='')

    def test_DBLOGGING_IGNORE_URLS(self):
        ignore_patterns = [re.compile('^/test.*')]
        with self.settings(DBLOGGING_IGNORE_URLS=ignore_patterns):
            self.client.get(self.url)
            self.assertEquals(0, RequestLog.objects.count())

    def test_DBLOGGING_LOG_EXPIRY_SECONDS(self):
        with self.settings(DBLOGGING_LOG_EXPIRY_SECONDS=180):
            log1 = RequestLogF(when=datetime.datetime.now() - datetime.timedelta(seconds=190))
            log2 = RequestLogF(when=datetime.datetime.now() - datetime.timedelta(seconds=170))
            self.client.get(self.url)
            with self.assertRaises(RequestLog.DoesNotExist):
                RequestLog.objects.get(pk=log1.pk)
            RequestLog.objects.get(pk=log2.pk)
            self.assertEquals(2, RequestLog.objects.count())
