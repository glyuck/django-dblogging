import time

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import MiddlewareNotUsed
from django.utils import simplejson

from dblogging.models import RequestLog


class RequestLogMiddleware(object):
    def __init__(self):
        if not getattr(settings, 'DBLOGGING_ENABLED', False):
            raise MiddlewareNotUsed('Enable dblogging middleware via '
                                    'DBLOGGING_ENABLED=True in your settings')

    def get_headers(self, request):
        return dict((header.lstrip('HTTP_').replace('_', '-'), value)
                    for header, value in request.META.items() if header.startswith('HTTP_'))

    def process_request(self, request):
        self.start = time.time()  # TODO: Better use time.clock on windows platform?

    def process_response(self, request, response):
        user = getattr(request, 'user', None)
        RequestLog.objects.create(
            ip=request.META.get('REMOTE_ADDR', ''),
            session_key=request.session.session_key,
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
            total_time=time.time() - self.start if hasattr(self, 'start') else 0)
        return response
