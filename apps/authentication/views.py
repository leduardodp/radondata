from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from django.contrib import messages

# Create your views here.

def login_view(request):
    form = LoginForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.error(request, 'Usuario y/o contraseña incorrectos')
                return redirect("login/")
        else:
            messages.error(request,'¡Algo ha ido mal! Inténtalo otra vez')
    context = {"form":form}
    return render(request, "accounts/login.html", context)


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            messages.success(request, "¡Su cuenta ha sido creada correctamente!")
            return redirect("login/")

        #else:
            messages.error(request,' Algo ha ido mal!')
    else:
        form = SignUpForm()

    context = {"form":form}
    return render(request, "accounts/register.html", context)
