from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from PIL import Image

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