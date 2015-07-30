from django import template

register = template.Library()

@register.filter(name = 'getkey')
def getDicKey(dictionary, key):
    return dictionary.get(key)

