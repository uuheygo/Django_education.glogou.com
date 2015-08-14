from django import template
from urllib import unquote
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            t, v = d.split(':')
            x = unquote(v)
            attrs[t] = unquote(v)

    return field.as_widget(attrs=attrs)



