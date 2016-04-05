"""
Django settings for slack_bot_manager project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&nno#55zzagdg+c8%=q$j&=_@x-s%csycoz_-!d$6+#x_p2a^$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'templatetag_handlebars',
    'compressor',
    'supporttools',
    'bot_manager',
    'linkbot',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'slack_bot_manager.urls'

WSGI_APPLICATION = 'slack_bot_manager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['DJANGO_DB_NAME'],
        'USER': os.environ['DJANGO_DB_USER'],
        'PASSWORD': os.environ['DJANGO_DB_PASSWORD'],
        'HOST': os.environ['DJANGO_DB_HOST'],
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# Set Static file path
PROJECT_ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\','/')


#COMPRESSOR SETTINGS
COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False

from socket import gethostname
# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.getenv('LOGPATH', '.'), 'slackbot-%s.log' % gethostname()),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'bot_manager': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'linkbot': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}

###
### LINKBOT CONFIG
###
LINKBOT_QUIPS = [
    '%s',
    'linkbot noticed a link!  %s',
    'Oh, here it is... %s',
    'Maybe this, %s, will help?',
    'Click me!  %s',
    'Here, let me link that for you... %s',
    'Couldn\'t help but notice %s was mentioned...',
    'Not that I was eavesdropping, but did you mention %s?',
    'hmmmm, did you mean %s?',
    '%s?  An epic, yet approachable tale...',
    '%s?  Reminds me of a story...',
]

LINKBOT_CONFIG = {
    'API_TOKEN': os.environ.get('LINKBOT_API_TOKEN'),
    'LINKBOTS': [
        {
            'MATCH': '(req|inc)[0-9]+',
            'LINK': '<https://uw.service-now.com/u_simple_requests.do?sysparm_type=labels&sysparm_table=u_simple_requests&sysparm_query=number=%s|%s>',
            'QUIPS': LINKBOT_QUIPS
        },
        {
            'MATCH': '(%s)\-[0-9]+' % ('|'.join([
                        'ALP','CAL','CAT','CVS','RAD','EWS','GRADE','GRP','IDCARD',
                        'IDCARD','LCRA','MM','MSCASUB','MYUW','MYPLAN','MUWM',
                        'PAN','PWS','SCOUT','SPOT','SQLSHR','SWS','MSCASUB'])),
            'LINK': '<https://jira.cac.washington.edu/browse/%s|%s>',
            'QUIPS': LINKBOT_QUIPS,
            'LINK_CLASS': 'JiraLinkBot',
            'JIRA_HOST': os.environ.get('LINKBOT_JIRA_HOST'),
            'JIRA_LOGIN': os.environ.get('LINKBOT_JIRA_LOGIN'),
            'JIRA_PASSWORD': os.environ.get('LINKBOT_JIRA_PASSWORD')
        }
    ]
}
