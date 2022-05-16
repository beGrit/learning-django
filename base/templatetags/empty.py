from django import template

register = template.Library()


@register.inclusion_tag('base/components/empty.html')
def show_empty():
    return {}


@register.inclusion_tag('base/components/empty_img_placeholder.html')
def show_img_placeholder(type: str = 'img-thumbnail'):
    return {
        'type': type,
    }
