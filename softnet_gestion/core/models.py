from django.db import models
from django.contrib.auth.models import User

class AppPermission(models.Model):
    codename = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.codename


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    es_admin = models.BooleanField(default=False)
    permisos = models.ManyToManyField(AppPermission, blank=True)

    def __str__(self):
        return f"Perfil({self.user.username})"


class Categoria(models.Model):
    nombre = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.nombre


class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=120)
    codigo = models.CharField(max_length=50, unique=True)
    talle = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT)
    cantidad = models.CharField(max_length=20)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
