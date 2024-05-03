from django import forms
from .models import *

from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']


class RegistroForm(forms.ModelForm):
    password1 = forms.CharField(label='Crea una clave para acceso', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '*********',
            'id': 'ClaveAcceso',
            'required': 'required',
        }
    ))

    password2 = forms.CharField(label='Repite la clave por favor', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '*********',
            'id': 'RepiteClave',
            'required': 'required',
        }
    ))

    class Meta:
        model = MiUsuario
        fields = ['nombres', 'apellidos', 'nombre_usuario', 'email', 'fecha_nacimiento', 'direccion']
        widgets = {
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: Emma Elizabeth',
                    'id': 'NombreCompleto',
                    'required': 'required',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: Mansilla Zanlongo',
                    'id': 'Apellidos',
                    'required': 'required',
                }
            ),
            'nombre_usuario': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: Pomni_Emma',
                    'id': 'NombreUsuario',
                    'required': 'required',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: Pomni_Emma@gmail.com',
                    'id': 'CorreoElectronico',
                    'required': 'required',
                }
            ),
            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'id': 'FechaNacimiento',
                    'required': 'required',
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese dirección de despacho',
                    'id': 'DireccionDespacho',
                }
            ),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    

class ModificarUsuarioForm(forms.ModelForm):
    class Meta:
        model = MiUsuario
        fields = ['nombres', 'apellidos', 'email', 'direccion']    