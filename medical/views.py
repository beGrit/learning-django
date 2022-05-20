import datetime

from django import urls
from django.db import transaction
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import ListView, DetailView

from base.views import CommonTableListView
from medical.forms import VaccinationSubscribeForm, VolunteerRegisterForm
from medical.models import Vaccination, Volunteer, News, Drug, Equipment, \
    Hospital, Vaccine


def home_page(request):
    home_banner_items = [
        {
            'details_url_path': reverse('medical:vaccine-list'),
            'title': '查疫苗',
            'description': '快来看看最新的疫苗',
        },
        {
            'details_url_path': reverse('medical:drug-list'),
            'title': '查药品',
            'description': '不知道吃啥药？快来看看药品信息大全',
        },
        {
            'details_url_path': reverse('medical:equipment-list'),
            'title': '查器材',
            'description': '看看有哪些有用的器材',
        },
        {
            'details_url_path': reverse('medical:hospital-list'),
            'title': '查医院',
            'description': '看看附近有哪些医院？',
        },
    ]
    news_arr = list(News.objects.all().order_by('-publish_date_time')[:5])
    if news_arr is not None:
        popularization_articles = []
        for news in news_arr:
            popularization_articles.append({
                'facade_image_url_path': news.image_url_path,
                'title': news.title,
                'content': news.content,
                'detail_route_path': news.get_detail_route_path(),
            })
    else:
        popularization_articles = None
    return TemplateResponse(request,
                            'custom/pages/home/home.html',
                            context={
                                'home_banner_items': home_banner_items,
                                'popularization_articles': popularization_articles
                            })


