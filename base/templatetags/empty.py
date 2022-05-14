from django import template

register = template.Library()


@register.inclusion_tag('base/components/empty.html')
def show_empty():
    return {}
