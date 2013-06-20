DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',

    'dblogging',
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'dblogging.middleware.RequestLogMiddleware',
)

ROOT_URLCONF = 'dblogging.tests.test_app.urls'
SECRET_KEY = "xd0&uj^-gyw-x*u$j-^%g*5bjlt=ufea6aqp+*#3z5^yvjqb#s"

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
)

# django-dblogging settings
DBLOGGING_ENABLED = True
DBLOGGING_SAVE_RESPONSE_BODY = True
DBLOGGING_IGNORE_URLS = []
DBLOGGING_LOG_EXPIRY_SECONDS = 60 * 60 * 24 * 30  # 30 days
