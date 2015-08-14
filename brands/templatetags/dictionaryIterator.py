from django import template

register = template.Library()

@register.filter(name = 'dictionaryIterator')
def dictionaryIterator(dictionary):
    return sorted(dictionary.keys())