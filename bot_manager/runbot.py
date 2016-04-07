from importlib import import_module
from multiprocessing import get_logger

def run_slackbot(bot_module_name, bot_class_name, settings):
    bot_module = import_module(bot_module_name)
    bot_class = getattr(bot_module, bot_class_name)
    bot_class(settings, logger=get_logger()).bot()
