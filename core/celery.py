from __future__ import absolute_import , unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# Establecer el módulo de configuración predeterminado de Django para el programa 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.conf.enable_utc = False
app.conf.update(timezone = 'Europe/Madrid')
#app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'django-db'

# Usar una cadena aquí significa que no tendrá que serializar la configuración del objeto a través de la red.
app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'send-mail-every-day-at-13':{
        'task': 'apps.authentication.tasks.send_notifications',
        'schedule': crontab(hour=19, minute = 5), # cada día a las 13h
        'args': ('D',),
    },
    'send-mail-every-week-at-10': {
        'task': 'apps.authentication.tasks.send_notifications',
        'schedule': crontab(day_of_week='6', hour=16, minute=0),  # cada lunes a las 10h
        'args': ('S',),
    },
    'send-mail-every-month-at-15': {
        'task': 'apps.authentication.tasks.send_notifications',
        'schedule': crontab(day_of_month='1', hour=15, minute=0),  # el primer día de cada mes a las 15h
        'args': ('M',),
    },
    'write-data-every-minute': {
        'task': 'apps.home.tasks.write_data_every_minute',
        'schedule': crontab(minute='*/1'),  # genera datos random cada minuto
    },
    'read-data-every-minute': {
        'task': 'apps.home.tasks.read_data_every_minute',
        'schedule': crontab(minute='*/1'),  # genera datos random cada minuto
    },
    'read-media-data-every-minute': {
        'task': 'apps.home.tasks.read_media_data_every_minute',
        'schedule': crontab(minute='*/1'),  # genera datos random cada minuto
    },

}

# Cargar tareas de todos los módulos de aplicaciones registradas en Django.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
