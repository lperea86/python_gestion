#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'softnet_gestion.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

from core.models import AppPermission

permisos = [
    "ver_usuarios",
    "administrar_perfiles",
    "administrar_permisos",
    "ver_productos",
    "crear_productos",
    "editar_productos",
    "eliminar_productos",
    "administrar_catalogos",
]

for codename in permisos:
    AppPermission.objects.get_or_create(codename=codename, descripcion=f"Permiso para {codename}")

print("✅ Permisos creados correctamente.")

