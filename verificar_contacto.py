"""
Script temporal para verificar datos de contacto de emergencia
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ob_care.settings')
django.setup()

from matronaApp.models import FichaObstetrica

# Obtener la ficha 1
ficha = FichaObstetrica.objects.get(pk=1)

print("=" * 60)
print(f"Ficha: {ficha.numero_ficha}")
print("=" * 60)
print(f"Nombre contacto emergencia: [{ficha.nombre_contacto_emergencia}]")
print(f"Teléfono emergencia: [{ficha.telefono_emergencia}]")
print(f"Parentesco: [{ficha.parentesco_contacto_emergencia}]")
print("=" * 60)

# Verificar si están vacíos o None
if not ficha.nombre_contacto_emergencia:
    print("⚠️ El nombre de contacto de emergencia está vacío!")
if not ficha.telefono_emergencia:
    print("⚠️ El teléfono de emergencia está vacío!")
if not ficha.parentesco_contacto_emergencia:
    print("⚠️ El parentesco está vacío!")
