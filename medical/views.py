import datetime

from django import urls
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.db import transaction

from medical.forms import VaccinationSubscribeForm
from medical.models import Vaccination


def home_page(request):
    home_banner_items = [
        {
            'details_url_path': '',
            'title': '查疾病',
            'description': '不知道生啥病了？快来看看权威疾病百科',
        },
        {
            'details_url_path': '',
            'title': '查药品',
            'description': '不知道吃啥药？快来看看药品信息大全',
        },
        {
            'details_url_path': '',
            'title': '查医院',
            'description': '看看附近有哪些医院？',
        },
        {
            'details_url_path': '',
            'title': '查检查/手术',
            'description': '检查与手术专业百科',
        },
        {
            'details_url_path': '',
            'title': '查疫苗',
            'description': '疫苗还有多少？哪些疫苗适合你呢？',
        },
        {
            'details_url_path': '',
            'title': '测一测',
            'description': '你是否困惑自己是不是到底生病了没？这里有专业的试题，评估您的问题',
        },
    ]
    popularization_articles = [
        {
            'facade_image_url_path': '',
            'title': '',
            'content': '',
            'detail_url_path': '',
        },
    ]
    return TemplateResponse(request,
                            'custom/pages/home/home.html',
                            context={
                                'home_banner_items': home_banner_items,
                                'home_article': {
                                    'popularization_articles': popularization_articles
                                },
                            })


def activity_vaccination_subscribe(request):
    today = datetime.datetime.today()
    week_days = [('星期一', 0),
                 ('星期二', 2),
                 ('星期三', 3),
                 ('星期四', 4),
                 ('星期五', 5),
                 ('星期六', 6),
                 ('星期日', 7)]
    week_days = week_days[today.isoweekday():] + week_days[0:today.isoweekday()]

    daily_vaccinations = []
    for index, week_day in enumerate(week_days):
        itr_datetime = today + datetime.timedelta(days=index)
        vaccinations = Vaccination.objects.filter(process_date_time__year=itr_datetime.year,
                                                  process_date_time__month=itr_datetime.month,
                                                  process_date_time__day=itr_datetime.day)
        forenoon = list(vaccinations.filter(process_date_time__hour__lte=12).all())
        afternoon = list(vaccinations.filter(process_date_time__hour__gt=12).all())
        daily_vaccinations.append(
            {
                week_day: {
                    'forenoon': forenoon,
                    'afternoon': afternoon,
                }
            })

    return TemplateResponse(request, 'custom/pages/activity/vaccination/subscribe.html', {
        'daily_vaccinations': daily_vaccinations
    })


def subscribe_vaccination_form(request, vaccination_id=1):
    initial = {
        'related_vaccination': Vaccination.objects.get(id=vaccination_id)
    }
    if request.method == 'POST':
        vaccination_subscribe_form = VaccinationSubscribeForm(request.POST, initial=initial)
        vaccination_subscribe_form.full_clean()
        if vaccination_subscribe_form.is_valid():
            # vaccination_subscribe_form.related_vaccination.amount_of_subscribe += 1
            with transaction.atomic():
                vaccination_subscribe_form.save()
                vaccination_subscribe_form.after_save()
                return HttpResponseRedirect(urls.reverse('medical:activity-vaccination-subscribe-success'))
    else:
        vaccination_subscribe_form = VaccinationSubscribeForm(initial=initial)
    return TemplateResponse(request, 'custom/pages/activity/vaccination/subscribe_form.html', {
        'form': vaccination_subscribe_form
    })


def subscribe_vaccination_success(request):
    return TemplateResponse(request, 'custom/pages/activity/vaccination/subscribe_success.html')
