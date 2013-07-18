from dblogging.tests import RequestLogF
from dblogging.tests.helpers import TestCase


class RequestLogTestCase(TestCase):
    def test_full_uri(self):
        instance = RequestLogF(host='localhost', path='/path')
        self.assertEqual('localhost/path', instance.full_uri())

    def test_full_uri_with_query(self):
        instance = RequestLogF(host='localhost', path='/path', query='param=value')
        self.assertEqual('localhost/path?param=value', instance.full_uri())
