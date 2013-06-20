from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from dblogging.tests.helpers.factories import SuperuserF, RequestLogF
from pyquery import PyQuery


class AdminChangeListTestCase(TestCase):
    urls = 'dblogging.tests.test_app.urls'

    def setUp(self):
        super(AdminChangeListTestCase, self).setUp()
        root = SuperuserF()
        self.client.login(username=root.username, password=SuperuserF.attributes()['password'])

    def test_renders_requests_list(self):
        RequestLogF()
        response = self.client.get(reverse('admin:dblogging_requestlog_changelist'))
        self.assertEqual(200, response.status_code)
        pq = PyQuery(response.content)
        self.assertEqual(1, len(pq('table#result_list tbody tr')))

    def test_has_no_permission_to_add(self):
        response = self.client.get(reverse('admin:dblogging_requestlog_add'))
        self.assertEqual(403, response.status_code)
