from django import template
from apps.authentication.utils import check_big_boss

register = template.Library()


@register.simple_tag
def check_big_boss(user):
    """Check rol user"""
    return check_big_boss(user)
