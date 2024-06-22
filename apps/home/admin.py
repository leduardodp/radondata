from django.contrib import admin
from django_celery_beat.admin import PeriodicTaskAdmin as BasePeriodicTaskAdmin, CrontabScheduleAdmin as BaseCrontabScheduleAdmin
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule, ClockedSchedule, SolarSchedule


# Desregistrar modelos si ya están registrados
models = [PeriodicTask, CrontabSchedule, ClockedSchedule, SolarSchedule, IntervalSchedule]
for model in models:
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass

# Crear una clase personalizada heredando de la original para ocultar los campos en PeriodicTask
class CustomPeriodicTaskAdmin(BasePeriodicTaskAdmin):
    exclude = ('clocked', 'solar_schedule', 'interval_schedule')

# Registrar el modelo PeriodicTask con la configuración personalizada
admin.site.register(PeriodicTask, CustomPeriodicTaskAdmin)

# Registrar el modelo CrontabSchedule con la configuración original
admin.site.register(CrontabSchedule, BaseCrontabScheduleAdmin)

# No registrar ClockedSchedule, SolarSchedule e IntervalSchedule para mantenerlos ocultos