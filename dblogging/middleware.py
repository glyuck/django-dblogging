import time
import datetime

from django.contrib.auth.models import User
from django.core.exceptions import MiddlewareNotUsed
from django.utils import simplejson

from dblogging.conf import settings
from dblogging.models import RequestLog


class RequestLogMiddleware(object):
    def __init__(self):
        if not settings.DBLOGGING_ENABLED:
            raise MiddlewareNotUsed('Enable dblogging middleware via '
                                    'DBLOGGING_ENABLED=True in your settings')

    def get_headers(self, request):
        def header_name(header):
            if header.startswith('HTTP_'):
                header = header[5:]
            return header.replace('_', ' ').title().replace(' ', '-')
        return dict((header_name(header), value)
                    for header, value in request.META.items() if header.startswith('HTTP_'))

    def process_request(self, request):
        self.start = time.time()  # TODO: Better use time.clock on windows platform?

    def process_response(self, request, response):
        for url_re in settings.DBLOGGING_IGNORE_URLS:
            if url_re.match(request.get_full_path()):
                return response

        user = getattr(request, 'user', None)
        session_key = None
        if hasattr(request, 'session'):
            session_key = request.session.session_key
        RequestLog.objects.create(
            ip=request.META.get('REMOTE_ADDR', ''),
            session_key=session_key,
            user=user if user and user.is_authenticated() and isinstance(user, User) else None,
            user_repr=str(user),
            method=request.method,
            host=request.get_host(),
            path=request.path,
            query=request.META.get('QUERY_STRING', ''),
            post=simplejson.dumps(dict(request.POST.items())),
            cookies=simplejson.dumps(dict(request.COOKIES.items())),
            request_headers=simplejson.dumps(self.get_headers(request)),
            response_headers=simplejson.dumps(dict(response.items())),
            response_status_code=response.status_code,
            response_body=response.content if settings.DBLOGGING_SAVE_RESPONSE_BODY else None,
            total_time=time.time() - self.start if hasattr(self, 'start') else 0)

        # Delete old RequestLog entries
        if settings.DBLOGGING_LOG_EXPIRY_SECONDS:
            RequestLog.objects.filter(when__lt=datetime.datetime.now() - datetime.timedelta(seconds=settings.DBLOGGING_LOG_EXPIRY_SECONDS)).delete()

        return response
