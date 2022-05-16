import datetime

from django import template
from pyecharts.charts import Line
from pyecharts.options import MarkPointOpts, MarkPointItem, MarkLineOpts, MarkLineItem, TooltipOpts, ToolboxOpts, \
    AxisOpts

from medical.models import DailyIncreaseVirusData, StaticsVirusData

register = template.Library()


@register.inclusion_tag('custom/components/epidemic/card.html')
def daily_data():
    # Build daily data.
    now = datetime.datetime.now()
    today = now.day
    daily_virus_entity = DailyIncreaseVirusData.objects.filter(date__day=today).first()
    if daily_virus_entity is not None:
        daily_items = daily_virus_entity.get_items()
        daily_charts = []
        bar_data = daily_virus_entity.render_as_bar()
        pie_data = daily_virus_entity.render_as_pie()
        daily_charts.append(bar_data)
        daily_charts.append(pie_data)
        data = {
            'title': '每日数据统计',
            'items': daily_items,
            'charts': daily_charts,
        }
    else:
        data = None
    return {
        'data': data,
    }


@register.inclusion_tag('custom/components/epidemic/card.html')
def week_data():
    end_time = now = datetime.datetime.now()
    delta = datetime.timedelta(days=6)
    start_time = now - delta
    data_list = list(
        DailyIncreaseVirusData.objects.filter(date__lte=end_time).filter(date__gte=start_time).order_by('date').all())
    if data_list is not None:
        week_name_list = []
        definite = []
        cure = []
        dead = []
        asymptomatic = []
        for item in data_list:
            week_name_list.append(item.date)
            definite.append(item.definite)
            cure.append(item.cure)
            dead.append(item.dead)
            asymptomatic.append(item.asymptomatic)
        line = Line(init_opts={
            'width': '500px',
            'height': '600px',
        })
        line.add_xaxis(xaxis_data=week_name_list)
        line.add_yaxis(
            series_name="确诊",
            y_axis=definite,
        )
        line.add_yaxis(
            series_name="治愈",
            y_axis=cure,
        )
        line.add_yaxis(
            series_name="死亡",
            y_axis=dead,
        )
        line.add_yaxis(
            series_name="无症状",
            y_axis=asymptomatic,
        )
        line.set_global_opts(
            tooltip_opts=TooltipOpts(trigger="axis"),
            toolbox_opts=ToolboxOpts(is_show=True),
            xaxis_opts=AxisOpts(type_="category", boundary_gap=False),
        )
        line_data = line.render_embed()
        data = {
            'title': '一周数据折线图',
            'items': [],
            'charts': [line_data],
        }
    else:
        data = None
    return {
        'data': data,
    }


@register.inclusion_tag('custom/components/epidemic/card.html')
def all_data():
    # Build statics data.
    statics_virus_entity = StaticsVirusData.objects.filter(label='all').filter(type=0).first()
    if statics_virus_entity is not None:
        statics_items = statics_virus_entity.get_items()
        statics_charts = []
        bar_data = statics_virus_entity.render_as_bar()
        pie_data = statics_virus_entity.render_as_pie()
        statics_charts.append(bar_data)
        statics_charts.append(pie_data)
        data = {
            'title': statics_virus_entity.description,
            'items': statics_items,
            'charts': statics_charts,
        }
    else:
        data = None
    return {
        'data': data,
    }


@register.inclusion_tag('custom/components/epidemic/cards.html')
def period_data():
    # Build period statics data.
    period_virus_entity = list(StaticsVirusData.objects.filter(publish_status=1).filter(type=1).all())
    if len(period_virus_entity) != 0:
        data = []
        for statics_virus_entity in period_virus_entity:
            statics_items = statics_virus_entity.get_items()
            statics_charts = []
            bar_data = statics_virus_entity.render_as_bar()
            pie_data = statics_virus_entity.render_as_pie()
            statics_charts.append(bar_data)
            statics_charts.append(pie_data)
            period_statics_data = {
                'title': statics_virus_entity.description,
                'items': statics_items,
                'charts': statics_charts,
            }
            data.append(period_statics_data)
    else:
        data = None
    return {
        'data_list': data,
    }
