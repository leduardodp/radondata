from django.http import HttpResponse
from django.shortcuts import redirect
#Un decorador es una función que toma otra función como parámetro y nos permite agregar una funcionalidad antes de llamar a la función original
#Esto se hace para que un usuario autenticado no pueda ir a la pantalla de login/register
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
        
    return wrapper_func

#Esto se hace para que un usuario pueda acceder solo a las vistas que le permite su rol
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No tienes permisos para acceder a esta página')
        return wrapper_func
    return decorator