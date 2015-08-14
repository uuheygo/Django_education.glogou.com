from django import template

register = template.Library()

@register.filter(name = 'wheregoshopping')
def wheregoshopping(request):
    if request.get_host().find('wheregoshopping') >=0:
        return True
    return False