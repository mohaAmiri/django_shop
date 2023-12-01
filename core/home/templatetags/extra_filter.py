from django import template

# *name of register is important

register = template.Library()


@register.filter()
def upper_name(value):
    return value.upper()
