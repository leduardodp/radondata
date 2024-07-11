
from django import forms
from django.contrib.auth.forms import UserCreationForm 
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
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input"
                }
        ),
        label="Recordarme"
    )


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
    
    #Función para comprobar si el usuario/email ya está registrado
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Ya existe un usuario con este nombre de usuario.")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo electrónico.")
        
        return cleaned_data


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


