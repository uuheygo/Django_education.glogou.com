from django import template

register = template.Library()

@register.filter(name = 'changespace')
def changespace(cat):
    cat = cat.replace(" ", "_")
    return cat