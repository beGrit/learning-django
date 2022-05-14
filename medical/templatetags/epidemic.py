import datetime

from django import template
from pyecharts.charts import Line
from pyecharts.options import MarkPointOpts, MarkPointItem, MarkLineOpts, MarkLineItem, TooltipOpts, ToolboxOpts, \
    AxisOpts

from medical.models import DailyIncreaseVirusData

register = template.Library()


@register.inclusion_tag('custom/components/epidemic/card.html')
def week_data():
    end_time = now = datetime.datetime.now()
    delta = datetime.timedelta(days=6)
    start_time = now - delta
    virus_data_list = list(DailyIncreaseVirusData.objects.filter(date__lte=end_time).filter(date__gte=start_time).order_by('date').all())
    if virus_data_list is not None:
        week_name_list = []
        definite = []
        cure = []
        dead = []
        asymptomatic = []
        for item in virus_data_list:
            week_name_list.append(item.date)
            definite.append(item.definite)
            cure.append(item.cure)
            dead.append(item.dead)
            asymptomatic.append(item.asymptomatic)
        line = Line(init_opts={
            'width': '1600px',
            'height': '800px',
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
        virus_data_item = {
            'description': '一周数据折线图',
            'items': [],
            'charts': [line_data],
        }
    else:
        virus_data_item = None
    return {
        'virus_data_item': virus_data_item,
    }
