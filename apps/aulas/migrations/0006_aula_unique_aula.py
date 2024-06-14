# Generated by Django 5.0.6 on 2024-06-12 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aulas', '0005_notificacion_unique_notificacion'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='aula',
            constraint=models.UniqueConstraint(fields=('nombre',), name='unique_aula'),
        ),
    ]