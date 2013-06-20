from appconf import AppConf
from django.conf import settings


class DBLoggingConf(AppConf):
    # Main switch
    ENABLED = settings.DEBUG
    # Should we save response body to database?
    SAVE_RESPONSE_BODY = False
    # regexp patterns for ignored urls
    IGNORE_URLS = ()
    # delete logs after # seconds
    LOG_EXPIRY_SECONDS = 60 * 60 * 24 * 30  # 30 days
