from django import forms
from apps.aulas.models import Aula, Notificacion


class PreferenciaNotificacionesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario')
        super(PreferenciaNotificacionesForm, self).__init__(*args, **kwargs)
        grupos_usuario = usuario.groups.all()
        aulas = Aula.objects.filter(grupo__in=grupos_usuario).distinct()
        for aula in aulas:
            notificacion = Notificacion.objects.filter(usuario=usuario, aula=aula).first()
            self.fields[f'preferencia_{aula.id}'] = forms.ChoiceField(
                label=f'Notificaciones {aula.nombre}',
                choices=Notificacion.PREFERENCIAS_NOTIFICACION,
                widget=forms.Select(attrs={'class': 'form-select'}),
                initial=notificacion.preferencia if notificacion else Notificacion.NINGUNA
            )

#Filtro aula - grupo desde el admin
class NotificacionAdminForm(forms.ModelForm):
    class Meta:
        model = Notificacion
        fields = '__all__'

    def clean(self):
        # Llama al método clean de la superclase para obtener los datos limpios del formulario
        cleaned_data = super().clean()
        
        # Obtén los datos específicos que necesitamos validar
        usuario = cleaned_data.get("usuario")
        aula = cleaned_data.get("aula")
        
        # Realiza la validación solo si ambos campos están presentes
        if usuario and aula:
            # Comprueba si el aula seleccionada está en los grupos a los que pertenece el usuario
            if not Aula.objects.filter(id=aula.id, grupo__in=usuario.groups.all()).exists():
                # Si no es así, lanza un error de validación
                raise forms.ValidationError(f'El usuario {usuario} no tiene acceso al aula {aula}.')
        
        # Devuelve los datos limpios si todo está bien
        return cleaned_data

        