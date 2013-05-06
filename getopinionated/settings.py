#!/usr/bin/env python
# Django settings for getopinionated project.
import sys, os
from os.path import dirname

SITE_ROOT = dirname(dirname(os.path.realpath(__file__)))
sys.path.insert(0, os.path.join(SITE_ROOT, 'libs'))

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Brussels'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'static/media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://localhost:8000/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'tmp/static')#Override this on your server

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'common.middleware.SSLRedirect',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    # "django.middleware.cache.FetchFromCacheMiddleware",
)

ROOT_URLCONF = 'getopinionated.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'getopinionated.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	os.path.join(SITE_ROOT, 'templates'),
    os.path.join(SITE_ROOT, 'libs/share/templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django.contrib.redirects',
    'django.contrib.flatpages',
    'common',
    'accounts',
	'proposing',
    'document',
    'django.contrib.humanize',
    'libs.sorl.thumbnail',
    'libs.share',
    'social_auth',
    # external apps
    'south'
)

AUTHENTICATION_BACKENDS = (
    'accounts.backend.EmailModelBackend',
    'accounts.backend.CustomUserModelBackend',
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
    'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# used by CustomUserModelBackend
CUSTOM_USER_MODEL = 'accounts.CustomUser'

### SSL settings (common.middleware.SSLRedirect) ###
# Forced SSL
SSL_URLS = (
    r'^/admin/',
    r'^/accounts/',
	r'.*',
)
# May be SSL & not SSL
MIXED_URLS = (
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#         #'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         #'LOCATION': '127.0.0.1:11211',
#     }
# }

# default url after login (used in contrib.auth)
LOGIN_REDIRECT_URL = '/'

# gets access to 'request' variable in templates
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)
 

# favour django-mailer but fall back to django.core.mail
if "mailer" in INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail

MAILER_LOCKFILE = os.path.join(SITE_ROOT, 'send_mail.lock')
MAILER_PAUSE_SEND = False



TWITTER_CONSUMER_KEY         = ''
TWITTER_CONSUMER_SECRET      = ''
FACEBOOK_APP_ID              = ''
FACEBOOK_API_SECRET          = ''
LINKEDIN_CONSUMER_KEY        = ''
LINKEDIN_CONSUMER_SECRET     = ''
GOOGLE_OAUTH2_CLIENT_ID      = ''
GOOGLE_OAUTH2_CLIENT_SECRET  = ''

LOGIN_URL          = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/logout/'
LOGIN_ERROR_URL    = '/accounts/login-error/'

#SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/another-login-url/'

#SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/new-users-redirect-url/'
#SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/new-association-redirect-url/'
#SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account-disconnected-redirect-url/'
SOCIAL_AUTH_BACKEND_ERROR_URL = '/accounts/new-error-url/'
#SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
#SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

#TODO: fix if needed?
SOCIAL_AUTH_USER_MODEL = 'accounts.CustomUser'


SOCIAL_AUTH_FORCE_POST_DISCONNECT = True

#####################################################################################
# Import local settings
#####################################################################################
try:
    from local_settings import *
except ImportError:
    try:
        from mod_python import apache
        apache.log_error("You need to copy local_settings.py.example to local_settings.py and edit settings")
    except ImportError:
        import sys
        sys.stderr.write("You need to copy local_settings.py.example to local_settings.py and edit settings")

TEMPLATE_DEBUG = DEBUG
MANAGERS = ADMINS

# easier template debugging (http://stackoverflow.com/questions/4300442/show-undefined-variable-errors-in-templates)
if DEBUG:
    class InvalidString(str):
        def __mod__(self, other):
            # hack for bug in admin
            if str(other) == 'header.class_attrib':
                return
            from django.template.base import TemplateSyntaxError
            raise TemplateSyntaxError(
                "Undefined variable or unknown value for: \"%s\"" % other)
    TEMPLATE_STRING_IF_INVALID = InvalidString("%s")
