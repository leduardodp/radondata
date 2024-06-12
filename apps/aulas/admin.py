# admin.py en la aplicación 'aulas'
from django.contrib import admin
from .models import Aula, Notificacion
from django.contrib.auth.models import Group


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ('nombre','grupo' , 'descripcion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('grupo',)

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'aula', 'preferencia')
    list_filter = ('preferencia','aula',)
    search_fields = ('usuario__username', 'aula__nombre')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "aula" or db_field.name == "despacho":
            # Get the groups of the logged-in user
            user_groups = request.user.groups.all()
            # Filter Aula objects based on the groups
            kwargs["queryset"] = Aula.objects.filter(grupo__in=user_groups)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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