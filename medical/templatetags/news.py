import datetime

from django import template
from pyecharts.charts import Line
from pyecharts.options import MarkPointOpts, MarkPointItem, MarkLineOpts, MarkLineItem, TooltipOpts, ToolboxOpts, \
    AxisOpts

from medical.models import DailyIncreaseVirusData, StaticsVirusData, News

register = template.Library()


@register.inclusion_tag('custom/components/news/news_cards.html')
def recent_news_cards():
    news_list = News.objects.order_by('publish_date_time')[:4]
    return {
        'data_list': news_list,
    }
