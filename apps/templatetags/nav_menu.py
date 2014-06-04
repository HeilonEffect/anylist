from django import template
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup
from apps.models import ThematicGroup

register = template.Library()


@register.inclusion_tag('components/header.html')
def main_menu(title='', user=''):
	nav_groups = ThematicGroup.objects.all()
	return {'header': title, 'nav_groups': nav_groups, 'user': user}


@register.filter
def add_class(html, css_class):
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup.children:
        if tag.name != 'script':
            if 'class' in tag:
                tag['class'].append(css_class)
            else:
                tag['class'] = [css_class]

    return mark_safe(soup.renderContents())