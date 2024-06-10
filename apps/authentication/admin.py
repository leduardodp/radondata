from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email','first_name','last_name','get_groups', 'is_active','is_staff', 
    'is_superuser', 'last_login','profile_pic',) #Lista que se ve de todos los usuarios

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Información personal'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
        'user_permissions')}),
        (('Fechas importantes'), {'fields': ('last_login', 'date_joined')}),
        (('Campos adicionales'), {'fields': ('phone', 'profile_pic')}),
    )   #Campos de cada usuario 

    def get_groups(self, obj): #Consulta a que grupo pertenece cada usuario en la pantalla de Admin
        return ', '.join([group.name for group in obj.groups.all()])
    get_groups.short_description = 'Grupo(s)'

    ordering =['-id'] #Aparece ultimo registro de primero en la lista
admin.site.register(CustomUser,CustomUserAdmin)