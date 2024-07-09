from collections import defaultdict
import datetime
from celery import shared_task
from django.core.mail import send_mail
from apps.aulas.models import Notificacion
from apps.home.tasks import get_media_diaria, get_media_semanal , get_media_mensual

@shared_task(bind=True)
def send_notifications(self,frequency):

    if frequency == 'D':
        label = 'diaria'
        
    elif frequency == 'S':
        label = 'semanal'
        
    elif frequency == 'M':
        label = 'mensual'
        
    else:
        return
    
    if frequency == "M":
        fecha_actual = datetime.now()
        siguiente_dia = fecha_actual + datetime.timedelta(days=1)
        if (siguiente_dia.month == fecha_actual.month):
            return
    
    notificaciones_por_usuario = defaultdict(list) # Diccionario para agrupar notificaciones por usuario
    
    notificaciones = Notificacion.objects.filter(preferencia=frequency)
    
    for notificacion in notificaciones:
        user = notificacion.usuario
        aula = notificacion.aula
        
        if frequency == "D":
            media_diaria = get_media_diaria(aula.nombre)
            message = f'Aquí están los datos de concentracion media {label} para {aula.nombre}:   \n\n {media_diaria} Bq/m3'
        elif frequency == 'S':
            media_semanal = get_media_semanal(aula.nombre)
            message = f'Aquí están los datos de concentracion media {label} para {aula.nombre}:   \n\n {media_semanal} Bq/m3'
        elif frequency == 'M':
            media_mensual = get_media_mensual(aula.nombre)
            message = f'Aquí están los datos de concentracion media {label} para {aula.nombre}:   \n\n {media_mensual} Bq/m3'
            
        
        # Agregar el mensaje al diccionario agrupado por usuario
        notificaciones_por_usuario[user].append(message)
        
        
    for user, mensajes in notificaciones_por_usuario.items():
        subject = f'Concentración media de radón {label}'
        email_from = 'ldagostino@alumnos.uvigo.es'
        mensaje_completo = '\n\n'.join(mensajes)  # Concatenar todos los mensajes para el usuario
        send_mail(subject, mensaje_completo, email_from, [user.email])