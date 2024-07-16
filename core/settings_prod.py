import os
from pathlib import Path
from django.contrib.messages import constants as messages


# Mensajes alertas
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-dark',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent.parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#########PARAMETROS DE PRODUCCIÓN#########
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# load production server from .env
ALLOWED_HOSTS  =['*']


INSTALLED_APPS = [
    #BASE APPS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #LOCAL APPS
    'apps.home',
    'apps.authentication',
    'apps.aulas',
    #EXTERNAL APPS
    'django_cleanup.apps.CleanupConfig', #Actualizar foto perfil ( borra la anterior)
    'django_celery_results',  #Log de tareas desde admin Django
    'django_celery_beat',  #Tareas programadas
    'django_extensions',  #Comandos de Django
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

CSRF_TRUSTED_ORIGINS = ['https://radondata.sytes.net/']
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in home/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.csrf',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', 
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/es/5.0/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
)

MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR, 'media')



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "authentication.CustomUser"

##Envio de Emails
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
#EMAIL_USE_SSL = True #Send data
EMAIL_USE_TLS = True  #Reset password
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

## Celery Worker Settings

CELERY_BROKER_URL = 'redis://redis:6379/0'  #La URL del broker de mensajería que se utilizará para enviar y recibir tareas
accept_content = ['json'] #El tipo de contenido que se aceptará para las tareas
task_serializer = 'json' #El serializador que se utilizará para serializar las tareas
result_serializer = 'json' #El serializador que se utilizará para serializar los resultados de las tareas
timezone = 'Europe/Madrid' #La zona horaria que se utilizará para las tareas
result_backend = 'django-db'


## Celery Beat
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


