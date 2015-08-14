from django import template

register = template.Library()

@register.filter(name = 'getRes')
def getRes(p,q):
    return p%q