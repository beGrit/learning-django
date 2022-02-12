from django.template.response import TemplateResponse


def home_page(request):
    return TemplateResponse(request, 'custom/pages/home/home.html')


def activity_vaccination_subscribe(request):
    return TemplateResponse(request, 'custom/pages/activity/vaccination/subscribe.html')
