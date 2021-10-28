from django.shortcuts import render


def http400(request, exception=None):
    return render(request, 'common/400.html')


def http403(request, exception=None):
    return render(request, 'common/403.html')


def http404(request, exception=None):
    return render(request, 'common/404.html')


def http500(request):
    return render(request, 'common/500.html')
