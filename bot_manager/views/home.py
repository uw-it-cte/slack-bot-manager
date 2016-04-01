from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def home(request):
    params = {}
    return render_to_response('bot_manager/home.html',
                              params,
                              context_instance=RequestContext(request))
