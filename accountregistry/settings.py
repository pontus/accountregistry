# Django settings for accountregistry project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Pontus Freyhult', 'webmaster@bils.se'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/var/db/django/django.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Stockholm'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

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
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*)m#n)8%d$j=f-r-ww&amp;y(vm5$0xk7x$3z$$(d5f#=zfo1d#ziw'

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
)

ROOT_URLCONF = 'accountregistry.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'accountregistry.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/home/pontusf/accountregistry/templates"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'register',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'djangosaml2',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'djangosaml2.backends.Saml2Backend',
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
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },

        'djangosaml2': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'register': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },


    }
}


LOGIN_URL = '/register/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

from saml2 import BINDING_HTTP_REDIRECT

SAML_ATTRIBUTE_MAPPING = {
    'eduPersonPrincipalName': ('username', ),
    'mail': ('mail', ),
    'givenName': ('first_name', ),
    'sn': ('last_name', ),
}

SAML_CONFIG = {
    "entityid" : "https://accounts.bils.se/saml2/metadata/",
    "service": {
        "sp":{
            "name" : "BILS Account Registry",
            "endpoints":{
                "assertion_consumer_service": ["https://accounts.bils.se/saml2/acs/"],
                "single_logout_service": [("https://accounts.bils.se/saml2/acs/", BINDING_HTTP_REDIRECT)],
            },
	'required_attributes': ['first_name','last_name'],
	'optional_attributes': ['mail', 'email'],
        }
    },
    "key_file" : "/etc/pki/tls/private/accounts.bils.se-nopass.key",
    "cert_file" : "/etc/pki/tls/certs/cert-accounts.bils.se.pem",
    "xmlsec_binary" : "/usr/bin/xmlsec1",
    "attribute_map_dir": "/home/pontusf/accountregistry/attributemaps",
    "metadata": {
        "local": ["/home/pontusf/accountregistry/idp.xml"]
    },
    "organization": {
        "display_name":["Bioinformatics Infrastructure for Life Sciences"]
    },
    "contact_person": [{
        "givenname": "Pontus",
        "surname": "Freyhult",
        "phone": "+46184711060",
        "mail": "pontus.freyhult@it.uu.se",
        "type": "technical",
        }]
}
