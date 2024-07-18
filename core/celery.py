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
    'send-mail-every-day-at-12':{
        'task': 'apps.authentication.tasks.send_notifications',
        'schedule': crontab(hour=23, minute = 45), # cada día a las 23h 45
        'args': ('D',),
    },
    'send-mail-every-week-at-1': {
        'task': 'apps.authentication.tasks.send_notifications',
        'schedule': crontab(day_of_week='1', hour=1, minute=0),  # cada lunes a las 1h
        'args': ('S',),
    },
    'send-mail-every-month-at-2': {
        'task': 'apps.authentication.tasks.send_notifications',
        'schedule': crontab(day_of_month='28-31', hour =23 , minute = 55),  # el último dia del mes a las 23h 55
        'args': ('M',),
    },
    'write-data-every-minute': {
        'task': 'apps.home.tasks.write_data_every_minute',
        'schedule': crontab(minute='*/10'),  # genera datos random cada 10 minutos
    },
    'read-data-every-minute': {
        'task': 'apps.home.tasks.read_daily_data',
        'schedule': crontab(minute='*/10'),  # lee datos random cada 10 minutos
    },
    'read-daily-media-data-every-minute': {
        'task': 'apps.home.tasks.read_daily_media_data',
        'schedule': crontab(minute='*/10'),  # lee la media diaria cada 10 minutos
    },
    'read-weekly-media-data-every-minute': {
        'task': 'apps.home.tasks.read_weekly_media_data',
        'schedule': crontab(minute='*/10'),  # lee la media semanal random cada 10 minutos
    },
    'read-monthly-media-data-every-minute': {
        'task': 'apps.home.tasks.read_monthly_media_data',
        'schedule': crontab(minute='*/10'),  # lee la media mensual cada 10 minutos
    },
    
}

# Cargar tareas de todos los módulos de aplicaciones registradas en Django.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
