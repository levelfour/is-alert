from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader


def index(request):
    template = loader.get_template('homework_alert/index.html')
    return HttpResponse(template.render())
