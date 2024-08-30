from django import template

register = template.Library()

@register.filter
def range_filter(value):
    """Returns a range of numbers."""
    return range(value)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)