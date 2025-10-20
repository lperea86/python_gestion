from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Producto, Categoria, UnidadMedida, Profile, AppPermission
from .forms import (
    LoginForm, CategoriaForm, UnidadForm, ProductoForm,
    ProfileForm, PermissionForm, BuscarProductoForm
)

# -------------------
# Funciones auxiliares
# -------------------

def tiene_permiso(user, codename: str) -> bool:
    """Verifica si el usuario tiene un permiso o es admin."""
    if not user.is_authenticated:
        return False
    if hasattr(user, "profile"):
        perfil = user.profile
        if perfil.es_admin:
            return True
        return perfil.permisos.filter(codename=codename).exists()
    return False


def requiere_permiso(codename):
    return user_passes_test(lambda u: tiene_permiso(u, codename), login_url="login")


# -------------------
# Autenticación
# -------------------

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("dashboard")
    return render(request, "core/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# -------------------
# Dashboard y Maestros
# -------------------

@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")


@login_required
def maestros(request):
    return render(request, "core/maestros.html")


# -------------------
# Usuarios / Perfiles / Permisos
# -------------------

@login_required
@requiere_permiso("ver_usuarios")
def usuarios_list(request):
    usuarios = User.objects.select_related("profile").all()
    return render(request, "core/usuarios_list.html", {"usuarios": usuarios})


@login_required
@requiere_permiso("administrar_perfiles")
def perfil_editar(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    perfil = usuario.profile
    form = ProfileForm(request.POST or None, instance=perfil)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Perfil actualizado correctamente.")
        return redirect("usuarios_list")
    return render(request, "core/categoria_form.html", {"form": form, "titulo": f"Editar perfil de {usuario.username}"})


@login_required
@requiere_permiso("administrar_permisos")
def permiso_crear(request):
    form = PermissionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Permiso creado correctamente.")
        return redirect("maestros")
    return render(request, "core/categoria_form.html", {"form": form, "titulo": "Crear permiso"})


# -------------------
# Catálogos (Categoría / Unidad de Medida)
# -------------------

@login_required
@requiere_permiso("administrar_catalogos")
def categoria_crear(request):
    form = CategoriaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Categoría creada correctamente.")
        return redirect("productos_list")
    return render(request, "core/categoria_form.html", {"form": form, "titulo": "Nueva Categoría"})


@login_required
@requiere_permiso("administrar_catalogos")
def unidad_crear(request):
    form = UnidadForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Unidad creada correctamente.")
        return redirect("productos_list")
    return render(request, "core/unidad_form.html", {"form": form, "titulo": "Nueva Unidad"})


# -------------------
# Productos (ABM + búsqueda)
# -------------------

@login_required
@requiere_permiso("ver_productos")
def productos_list(request):
    form_buscar = BuscarProductoForm(request.GET or None)
    productos = Producto.objects.select_related("categoria", "unidad_medida").all()
    if form_buscar.is_valid():
        q = form_buscar.cleaned_data.get("q")
        if q:
            productos = productos.filter(nombre__icontains=q) | productos.filter(codigo__icontains=q)
    return render(request, "core/productos_list.html", {"productos": productos, "form_buscar": form_buscar})


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "core/producto_form.html"
    success_url = reverse_lazy("productos_list")

    def dispatch(self, request, *args, **kwargs):
        if not tiene_permiso(request.user, "crear_productos"):
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        messages.success(self.request, "Producto creado correctamente.")
        return super().form_valid(form)


class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "core/producto_form.html"
    success_url = reverse_lazy("productos_list")

    def dispatch(self, request, *args, **kwargs):
        if not tiene_permiso(request.user, "editar_productos"):
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Producto actualizado correctamente.")
        return super().form_valid(form)


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = "core/producto_confirm_delete.html"
    success_url = reverse_lazy("productos_list")

    def dispatch(self, request, *args, **kwargs):
        if not tiene_permiso(request.user, "eliminar_productos"):
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)
