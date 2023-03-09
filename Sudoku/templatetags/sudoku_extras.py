from django import template

register = template.Library()


@register.simple_tag
def get_width(index=None):
	if index == 1 or (index-1) % 3 != 0:
		return 1
	else:
		return 5

