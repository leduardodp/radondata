# admin.py en la aplicación 'aulas'
from django.contrib import admin
from .forms import NotificacionAdminForm
from .models import Aula, Notificacion
from django.contrib.auth.models import Group


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ('nombre','grupo' , 'descripcion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('grupo',)

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    form = NotificacionAdminForm
    list_display = ('usuario', 'aula', 'preferencia')
    list_filter = ('preferencia','aula',)
    search_fields = ('usuario__username', 'aula__nombre')


#Para ver que aulas pertenecen a cada grupo
class AulaInline(admin.TabularInline):
    model = Aula
    extra = 0


class GroupAdmin(admin.ModelAdmin):
    inlines = [
        AulaInline,
    ]

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)