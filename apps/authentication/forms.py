# -*- encoding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from .models import CustomUser

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Usuario",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Usuario",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Correo electrónico",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repite contraseña",
                "class": "form-control"
            }
        ))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo electrónico.")
        return email


class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nombre",
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Apellidos",
                "class": "form-control"
            }
        ))
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Usuario",
                "class": "form-control"
            }
        ))
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Correo electrónico",
                "class": "form-control"
            }
        ))
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nº teléfono",
                "class": "form-control"
            }
        ))
    profile_pic = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "placeholder": "Foto de perfil",
                "class": "form-control"
            }
        ))
    
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','username', 'email', 'phone','profile_pic')

