from django.contrib.auth.models import User
from django.db import models


class RequestLog(models.Model):
    when = models.DateTimeField(auto_now_add=True)
    ip = models.IPAddressField()
    session_key = models.CharField(max_length=32, blank=True, null=True, default=None)
    user = models.ForeignKey(User, null=True, blank=True, default=None)
    user_repr = models.CharField(max_length=255)
    method = models.CharField(max_length=16)
    host = models.CharField(max_length=255)
    path = models.CharField(max_length=4000)  # IE8 limit is ~2048, mssql limit is 4000
    query = models.CharField(max_length=4000)
    post = models.TextField()
    files = models.TextField()
    cookies = models.TextField()
    request_headers = models.TextField()
    response_headers = models.TextField()
    response_status_code = models.IntegerField()
    response_body = models.TextField(blank=True, null=True, default=None)
    total_time = models.FloatField()

    class Meta:
        get_latest_by = 'when'
