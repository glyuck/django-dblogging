from django.http import HttpResponse


def test(request):
    return HttpResponse('Sample response', content_type='text/html')
