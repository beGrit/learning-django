from django import template

register = template.Library()


@register.inclusion_tag('base/dummy.html')
def model_view(template_name: str):
    return {
        'template': template_name,
    }
