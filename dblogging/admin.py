try:
    from urllib import parse as urlparse  # python3 compatibility
except ImportError:
    import urlparse
from django.contrib import admin
from django.utils import simplejson

from dblogging.models import RequestLog


class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('log_when', 'total_time', 'ip', 'session_key', 'user', 'user_repr', 'status_code', 'method', 'path', 'query_short')
    search_fields = ('ip', 'session_key', 'user_repr', 'path', 'query', 'cookies')
    ordering = ('-id',)
    readonly_fields = RequestLog._meta.get_all_field_names() + ['full_uri_with_method', 'request_headers_html', 'response_headers_html', 'query_params_html', 'post_params_html']
    fieldsets = (
        (None, {
            'fields': ('when', 'ip', 'session_key', 'user', 'user_repr')
        }),
        ('Request', {
            'fields': ('full_uri_with_method', 'request_headers_html', 'query_params_html', 'post_params_html')
        }),
        ('Response', {
            'fields': ('response_status_code', 'response_headers_html', 'response_body', 'total_time')
        }),
    )

    class Media:
        css = {
            "all": ("dblogging/admin.css",)
        }

    def has_add_permission(self, request):
        return False

    def dict_to_html(self, dictionary):
        if not dictionary:
            return ''

        def value_to_string(value):
            if isinstance(value, (list, tuple)):
                if len(value) == 0:
                    return ''
                elif len(value) == 1:
                    return value[0]
                else:
                    return '<ul><li>%s</li></ul>' % '</li><li>'.join(sorted(value))
            return value
        return '<table class="dictionary">%s</table>' % ''.join('<tr><th>%s</th><td>%s</td></tr>' % (name, value_to_string(dictionary[name]))
                                                          for name in sorted(dictionary.keys()))

    def log_when(self, requestlog):
        return '<nobr>' + requestlog.when.strftime('%Y-%m-%d %H:%M:%S.%f') + '</nobr>'
    log_when.allow_tags = True

    def status_code(self, requestlog):
        return requestlog.response_status_code
    status_code.short_description = 'Code'

    def query_short(self, requestlog):
        return requestlog.query[:80]

    def query_params_html(self, requestlog):
        return self.dict_to_html(urlparse.parse_qs(requestlog.query))
    query_params_html.allow_tags = True
    query_params_html.short_description = 'Query params'

    def post_params_html(self, requestlog):
        return self.dict_to_html(simplejson.loads(requestlog.post))
    post_params_html.allow_tags = True
    post_params_html.short_description = 'POST params'

    def request_headers_html(self, requestlog):
        return self.dict_to_html(simplejson.loads(requestlog.request_headers))
    request_headers_html.allow_tags = True
    request_headers_html.short_description = 'Request headers'

    def response_headers_html(self, requestlog):
        return self.dict_to_html(simplejson.loads(requestlog.response_headers))
    response_headers_html.allow_tags = True
    response_headers_html.short_description = 'Response headers'


admin.site.register(RequestLog, RequestLogAdmin)
