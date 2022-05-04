import datetime

from django import urls
from django.db import transaction
from django.http import HttpResponseRedirect, HttpRequest
from django.template.response import TemplateResponse
from django.urls import reverse
from pyecharts.charts import Bar, Pie

from medical.forms import VaccinationSubscribeForm, VolunteerRegisterForm
from medical.models import Vaccination, Volunteer


def home_page(request):
    home_banner_items = [
        {
            'details_url_path': '',
            'title': '查疫苗',
            'description': '快来看看最新的疫苗',
        },
        {
            'details_url_path': '',
            'title': '查药品',
            'description': '不知道吃啥药？快来看看药品信息大全',
        },
        {
            'details_url_path': '',
            'title': '查器材',
            'description': '看看有哪些有用的器材',
        },
        {
            'details_url_path': reverse('medical:hospital-index'),
            'title': '查医院',
            'description': '看看附近有哪些医院？',
        },
        {
            'details_url_path': reverse('medical:hospital-index'),
            'title': '查医生',
            'description': '看看有哪些医生',
        },
        {
            'details_url_path': reverse('medical:activity-vaccination-subscribe'),
            'title': '查看疫苗接种活动',
            'description': '查看疫苗接种活动',
        },
    ]
    popularization_articles = [
        {
            'facade_image_url_path': '/media/medical/images/home-article/img_01.png',
            'title': '四川省新型冠状病毒肺炎疫情最新情况（3月14日发布）',
            'content': '截至3月13日24时，全省累计报告新型冠状病毒肺炎确诊病例1568例（其中境外输入940例），累计治愈出院1405例，死亡3例，目前在院隔离治疗160例，1784人尚在接受医学观察。',
            'detail_url_path': '',
        },
        {
            'facade_image_url_path': '/media/medical/images/home-article/img_1.png',
            'title': '四川将全力推进国家中医药综合改革示范区和中医药强省建设',
            'content': '四川新闻网-首屏新闻成都3月14日讯（记者 李丹）日前，2022年全省中医药工作暨中医药系统党风廉政建设工作电视电话会在成都召开。2021年，全省中医药系统开拓创新、担当作为，中医药事业产业文化“三位一体”高质量发展取得新成效，在疫情防控中彰显独特作用。2022年，全省中医药系统认真贯彻党中央、国务院和省委、省政府决策部署，坚持传承精华、守正创新，大力弘扬中医药文化，提升中医药服务能力，壮大中医药现代产业规模，加快推进中医药强省建设，更好造福全省人民。要坚持中西医并重，深化中医药改革，加强人才培养、科技创新和药品研发，全力推进国家中医药综合改革示范区建设，以优异成绩迎接党的二十大和省第十二次党代会胜利召开。',
            'detail_url_path': '',
        },
        {
            'facade_image_url_path': '',
            'title': '四川:13条措施支持医疗健康装备产业发展,补助资金最高达5000万元',
            'content': '''
            四川在线记者 张彧希

　　省政府办公厅近日印发《关于支持医疗健康装备产业高质量发展的若干政策措施》，13条措施聚焦核心技术攻关、创新平台建设、加大研发投入、创新成果转化、产业发展支持等方面，着力培育产业新动能，打造新优势。

　　近年来，我国大力推进高端医疗装备进口替代和自主可控。四川省高度重视医药健康产业发展，将包括医疗健康装备产业在内的医药健康产业纳入“5+1”现代工业体系进行重点培育。新冠疫情发生后，医疗健康装备在打赢疫情防控阻击战中发挥了重要作用。“为抢抓医疗健康装备产业发展机遇，加快培育和招引生成一批具有引领示范意义的重大项目，加速产业延链强链和集聚发展，推动我省医疗健康装备产业实现新突破，出台支持医疗健康装备产业高质量发展的相关政策措施十分必要。”省经信厅相关负责人说，这是全国第一个省级层面关于医疗健康装备产业的政策措施。

　　此次出台的《政策措施》，“创新驱动”特征明显。13条措施中，有6条在聚焦核心技术攻关、创新平台建设、提升临床研究能力、加大研发投入、智能装备开发和创新成果转化等。“在加强核心技术攻关上，提出了要聚焦医疗健康行业发展的重点和关键，以需‘定榜’。”省经信厅相关负责人解读。在创新平台建设和创新成果转化上，补助资金最高可达5000万元。

　　《政策措施》还特别提到支持新业态新模式、支持企业登峰发展。新业态新模式包括企业牵头会同医疗健康机构投资建设的远程诊疗、智能诊断、数据中心等医疗健康装备集成创新服务平台等；支持企业登峰发展，一方面对国内外医疗健康装备标杆企业和头部企业来川设立地区总部、研发中心、生产基地等，纳入招引重点，加强地方配套支持；另一方面，对医疗健康装备“贡嘎培优”企业、“单项冠军”企业和专精特新“小巨人”企业，按有关规定给予奖补。''',
            'detail_url_path': '',
        },
        {
            'facade_image_url_path': '',
            'title': '成都鼓励设立“首席健康官”！职场医疗再获官方助力',
            'content': '近日，成都高新区印发《关于鼓励企业建立首席健康官制度的通知》，明确企业要发挥健康管理主体作用，企业可根据组织架构和工作实际需要，分层级设立首席健康官、健康管理专员。目前，富士康、腾讯、天府软件园、银泰城等10家企业、专业园区、商业商务楼宇已作为区内首批示范点位率先“试水”。',
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


def epidemic(request):
    virus_data = [
        {
            'label': '新增确诊',
            'data': 4,
        },
        {
            'label': '新增本土',
            'data': 0,
        },
        {
            'label': '新增境外',
            'data': 4,
        },
        {
            'label': '新增无症状',
            'data': 9,
        },
        {
            'label': '现存确诊',
            'data': 152,
        },
        {
            'label': '累计确诊',
            'data': 1572,
        },
        {
            'label': '累计治愈',
            'data': 1417,
        },
        {
            'label': '累计死亡',
            'data': 3,
        },
    ]

    x_axis = []
    data_axis = []
    for virus_item in virus_data:
        x_axis.append(virus_item['label'])
        data_axis.append(virus_item['data'])

    # Build the bar chart.
    bar = Bar(init_opts={
        'width': '500px',
        'height': '300px',
    })
    bar.add_xaxis(x_axis)
    bar.add_yaxis("今日疫情走势", y_axis=data_axis, color='#FF6A57')
    bar_data = bar.render_embed()

    # Build the pie chart.
    pie = Pie(init_opts={
        'width': '500px',
        'height': '600px',
    })
    pie_data_pair = []
    for data_item in virus_data:
        pie_data_pair.append([
            data_item['label'],
            data_item['data'],
        ])
    pie.add(series_name='', data_pair=pie_data_pair)
    pie_data = pie.render_embed()
    return TemplateResponse(request,
                            'custom/pages/epidemic/index.html',
                            context={
                                'virus_data': virus_data,
                                'bar_data': bar_data,
                                'pie_data': pie_data,
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
    pass


def volunteer_register_form(request: HttpRequest):
    if request.method == 'POST':
        form = VolunteerRegisterForm(request.POST)
        form.full_clean()
        if form.is_valid():
            with transaction.atomic():
                model: Volunteer = form.save(commit=False)
                model.support_type = 1
                model.work_year = 0
                model.save()
                return HttpResponseRedirect(urls.reverse('medical:activity-vaccination-subscribe-success'))
    else:
        form = VolunteerRegisterForm()
    return TemplateResponse(request, 'custom/pages/volunteer/register_form.html', {
        'form': form
    })
