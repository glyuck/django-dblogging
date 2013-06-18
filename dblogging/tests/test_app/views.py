from django.http import HttpResponse
from django.shortcuts import redirect


def test(request):
    return HttpResponse('Sample response', content_type='text/html')


def test_redirect(request):
    return redirect('dblogging_test')
