from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Producto, PerfilUsuario
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nomProducto', 'descripcion', 'precio', 'porcDesctoSubscriptor', 'porDesctoOferta', 'urlImagenProducto']

class RegistrarUsuarioForm(UserCreationForm):
    rut = forms.CharField(max_length=80, required=True, label="Rut")
    direccion = forms.CharField(max_length=80, required=True, label="Dirección")
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'rut', 'direccion']

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class EditarPerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['rut', 'direccion', 'urlImagenUsuario']

class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']