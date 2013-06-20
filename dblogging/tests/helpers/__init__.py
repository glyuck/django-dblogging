from django.test import TestCase as DjangoTestCase
from django.utils import simplejson

from dblogging.models import RequestLog


class TestCase(DjangoTestCase):
    urls = 'dblogging.tests.test_app.urls'
    host = 'testserver'

    def assertLog(self, **params):
        log = RequestLog.objects.latest()
        for attr, expected in params.items():
            if isinstance(expected, dict):
                value = simplejson.loads(getattr(log, attr))
            else:
                value = getattr(log, attr)
            self.assertEqual(expected, value,
                             'Logging error for param %s (expected=%s, actual=%s)' % (attr, expected, value))
