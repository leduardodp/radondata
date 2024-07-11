from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from .forms import LoginForm, SignUpForm , UpdateProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user



# Create your views here.

@unauthenticated_user
def login_view(request):
    form = LoginForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                remember_me = "on" in form.data.get("remember_me", [])
                if remember_me:
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)
                return redirect("/")
            else:
                messages.error(request, 'Usuario y/o contraseña incorrectos')
                return redirect("/")
        else:
            messages.error(request,'¡Algo ha ido mal! Inténtalo otra vez')
    context = {"form":form}
    return render(request, "accounts/login.html", context)

@unauthenticated_user
def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user =form.save()
            username = form.cleaned_data.get("username")

            messages.success(request, "Usuario creado con éxito, {}\n¡Bienvenido!".format(username))
            return redirect("/")

        else:
            messages.error(request,' Algo ha ido mal!')
    else:
        form = SignUpForm()

    context = {"form":form}
    return render(request, "accounts/register.html", context)

@login_required(login_url="login/")
def logout_view(request):
    logout(request)
    messages.success(request, "Se ha cerrado la sesión correctamente.")
    return redirect("login")

@login_required(login_url="login/")
def profile(request):
    user = request.user
    context={"user": user}
    return render(request, "accounts/profile.html", context)


@login_required(login_url="login/")
def update_profile(request):
    user = request.user
    form = UpdateProfileForm(instance=user)
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Su perfil ha sido actualizado correctamente!")
            return redirect("profile")
    
    context = {"form":form}
    return render(request, "accounts/update_profile.html", context)

