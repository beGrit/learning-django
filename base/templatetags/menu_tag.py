from django import template

register = template.Library()


@register.inclusion_tag('base/components/menu.html')
def menu_item_list():
    return {
        'menus': [
            {
                'path': 'medical:home-page',
                'name': '首页',
            },
            {
                'path': 'medical:home-page',
                'name': '资讯专栏',
            },
            {
                'path': 'medical:home-page',
                'name': '医疗数据专栏',
            },
            {
                'path': 'medical:home-page',
                'name': '物资专栏',
            },
            {
                'path': 'medical:epidemic-index',
                'name': '疫情信息专栏',
            },
            {
                'path': 'medical:volunteer-register-form',
                'name': '志愿者申请',
            },
            {
                'path': 'medical:activity-vaccination-subscribe',
                'name': '疫苗预约',
            },
            {
                'path': 'chat:available-chat-rooms',
                'name': '聊天室',
            }
        ]
    }
