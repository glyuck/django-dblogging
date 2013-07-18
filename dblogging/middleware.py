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

    def get_host(self, request):
        """Returns the HTTP host using the environment or request headers.
        Django1.4 version, doesn't raise SuspiciousOperation if host is not in settings.ALLOWED_HOSTS"""
        # We try three options, in order of decreasing preference.
        if settings.USE_X_FORWARDED_HOST and (
                'HTTP_X_FORWARDED_HOST' in request.META):
            host = request.META['HTTP_X_FORWARDED_HOST']
        elif 'HTTP_HOST' in request.META:
            host = request.META['HTTP_HOST']
        else:
            # Reconstruct the host using the algorithm from PEP 333.
            host = request.META['SERVER_NAME']
            server_port = str(request.META['SERVER_PORT'])
            if server_port != (request.is_secure() and '443' or '80'):
                host = '%s:%s' % (host, server_port)
        return host

    def get_headers(self, request):
        def header_name(header):
            return header[5:].replace('_', ' ').title().replace(' ', '-')
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
        response_body = None
        if settings.DBLOGGING_SAVE_RESPONSE_BODY:
            if isinstance(settings.DBLOGGING_SAVE_RESPONSE_BODY, (bool)):
                response_body = response.content
            else:
                response_body = response.content[:settings.DBLOGGING_SAVE_RESPONSE_BODY]
        RequestLog.objects.create(
            ip=request.META.get('REMOTE_ADDR', ''),
            session_key=session_key,
            user=user if user and user.is_authenticated() and isinstance(user, User) else None,
            user_repr=str(user),
            method=request.method,
            host=self.get_host(request),
            path=request.path,
            query=request.META.get('QUERY_STRING', ''),
            post=simplejson.dumps(dict(request.POST.items())),
            cookies=simplejson.dumps(dict(request.COOKIES.items())),
            request_headers=simplejson.dumps(self.get_headers(request)),
            response_headers=simplejson.dumps(dict(response.items())),
            response_status_code=response.status_code,
            response_body=response_body,
            total_time=time.time() - self.start if hasattr(self, 'start') else 0)

        # Delete old RequestLog entries
        if settings.DBLOGGING_LOG_EXPIRY_SECONDS:
            RequestLog.objects.filter(when__lt=datetime.datetime.now() - datetime.timedelta(seconds=settings.DBLOGGING_LOG_EXPIRY_SECONDS)).delete()

        return response
