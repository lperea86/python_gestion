from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Categoria, UnidadMedida, Producto, Profile, AppPermission

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

class UnidadForm(forms.ModelForm):
    class Meta:
        model = UnidadMedida
        fields = ['nombre']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'codigo', 'talle', 'color', 'categoria', 'unidad_medida', 'cantidad']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['es_admin', 'permisos']
        widgets = {'permisos': forms.CheckboxSelectMultiple}

class PermissionForm(forms.ModelForm):
    class Meta:
        model = AppPermission
        fields = ['codename', 'descripcion']

class BuscarProductoForm(forms.Form):
    q = forms.CharField(label="Buscar producto", max_length=100, required=False)
