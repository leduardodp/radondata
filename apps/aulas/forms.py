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
        