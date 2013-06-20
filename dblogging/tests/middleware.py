from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, AnonymousUser

from dblogging.models import RequestLog
from dblogging.tests.helpers import TestCase


class RequestLogMiddlewareTestCase(TestCase):
    @property
    def url(self):
        return reverse('dblogging_test')

    def test_redirect(self):
        self.client.get(reverse('dblogging_test_redirect'))
        self.assertLog(response_status_code=302, response_body='')

    def test_method_host_url(self):
        query = 'a=b'
        url = self.url + '?' + query
        self.client.get(url)
        self.assertEqual(1, RequestLog.objects.count())
        self.assertLog(method='GET',
                       host=self.host,
                       path=self.url,
                       query='a=b',
                       post={})

        post_params = {'post_param': 'post_value'}
        self.client.post(url, post_params)
        self.assertEqual(2, RequestLog.objects.count())
        self.assertLog(method='POST',
                       host=self.host,
                       path=self.url,
                       query='a=b',
                       post=post_params)

    def test_user(self):
        user = User.objects.create_user('user1', 'user1@example.com', '123123')
        self.client.login(username=user.username, password='123123')
        self.client.get(self.url)
        self.assertLog(method='GET', user=user, user_repr=str(user))

    def test_anonymous_user(self):
        self.client.get(self.url)
        self.assertLog(method='GET', user=None, user_repr=str(AnonymousUser()))

    def test_cookies(self):
        self.client.cookies['test'] = 'test-value'
        self.client.get(self.url)
        self.assertLog(cookies={'test': 'test-value'})

    def test_request_headers(self):
        expected_headers = {'Cookie': '',  # Sent with each test client request
                            'X-Requested-With': 'XMLHttpRequest',
                            'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7'}
        self.client.get(self.url,
                        HTTP_X_REQUESTED_WITH=expected_headers['X-Requested-With'],
                        HTTP_USER_AGENT=expected_headers['User-Agent'])
        self.assertLog(request_headers=expected_headers)

    def test_response_headers(self):
        self.client.get(self.url)
        self.assertLog(response_headers={'Content-Type': 'text/html'})

    def test_response_status_code_response_body(self):
        self.client.get(self.url)
        self.assertLog(response_status_code=200, response_body='Sample response')
