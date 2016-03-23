"""
startup script for slack_bot_manager project.

It syncs the slack bot table by inspecting installed apps

"""

from django.conf import settings
#from django.apps import apps

def update_manager_models():
    pass
#    for model in apps.get_models():
#        import pdb; pdb.set_trace()
#        pass

def run():
    update_manager_models()
