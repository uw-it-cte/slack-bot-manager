from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request, template='bot_manager/home.html'):
    context = {}
    return render_to_response(template, context, RequestContext(request))
