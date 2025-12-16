"""
Script standalone para poblar catálogos
"""
import os
import django

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from partosApp.catalogos_nuevos import CatalogoRegimenParto, CatalogoTipoRoturaMembrana

def poblar():
    print("📋 Poblando Catálogo Régimen de Parto...")
    
    regimenes_data = [
        {'codigo': 'REGIM_0', 'descripcion': 'Cero (Sin restricciones)', 'orden': 1},
        {'codigo': 'REGIM_LIBRE', 'descripcion': 'Régimen Libre', 'orden': 2},
        {'codigo': 'REGIM_LIVIANO', 'descripcion': 'Régimen Liviano', 'orden': 3},
        {'codigo': 'REGIM_LIQUIDO', 'descripcion': 'Régimen Líquido', 'orden': 4},
        {'codigo': 'REGIM_ABSOLUTO', 'descripcion': 'Régimen Absoluto (Ayuno)', 'orden': 5},
        {'codigo': 'REGIM_HIDRICO', 'descripcion': 'Régimen Hídrico', 'orden': 6},
    ]

    for item in regimenes_data:
        obj, created = CatalogoRegimenParto.objects.get_or_create(
            codigo=item['codigo'],
            defaults={
                'descripcion': item['descripcion'],
                'orden': item['orden'],
                'activo': True
            }
        )
        status = "✅ Creado" if created else "⏭️  Ya existe"
        print(f"  {status}: {obj.descripcion}")

    print("📋 Poblando Catálogo Tipo de Rotura de Membranas...")
    
    roturas_data = [
        {'codigo': 'ESPONTANEA', 'descripcion': 'Rotura Espontánea', 'orden': 1},
        {'codigo': 'ARTIFICIAL', 'descripcion': 'Rotura Artificial (Amniotomía)', 'orden': 2},
        {'codigo': 'TARDIA', 'descripcion': 'Rotura Tardía', 'orden': 3},
        {'codigo': 'PREMATURA', 'descripcion': 'Rotura Prematura de Membranas (RPM)', 'orden': 4},
        {'codigo': 'PROLONGADA', 'descripcion': 'Rotura Prematura Prolongada (>18h)', 'orden': 5},
        {'codigo': 'INTEGRAS', 'descripcion': 'Membranas Íntegras', 'orden': 6},
    ]

    for item in roturas_data:
        obj, created = CatalogoTipoRoturaMembrana.objects.get_or_create(
            codigo=item['codigo'],
            defaults={
                'descripcion': item['descripcion'],
                'orden': item['orden'],
                'activo': True
            }
        )
        status = "✅ Creado" if created else "⏭️  Ya existe"
        print(f"  {status}: {obj.descripcion}")

if __name__ == '__main__':
    poblar()
