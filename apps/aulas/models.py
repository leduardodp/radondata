from django.db import models
from django.conf import settings
from apps.authentication.models import CustomUser
from django.contrib.auth.models import Group


class Aula(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    grupo = models.ForeignKey(Group,on_delete=models.CASCADE ,null=True, blank= True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nombre'], name='unique_aula')
        ]

    def __str__(self):
        return self.nombre

class Notificacion(models.Model):
    DIARIA = 'D'
    SEMANAL = 'S'
    MENSUAL = 'M'
    NINGUNA = 'N'

    PREFERENCIAS_NOTIFICACION = [
        (DIARIA, 'Diariamente'),
        (SEMANAL, 'Semanalmente'),
        (MENSUAL, 'Mensualmente'),
        (NINGUNA, 'No notificar')
    ]

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    preferencia = models.CharField(
        max_length=1,
        choices=PREFERENCIAS_NOTIFICACION,
        default=NINGUNA
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'aula'], name='unique_notificacion')
        ]

    def __str__(self):
        return f'Notificación de {self.usuario} para {self.aula}: {self.get_preferencia_display()}'