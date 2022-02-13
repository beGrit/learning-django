import datetime

from django.template.response import TemplateResponse

from medical.models import COVIDActivity, Vaccination


def home_page(request):
    return TemplateResponse(request, 'custom/pages/home/home.html')


def activity_vaccination_subscribe(request):
    today = datetime.datetime.today()
    week_days = [('星期一', 0),
                 ('星期二', 1),
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
