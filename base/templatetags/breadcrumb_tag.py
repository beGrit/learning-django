from django import template

register = template.Library()


@register.inclusion_tag('base/components/breadcrumb.html')
def breadcrumb(active_label: str | None | list = None):
    if type(active_label) == list:
        pass
    else:
        return {
            'active_label': active_label,
        }
