from django.shortcuts import render


def favicon(request):
    return render(request, 'favicon.svg', content_type="image/svg+xml")


def robots(request):
    return render(request, 'robots.txt', content_type='text/plain')
