from django import template


register = template.Library()


@register.filter(name='bad_word')
def bad_word(value):
    lst = ['жопа', 'тварь', 'сволочь', 'твари']
    value = value.split()
    for el in value:
        if el.lower() in lst:
            value.remove(el)
    return ' '.join(value)

