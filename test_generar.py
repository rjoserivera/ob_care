import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from django.core.management import call_command

print("=" * 70)
print("EJECUTANDO GENERADOR DE DATOS DEMO")
print("=" * 70)
print()

try:
    call_command('generar_datos_demo', '--cantidad', '5')
    print("\n[OK] Comando ejecutado exitosamente")
except Exception as e:
    print(f"\n[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()
