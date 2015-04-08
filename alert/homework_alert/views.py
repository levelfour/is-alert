from django.shortcuts import render
from homework_alert.models import Homework


def index(request):
    works = Homework.objects.all()
    return render(request, 'homework_alert/index.html', {'works': works})
