from django import template

register = template.Library()


@register.inclusion_tag('base/dummy.html')
def model_view(template_name: str):
    return {
        'template': template_name,
    }


@register.inclusion_tag('base/components/pagination.html')
def pagination(page_obj):
    return {
        'page_obj': page_obj,
    }
