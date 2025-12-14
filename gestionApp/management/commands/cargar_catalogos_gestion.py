"""
Comando para cargar catálogos de gestionApp
"""
from django.core.management.base import BaseCommand
from gestionApp.models import (
    CatalogoSexo, CatalogoNacionalidad, CatalogoPuebloOriginario,
    CatalogoTurno, CatalogoEspecialidad, CatalogoNivelTens, CatalogoCertificacion
)


class Command(BaseCommand):
    help = 'Carga los catálogos base de gestionApp (Sexo, Nacionalidad, Turno, etc.)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('   CARGANDO CATÁLOGOS DE GESTIÓN'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))
        
        # 1. Sexo
        self.stdout.write('📋 Catálogo Sexo...')
        sexos = [
            ('M', 'Masculino', 1),
            ('F', 'Femenino', 2),
            ('I', 'Intersex', 3)
        ]
        for codigo, nombre, orden in sexos:
            CatalogoSexo.objects.get_or_create(
                codigo=codigo,
                defaults={'nombre': nombre, 'activo': True, 'orden': orden}
            )
        self.stdout.write(self.style.SUCCESS('   ✅ Sexo: 3 registros'))
        
        # 2. Nacionalidad
        self.stdout.write('\n📋 Catálogo Nacionalidad...')
        nacionalidades = [
            ('CL', 'Chilena', 1),
            ('VE', 'Venezolana', 2),
            ('PE', 'Peruana', 3),
            ('BO', 'Boliviana', 4),
            ('CO', 'Colombiana', 5),
            ('HT', 'Haitiana', 6),
            ('AR', 'Argentina', 7),
            ('EC', 'Ecuatoriana', 8),
            ('OT', 'Otra', 99)
        ]
        for codigo, nombre, orden in nacionalidades:
            CatalogoNacionalidad.objects.get_or_create(
                codigo=codigo,
                defaults={'nombre': nombre, 'activo': True, 'orden': orden}
            )
        self.stdout.write(self.style.SUCCESS(f'   ✅ Nacionalidad: {len(nacionalidades)} registros'))
        
        # 3. Pueblo Originario
        self.stdout.write('\n📋 Catálogo Pueblo Originario...')
        pueblos = [
            ('NO', 'No pertenece', 1),
            ('MAP', 'Mapuche', 2),
            ('AYM', 'Aymara', 3),
            ('RAP', 'Rapa Nui', 4),
            ('DIA', 'Diaguita', 5),
            ('LIK', 'Lickanantay', 6),
            ('QUE', 'Quechua', 7),
            ('COL', 'Colla', 8),
            ('KAW', 'Kawésqar', 9),
            ('YAG', 'Yagán', 10)
        ]
        for codigo, nombre, orden in pueblos:
            CatalogoPuebloOriginario.objects.get_or_create(
                codigo=codigo,
                defaults={'nombre': nombre, 'activo': True, 'orden': orden}
            )
        self.stdout.write(self.style.SUCCESS(f'   ✅ Pueblo Originario: {len(pueblos)} registros'))
        
        # 4. Turnos
        self.stdout.write('\n📋 Catálogo Turno...')
        turnos = [
            ('DIA', 'Diurno', 1),
            ('NOC', 'Nocturno', 2),
            ('ROT', 'Rotativo', 3),
            ('VES', 'Vespertino', 4)
        ]
        for codigo, nombre, orden in turnos:
            CatalogoTurno.objects.get_or_create(
                codigo=codigo,
                defaults={'nombre': nombre, 'activo': True, 'orden': orden}
            )
        self.stdout.write(self.style.SUCCESS(f'   ✅ Turno: {len(turnos)} registros'))
        
        # 5. Especialidades Médicas
        self.stdout.write('\n📋 Catálogo Especialidad...')
        especialidades = [
            ('GO', 'Ginecología y Obstetricia', 1),
            ('PED', 'Pediatría', 2),
            ('ANE', 'Anestesiología', 3),
            ('MG', 'Medicina General', 4),
            ('NEO', 'Neonatología', 5),
            ('CIR', 'Cirugía General', 6),
            ('MIF', 'Medicina Interna', 7)
        ]
        for codigo, nombre, orden in especialidades:
            CatalogoEspecialidad.objects.get_or_create(
                codigo=codigo,
                defaults={'nombre': nombre, 'activo': True, 'orden': orden}
            )
        self.stdout.write(self.style.SUCCESS(f'   ✅ Especialidad: {len(especialidades)} registros'))
        
        # 6. Nivel TENS
        self.stdout.write('\n📋 Catálogo Nivel TENS...')
        niveles = [
            ('N1', 'Nivel 1', 1),
            ('N2', 'Nivel 2', 2),
            ('N3', 'Nivel 3', 3)
        ]
        for codigo, nombre, orden in niveles:
            CatalogoNivelTens.objects.get_or_create(
                codigo=codigo,
                defaults={'nombre': nombre, 'activo': True, 'orden': orden}
            )
        self.stdout.write(self.style.SUCCESS(f'   ✅ Nivel TENS: {len(niveles)} registros'))
        
        # 7. Certificaciones
        self.stdout.write('\n📋 Catálogo Certificaciones...')
        certificaciones = [
            ('BLS', 'BLS (Soporte Vital Básico)', 1),
            ('ACLS', 'ACLS (Soporte Vital Avanzado)', 2),
            ('PALS', 'PALS (Soporte Vital Pediátrico)', 3),
            ('NRP', 'NRP (Reanimación Neonatal)', 4)
        ]
        for codigo, nombre, orden in certificaciones:
            CatalogoCertificacion.objects.get_or_create(
                codigo=codigo,
                defaults={'nombre': nombre, 'activo': True, 'orden': orden}
            )
        self.stdout.write(self.style.SUCCESS(f'   ✅ Certificaciones: {len(certificaciones)} registros'))
        
        # Resumen
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('✅ CATÁLOGOS DE GESTIÓN CARGADOS'))
        self.stdout.write('='*60)
        self.stdout.write(f"""
📊 Resumen:
   - Sexo: 3
   - Nacionalidad: {len(nacionalidades)}
   - Pueblo Originario: {len(pueblos)}
   - Turno: {len(turnos)}
   - Especialidad: {len(especialidades)}
   - Nivel TENS: {len(niveles)}
   - Certificaciones: {len(certificaciones)}

✅ Total: {3 + len(nacionalidades) + len(pueblos) + len(turnos) + len(especialidades) + len(niveles) + len(certificaciones)} registros
        """)
