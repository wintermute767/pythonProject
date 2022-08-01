from django import template
import re

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return str(value) * arg

@register.filter(name='censor')
def censor(value):
    pattern=[
        'бля',
        'пздц',
        'еблан',
        'пидар',
        'сука',
        'тварь',
        'ублюдок',
    ]
    rezult=str(value)
    for patt in pattern:
        rezult=re.sub(patt, '███████', rezult)
    return rezult