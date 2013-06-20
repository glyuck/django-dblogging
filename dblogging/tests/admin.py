from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from pyquery import PyQuery

from dblogging.admin import admin, RequestLogAdmin
from dblogging.models import RequestLog
from dblogging.tests.helpers.factories import SuperuserF, RequestLogF


class RequestLogAdminTestCase(TestCase):
    def setUp(self):
        super(RequestLogAdminTestCase, self).setUp()
        self.admin = RequestLogAdmin(RequestLog, admin.site)

    def test_dict_to_html_returns_empty_string(self):
        self.assertEqual('', self.admin.dict_to_html({}))

    def test_dict_to_html_returns_table(self):
        self.assertEqual('<table class="dictionary">'
                         '<tr><th>another</th><td>value</td></tr>'
                         '<tr><th>some</th><td>key</td></tr>'
                         '</table>',
                         self.admin.dict_to_html({'some': 'key', 'another': 'value'}))

    def test_dict_to_html_multiple_values(self):
        self.assertEqual('<table class="dictionary">'
                         '<tr><th>another</th><td><ul><li>value1</li><li>value2</li></ul></td></tr>'
                         '<tr><th>some</th><td>key</td></tr>'
                         '<tr><th>third</th><td></td></tr>'
                         '</table>',
                         self.admin.dict_to_html({'some': ['key'], 'another': ['value2', 'value1'], 'third': []}))


class RequestLogAdminSmokeTestCase(TestCase):
    urls = 'dblogging.tests.test_app.urls'

    def setUp(self):
        super(RequestLogAdminSmokeTestCase, self).setUp()
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

    def test_renders_change_form(self):
        requestlog = RequestLogF()
        response = self.client.get(reverse('admin:dblogging_requestlog_change', args=[requestlog.id]))
        self.assertEqual(200, response.status_code)
