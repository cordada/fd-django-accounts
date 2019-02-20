import django  # noqa: F401

DEBUG = False
TIME_ZONE = 'UTC'
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "^e8thszumk=vywe=-9!6aizo^+h*rf2v8$88*_*@^194&-^3)n"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'PORT': 5432,
        'NAME': 'accounts_dev',
        'USER': 'django_dev',
        'PASSWORD': 'django_dev',
        'ATOMIC_REQUESTS': False,
        'AUTOCOMMIT': True,
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "fd_dj_accounts",
    'fd_accounts',
]

MIDDLEWARE = ()

###############################################################################
# auth and package-related
###############################################################################

AUTH_USER_MODEL = 'fd_accounts.User'
FD_ACCOUNTS_SYSTEM_USER = 'accounts-system-user@localhost'
