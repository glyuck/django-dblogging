import factory
from django.contrib.auth.models import User, AnonymousUser

from dblogging.models import RequestLog


class SuperuserF(factory.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.sequence(lambda n: 'root%i' % n)
    email = factory.sequence(lambda n: 'root%i@root.root' % n)
    password = 'password'
    is_staff = True
    is_active = True
    is_superuser = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(SuperuserF, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user


class RequestLogF(factory.DjangoModelFactory):
    FACTORY_FOR = RequestLog

    ip = '127.0.0.1'
    user_repr = str(AnonymousUser())
    method = 'GET'
    host = 'localhost'
    path = '/'
    response_status_code = 200
    total_time = 0.01
