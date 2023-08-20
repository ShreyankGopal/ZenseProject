from django import template

register = template.Library()

@register.filter
def ends_with_iiitb_com(email):
    return email.lower().endswith('@iiitb.com')