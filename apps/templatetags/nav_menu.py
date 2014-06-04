from django import template
from apps.models import ThematicGroup

register = template.Library()

@register.inclusion_tag('components/nav.html')
def navigation_menu():
	nav_groups = ThematicGroup.objects.all()
	return {'nav_groups': nav_groups}
