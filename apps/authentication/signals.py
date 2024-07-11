from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import CustomUser
from apps.aulas.models import Aula, Notificacion
from PIL import Image

#Añadir al usuario a un grupo por defecto
@receiver(post_save, sender=CustomUser)
def add_user_to_default_group(sender, instance, created, **kwargs):
    if created:
            #Asigna grupo default
            group, created = Group.objects.get_or_create(name='student')
            instance.groups.add(group)

            # Asignar notificaciones para cada aula del grupo
            aulas = Aula.objects.filter(grupo=group)
            for aula in aulas:
                Notificacion.objects.create(
                    usuario=instance,
                    aula=aula,
                    preferencia=Notificacion.NINGUNA
                )


#Limitar tamaño foto
@receiver(post_save, sender=CustomUser)
def resize_profile_pic(sender, instance, **kwargs):
    if instance.profile_pic:
        try:
            img = Image.open(instance.profile_pic.path)

            if img.height > 250 or img.width > 250:
                output_size = (250, 250)
                img.thumbnail(output_size)
                img.save(instance.profile_pic.path)
        except Exception as e:
            print(f"Error processing image: {e}")