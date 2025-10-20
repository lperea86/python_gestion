from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('maestros/', views.maestros, name='maestros'),

    # Usuarios
    path('usuarios/', views.usuarios_list, name='usuarios_list'),
    path('perfil/<int:user_id>/', views.perfil_editar, name='perfil_editar'),
    path('permisos/crear/', views.permiso_crear, name='permiso_crear'),

    # Catálogos
    path('categorias/crear/', views.categoria_crear, name='categoria_crear'),
    path('unidades/crear/', views.unidad_crear, name='unidad_crear'),

    # Productos
    path('productos/', views.productos_list, name='productos_list'),
    path('productos/nuevo/', views.ProductoCreateView.as_view(), name='producto_crear'),
    path('productos/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_editar'),
    path('productos/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_eliminar'),
]