def epidemic(request):
    return TemplateResponse(request,
                            'custom/pages/epidemic/index.html',
                            context={
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
    week_days = week_days[today.isoweekday() - 1:] + week_days[0:today.isoweekday() - 1]

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
                vaccination = Vaccination.objects.get(id=vaccination_id)
                vaccination.amount_of_subscribe += 1
                vaccination.save()
                return HttpResponseRedirect(urls.reverse('medical:activity-vaccination-subscribe-success'))
    else:
        vaccination_subscribe_form = VaccinationSubscribeForm(initial=initial)
    return TemplateResponse(request, 'custom/pages/activity/vaccination/subscribe_form.html', {
        'form': vaccination_subscribe_form
    })


def subscribe_vaccination_success(request):
    return TemplateResponse(request, 'custom/pages/activity/vaccination/subscribe_success.html')


def hospital_list(request: HttpRequest):
    hospital_data_list = [
        {
            'name': '四川大学华西医院',
            'level_name': '三级甲等',
            'address_name': '四川省成都市武侯区国学巷37号',
            'badge_path': 'medical/images/hospital/badge/img_01.png',
            'details_url': reverse('medical:hospital-details', kwargs={
                'hospital_id': 1,
            }),
            'tag_data': {
                '三级甲等', '可做核酸',
            },
        },
        {
            'name': '四川省人民医院',
            'level_name': '三级甲等',
            'address_name': '成都市一环路西二段32号',
            'badge_path': '/medical/images/hospital/badge/image_01.png',
            'details_url': '',
            'tag_data': {
                '三级甲等', '可做核酸', '系统推荐',
            },
        },
        {
            'name': '四川省肿瘤医院',
            'level_name': '三级甲等',
            'address_name': '成都市人民南路55号',
            'badge_path': '/medical/images/hospital/badge/image_01.png',
            'details_url': '',
            'tag_data': {
                '三级甲等',
            },
        },
        {
            'name': '四川省人民医院',
            'level_name': '三级甲等',
            'address_name': '成都市一环路西二段32号',
            'badge_path': '/medical/images/hospital/badge/image_01.png',
            'details_url': '',
            'tag_data': {
                '三级甲等', '可做核酸', '系统推荐',
            },
        },
        {
            'name': '四川省第二人民医院',
            'level_name': '三级甲等',
            'address_name': '成都市一环路西二段32号',
            'badge_path': '/medical/images/hospital/badge/image_01.png',
            'details_url': '',
            'tag_data': {
                '三级甲等', '可做核酸',
            },
        },
    ]
    return TemplateResponse(request, 'custom/pages/hospital/index.html', context={
        'hospital_data_list': hospital_data_list,
    })


def hospital_details(request, hospital_id):
    hospital_details_data = {
        'name': '四川大学华西医院',
        'level_name': '三级甲等',
        'address_name': '成都市人民南路55号',
        'badge_path': '/medical/images/hospital/badge/img_01.png',
        'description': '锦江春色来天地，玉垒浮云变古今。    在中国历史文化名城成都市锦江万里桥头的华西坝，有一座闻名遐迩的医学城，她就是四川大学华西临床医学院/华西医院。    追溯历史，华西医院起源于美国、加拿大、英国等国基督教会1892年在成都创建的仁济、存仁医院；华西临床医学院起源于1914年的华西协合大学医科，是由美、加、英等国教会按西方医学教育模式建立的医学院。1937年抗日战争全面爆发，中央大学、燕京大学、齐鲁大学、金陵大学、金陵女子文理学院内迁成都，与华西协合大学联合办学办医，是时，华西坝大师云集、名家汇萃、盛况空前。1938年，有医学院的华大、中大、齐大组建联合医院；1946年，华西协合大学医院在现址全部建成，简称华西医院。    1951年，新中国人民政府接管华西协合大学；1953年，经院系调整为四川医学院，医院更名为四川医学院附属医院；1985年，四川医学院更名为华西医科大学，医院更名为华西医科大学附属第一医院；2000年，四川大学与华西医科大学合并，2001年5月，学院/医院更名为四川大学华西临床医学',
    }
    return TemplateResponse(request, 'custom/pages/hospital/details.html', context={
        'hospital_details_data': hospital_details_data,
    })


def news_list(request):
    news_arr = list(News.objects.all())
    if len(news_arr) == 0:
        news_arr = None
    return render(request, 'custom/pages/news/news_list.html', {
        'data': news_arr,
    })


def volunteer_register_form(request: HttpRequest):
    if request.method == 'POST':
        form = VolunteerRegisterForm(request.POST)
        form.full_clean()
        if form.is_valid():
            with transaction.atomic():
                model: Volunteer = form.save(commit=False)
                model.related_user = request.user
                model.support_type = 1
                model.work_year = 0
                model.email = model.related_user.email
                model.save()
                return HttpResponseRedirect(urls.reverse('medical:activity-vaccination-subscribe-success'))
    else:
        form = VolunteerRegisterForm()
    return TemplateResponse(request, 'custom/pages/volunteer/register_form.html', {
        'form': form
    })


def property_list(request):
    return render(request, 'custom/pages/property/index.html')


class DrugListView(CommonTableListView):
    model = Drug
    paginate_by = 5

    def get_headers(self):
        return ['编码', '药物名', '价格', '上架时间']

    def get_body_fields_name(self):
        return ['code', 'name', 'price', 'produced_date_time']

    def get_breadcrumb_name(self):
        return self.model._meta.model_name


class EquipmentListView(CommonTableListView):
    model = Equipment
    paginate_by = 5

    def get_headers(self):
        return ['编码', '装备名', '价格', '上架时间']

    def get_body_fields_name(self):
        return ['code', 'name', 'price', 'produced_date_time']

    def get_breadcrumb_name(self):
        return self.model._meta.model_name


class HospitalListView(ListView):
    model = Hospital
    paginate_by = 5

    def get_detail_route(self):
        return 'medical:hospital-detail'


class HospitalDetailView(DetailView):
    model = Hospital

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actions = []
        # Add vaccination activity.
        vaccination = Vaccination.objects.filter(related_builder_area__related_hospital_id=self.object.id).first()
        if vaccination is not None:
            actions.append(
                {
                    'name': '最新疫苗预约',
                    'action_route': reverse('medical:activity-vaccination-subscribe-form', kwargs={
                        'vaccination_id': vaccination.id,
                    }),
                },
            )
        context['actions'] = actions
        return context


class VaccineListView(CommonTableListView):
    model = Vaccine
    paginate_by = 3

    def get_headers(self):
        return ['疫苗名', '简介 ']

    def get_body_fields_name(self):
        return ['name', 'description']

    def get_breadcrumb_name(self):
        return self.model._meta.model_name


class NewsDetailsView(DetailView):
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
