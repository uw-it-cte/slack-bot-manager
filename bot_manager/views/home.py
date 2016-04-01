from django.shortcuts import render
from django.template import RequestContext

# Create your views here.

def home(request):
    context = {
        'supporttools_parent_app': 'Slack',
        'supporttools_parent_app_url': 'http://uw-it-aca.slack.com',
    }
    return render(request, 'bot_manager/home.html', context=context)
