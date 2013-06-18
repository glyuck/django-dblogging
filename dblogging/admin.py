import datetime

from django.contrib import admin

from dblogging.models import RequestLog


class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('log_when', 'total_time', 'ip', 'session_key', 'user', 'user_repr', 'method', 'path', 'query')
    search_fields = ('ip', 'session_key', 'user_repr', 'path', 'query', 'cookies')
    ordering = ('-id',)

    def log_when(self, obj):
        return obj.when.strftime('%Y-%m-%d %H:%M:%S.%f')


admin.site.register(RequestLog, RequestLogAdmin)
