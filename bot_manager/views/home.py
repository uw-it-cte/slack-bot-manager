from django.shortcuts import render


def home(request, template='bot_manager/home.html'):
    context = {}
    return render(request, template, context)
