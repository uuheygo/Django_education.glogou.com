from django import template

register = template.Library()

@register.filter
def nospace(value):
    return value.replace(' ', '_')