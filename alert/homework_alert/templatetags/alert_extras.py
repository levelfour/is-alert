import datetime as dt
from django.utils import timezone
from django import template
from homework_alert.models import UserHomework


register = template.Library()

@register.filter
def is_done(work, user_id):
    return len(UserHomework.objects.filter(user_id=user_id, homework_id=work.id)) == 1

@register.filter
def style(work, user_id):
    until_deadline = work.deadline - timezone.now()
    if is_done(work, user_id):
        if until_deadline < dt.timedelta(days=0):
            return 'deadline'
        else:
            return 'done'
    elif until_deadline < dt.timedelta(days=2):
        return 'alert'
    else:
        return ''
