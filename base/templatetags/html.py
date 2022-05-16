from django import template

register = template.Library()


@register.inclusion_tag('base/components/image_node.html')
def image_node(src, type: int = 0):
    # (0, '200 * 200'), (1, 'full'), (2, '400 * 400')
    return {
        'src': src,
        'type': type,
    }
