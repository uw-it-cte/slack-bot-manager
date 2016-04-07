##
## run the slackbot 
##
## it needs to be self contained for windows multiprocessing
##


def run_slackbot(bot_module_name, bot_class_name, settings):
    from importlib import import_module
    from multiprocessing import get_logger

    bot_module = import_module(bot_module_name)
    bot_class = getattr(bot_module, bot_class_name)
    logger = get_logger()

    try:
        bot_class(settings, logger=logger).bot()
    except:
        logger.error('run_slackbot instantiate FAILED')
        return
