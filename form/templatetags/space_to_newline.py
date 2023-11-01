from django import template

register = template.Library()


@register.filter
def space_to_newline(value):
    return value.replace(' ', '\n')
