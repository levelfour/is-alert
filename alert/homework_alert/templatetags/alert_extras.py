from django import template
from homework_alert.models import UserHomework


register = template.Library()

@register.filter
def is_done(work, user_id):
    return len(UserHomework.objects.filter(user_id=user_id, homework_id=work.id)) == 1
