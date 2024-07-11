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
