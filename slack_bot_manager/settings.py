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
    'manager',
    'linkbot',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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


### Slack API Access Key
SLACK_ACCESS_KEY='barf-3443977346-C2J58ecuMIf7zPCBccUdmE5g'


### LINK BOT CONFIG
LINKBOT_QUIPS=[
    '%s',
    'linkbot noticed a link!  %s',
    'Oh, here it is... %s',
    'Maybe this will help?  %s',
    'Click me!  %s',
    'Here, let me link that for you... %s',
    'Couldn\'t help but notice %s was mentioned...',
    'Not that I was eavesdropping, but did you mention %s?',
    'hmmmm, try...  %s'
]

LINKBOT_MATCHES=[
    (
        r'^(.* |)((req|inc)[0-9]+)([ ?.,].*|)',
        '<https://uw.service-now.com/u_simple_requests.do?sysparm_type=labels&sysparm_table=u_simple_requests&sysparm_query=number=%s|%s>',
        LINKBOT_QUIPS
    ),
    (
        r'^(.* |)((%s)-[0-9]+)([ ?.,].*|)' % ('|'.join([
                        'ALP','CAL','CAT','CVS','RAD','EWS','GRADE','GRP','IDCARD',
                        'IDCARD','LCRA','MM','MSCASUB','MYUW','MYPLAN','MUWM',
                        'PAN','PWS','SCOUT','SPOT','SQLSHR','SWS'])),
        '<https://jira.cac.washington.edu/browse/%s|%s>',
        LINKBOT_QUIPS
    )
]
