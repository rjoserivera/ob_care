"""
gestionApp/management/commands/crear_usuarios_iniciales.py
Comando para crear usuarios iniciales del sistema
Uso: python manage.py crear_usuarios_iniciales
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from gestionApp.models import (
    Persona, Medico, Matrona, Tens, Paciente,
    CatalogoSexo, CatalogoNacionalidad, CatalogoPuebloOriginario,
    CatalogoTurno, CatalogoEspecialidad, CatalogoNivelTens, CatalogoCertificacion
)
from datetime import date


class Command(BaseCommand):
    help = 'Crea usuarios iniciales: Admin, Médico, Matrona, TENS y Pacientes de prueba'

    def handle(self, *args, **options):
        self.stdout.write('=' * 50)
        self.stdout.write('Creando usuarios iniciales...')
        self.stdout.write('=' * 50)

        # ============================================
        # 0. CREAR CATÁLOGOS BASE PRIMERO
        # ============================================
        self.stdout.write('\n📚 Creando catálogos base...')
        
        # Sexo
        sexo_m, _ = CatalogoSexo.objects.get_or_create(
            codigo='M', defaults={'nombre': 'Masculino', 'activo': True, 'orden': 1}
        )
        sexo_f, _ = CatalogoSexo.objects.get_or_create(
            codigo='F', defaults={'nombre': 'Femenino', 'activo': True, 'orden': 2}
        )
        CatalogoSexo.objects.get_or_create(
            codigo='I', defaults={'nombre': 'Intersex', 'activo': True, 'orden': 3}
        )
        self.stdout.write(self.style.SUCCESS('   ✅ Catálogo Sexo'))
        
        # Nacionalidad
        nac_chile, _ = CatalogoNacionalidad.objects.get_or_create(
            codigo='CL', defaults={'nombre': 'Chilena', 'activo': True, 'orden': 1}
        )
        CatalogoNacionalidad.objects.get_or_create(
            codigo='VE', defaults={'nombre': 'Venezolana', 'activo': True, 'orden': 2}
        )
        CatalogoNacionalidad.objects.get_or_create(
            codigo='PE', defaults={'nombre': 'Peruana', 'activo': True, 'orden': 3}
        )
        CatalogoNacionalidad.objects.get_or_create(
            codigo='BO', defaults={'nombre': 'Boliviana', 'activo': True, 'orden': 4}
        )
        CatalogoNacionalidad.objects.get_or_create(
            codigo='CO', defaults={'nombre': 'Colombiana', 'activo': True, 'orden': 5}
        )
        CatalogoNacionalidad.objects.get_or_create(
            codigo='HT', defaults={'nombre': 'Haitiana', 'activo': True, 'orden': 6}
        )
        CatalogoNacionalidad.objects.get_or_create(
            codigo='OT', defaults={'nombre': 'Otra', 'activo': True, 'orden': 99}
        )
        self.stdout.write(self.style.SUCCESS('   ✅ Catálogo Nacionalidad'))
        
        # Pueblo Originario
        pueblo_no, _ = CatalogoPuebloOriginario.objects.get_or_create(
            codigo='NO', defaults={'nombre': 'No pertenece', 'activo': True, 'orden': 1}
        )
        CatalogoPuebloOriginario.objects.get_or_create(
            codigo='MAP', defaults={'nombre': 'Mapuche', 'activo': True, 'orden': 2}
        )
        CatalogoPuebloOriginario.objects.get_or_create(
            codigo='AYM', defaults={'nombre': 'Aymara', 'activo': True, 'orden': 3}
        )
        CatalogoPuebloOriginario.objects.get_or_create(
            codigo='RAP', defaults={'nombre': 'Rapa Nui', 'activo': True, 'orden': 4}
        )
        CatalogoPuebloOriginario.objects.get_or_create(
            codigo='DIA', defaults={'nombre': 'Diaguita', 'activo': True, 'orden': 5}
        )
        self.stdout.write(self.style.SUCCESS('   ✅ Catálogo Pueblo Originario'))
        
        # Turnos
        turno_dia, _ = CatalogoTurno.objects.get_or_create(
            codigo='DIA', defaults={'nombre': 'Diurno', 'activo': True, 'orden': 1}
        )
        CatalogoTurno.objects.get_or_create(
            codigo='NOC', defaults={'nombre': 'Nocturno', 'activo': True, 'orden': 2}
        )
        CatalogoTurno.objects.get_or_create(
            codigo='ROT', defaults={'nombre': 'Rotativo', 'activo': True, 'orden': 3}
        )
        self.stdout.write(self.style.SUCCESS('   ✅ Catálogo Turno'))
        
        # Especialidades médicas
        esp_go, _ = CatalogoEspecialidad.objects.get_or_create(
            codigo='GO', defaults={'nombre': 'Ginecología y Obstetricia', 'activo': True, 'orden': 1}
        )
        CatalogoEspecialidad.objects.get_or_create(
            codigo='PED', defaults={'nombre': 'Pediatría', 'activo': True, 'orden': 2}
        )
        CatalogoEspecialidad.objects.get_or_create(
            codigo='ANE', defaults={'nombre': 'Anestesiología', 'activo': True, 'orden': 3}
        )
        CatalogoEspecialidad.objects.get_or_create(
            codigo='MG', defaults={'nombre': 'Medicina General', 'activo': True, 'orden': 4}
        )
        self.stdout.write(self.style.SUCCESS('   ✅ Catálogo Especialidad'))
        
        # Nivel TENS
        nivel_t2, _ = CatalogoNivelTens.objects.get_or_create(
            codigo='N1', defaults={'nombre': 'Nivel 1', 'activo': True, 'orden': 1}
        )
        nivel_t2, _ = CatalogoNivelTens.objects.get_or_create(
            codigo='N2', defaults={'nombre': 'Nivel 2', 'activo': True, 'orden': 2}
        )
        CatalogoNivelTens.objects.get_or_create(
            codigo='N3', defaults={'nombre': 'Nivel 3', 'activo': True, 'orden': 3}
        )
        self.stdout.write(self.style.SUCCESS('   ✅ Catálogo Nivel TENS'))
        
        # Certificaciones
        cert_bls, _ = CatalogoCertificacion.objects.get_or_create(
            codigo='BLS', defaults={'nombre': 'BLS (Soporte Vital Básico)', 'activo': True, 'orden': 1}
        )
        CatalogoCertificacion.objects.get_or_create(
            codigo='ACLS', defaults={'nombre': 'ACLS (Soporte Vital Avanzado)', 'activo': True, 'orden': 2}
        )
        self.stdout.write(self.style.SUCCESS('   ✅ Catálogo Certificaciones'))

        # ============================================
        # 1. CREAR GRUPOS
        # ============================================
        self.stdout.write('\n📁 Creando grupos...')
        
        grupo_admin, _ = Group.objects.get_or_create(name='Administrador')
        grupo_medico, _ = Group.objects.get_or_create(name='Medico')
        grupo_matrona, _ = Group.objects.get_or_create(name='Matrona')
        grupo_tens, _ = Group.objects.get_or_create(name='TENS')
        
        self.stdout.write(self.style.SUCCESS('   ✅ Grupos creados'))

        # ============================================
        # 2. CREAR SUPERUSUARIO ADMIN
        # ============================================
        self.stdout.write('\n👑 Creando Administrador...')
        
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@hospital.cl',
                password='pass123',
                first_name='Administrador',
                last_name='Sistema'
            )
            admin_user.groups.add(grupo_admin)
            self.stdout.write(self.style.SUCCESS('   ✅ Admin creado: admin / pass123'))
        else:
            self.stdout.write(self.style.WARNING('   ⚠️ Admin "admin" ya existe'))

        # ============================================
        # 3. CREAR MÉDICO
        # ============================================
        self.stdout.write('\n🩺 Creando Médico...')
        
        if not User.objects.filter(username='medico').exists():
            user_medico = User.objects.create_user(
                username='medico',
                email='medico@hospital.cl',
                password='pass123',
                first_name='Carlos',
                last_name='González'
            )
            user_medico.groups.add(grupo_medico)
            
            persona_medico = Persona.objects.create(
                Rut='11111111-1',
                Nombre='Carlos',
                Apellido_Paterno='González',
                Apellido_Materno='Pérez',
                Fecha_nacimiento=date(1980, 5, 15),
                Sexo=sexo_m,
                Nacionalidad=nac_chile,
                Pueblos_originarios=pueblo_no,
                Telefono='912345678',
                Direccion='Av. Principal 123',
                Email='medico@hospital.cl'
            )
            
            Medico.objects.create(
                persona=persona_medico,
                Especialidad=esp_go,
                Registro_medico='RM-12345',
                Años_experiencia=10,
                Turno=turno_dia,
                Activo=True
            )
            
            self.stdout.write(self.style.SUCCESS('   ✅ Médico creado: medico / pass123'))
        else:
            self.stdout.write(self.style.WARNING('   ⚠️ Usuario "medico" ya existe'))

        # ============================================
        # 4. CREAR MATRONA
        # ============================================
        self.stdout.write('\n👩‍⚕️ Creando Matrona...')
        
        if not User.objects.filter(username='matrona').exists():
            user_matrona = User.objects.create_user(
                username='matrona',
                email='matrona@hospital.cl',
                password='pass123',
                first_name='María',
                last_name='López'
            )
            user_matrona.groups.add(grupo_matrona)
            
            persona_matrona = Persona.objects.create(
                Rut='22222222-2',
                Nombre='María',
                Apellido_Paterno='López',
                Apellido_Materno='Silva',
                Fecha_nacimiento=date(1985, 8, 20),
                Sexo=sexo_f,
                Nacionalidad=nac_chile,
                Pueblos_originarios=pueblo_no,
                Telefono='923456789',
                Direccion='Calle Secundaria 456',
                Email='matrona@hospital.cl'
            )
            
            Matrona.objects.create(
                persona=persona_matrona,
                Especialidad=esp_go,
                Registro_medico='MAT-54321',
                Años_experiencia=8,
                Turno=turno_dia,
                Activo=True
            )
            
            self.stdout.write(self.style.SUCCESS('   ✅ Matrona creada: matrona / pass123'))
        else:
            self.stdout.write(self.style.WARNING('   ⚠️ Usuario "matrona" ya existe'))

        # ============================================
        # 5. CREAR TENS
        # ============================================
        self.stdout.write('\n🏥 Creando TENS...')
        
        if not User.objects.filter(username='tens').exists():
            user_tens = User.objects.create_user(
                username='tens',
                email='tens@hospital.cl',
                password='pass123',
                first_name='Juan',
                last_name='Martínez'
            )
            user_tens.groups.add(grupo_tens)
            
            persona_tens = Persona.objects.create(
                Rut='33333333-3',
                Nombre='Juan',
                Apellido_Paterno='Martínez',
                Apellido_Materno='Rojas',
                Fecha_nacimiento=date(1990, 3, 10),
                Sexo=sexo_m,
                Nacionalidad=nac_chile,
                Pueblos_originarios=pueblo_no,
                Telefono='934567890',
                Direccion='Pasaje Norte 789',
                Email='tens@hospital.cl'
            )
            
            Tens.objects.create(
                persona=persona_tens,
                Nivel=nivel_t2,
                Años_experiencia=5,
                Turno=turno_dia,
                Certificaciones=cert_bls,
                Activo=True
            )
            
            self.stdout.write(self.style.SUCCESS('   ✅ TENS creado: tens / pass123'))
        else:
            self.stdout.write(self.style.WARNING('   ⚠️ Usuario "tens" ya existe'))

        # ============================================
        # 6. CREAR PACIENTES DE PRUEBA
        # ============================================
        self.stdout.write('\n🤰 Creando Pacientes de prueba...')
        
        pacientes_data = [
            {
                'rut': '44444444-4',
                'nombre': 'Ana',
                'ap_paterno': 'Soto',
                'ap_materno': 'Vera',
                'fecha_nac': date(1995, 6, 25),
                'telefono': '945678901',
                'direccion': 'Villa Los Aromos 321',
                'email': 'ana.soto@email.cl'
            },
            {
                'rut': '55555555-5',
                'nombre': 'Camila',
                'ap_paterno': 'Fernández',
                'ap_materno': 'Muñoz',
                'fecha_nac': date(1992, 11, 8),
                'telefono': '956789012',
                'direccion': 'Población Central 654',
                'email': 'camila.fernandez@email.cl'
            },
            {
                'rut': '66666666-6',
                'nombre': 'Valentina',
                'ap_paterno': 'Díaz',
                'ap_materno': 'Castro',
                'fecha_nac': date(1998, 2, 14),
                'telefono': '967890123',
                'direccion': 'Conjunto Habitacional 987',
                'email': 'valentina.diaz@email.cl'
            },
        ]
        
        for p in pacientes_data:
            if not Persona.objects.filter(Rut=p['rut']).exists():
                persona = Persona.objects.create(
                    Rut=p['rut'],
                    Nombre=p['nombre'],
                    Apellido_Paterno=p['ap_paterno'],
                    Apellido_Materno=p['ap_materno'],
                    Fecha_nacimiento=p['fecha_nac'],
                    Sexo=sexo_f,
                    Nacionalidad=nac_chile,
                    Pueblos_originarios=pueblo_no,
                    Telefono=p['telefono'],
                    Direccion=p['direccion'],
                    Email=p['email']
                )
                
                Paciente.objects.create(
                    persona=persona,
                    activo=True
                )
                
                self.stdout.write(self.style.SUCCESS(f'   ✅ Paciente: {p["nombre"]} {p["ap_paterno"]} ({p["rut"]})'))
            else:
                self.stdout.write(self.style.WARNING(f'   ⚠️ Paciente {p["rut"]} ya existe'))

        # ============================================
        # 7. CREAR CATÁLOGOS DE MATRONAAPP
        # ============================================
        self.stdout.write('\n📚 Creando catálogos de matronaApp...')
        
        try:
            from matronaApp.models import CatalogoConsultorioOrigen, CatalogoViaAdministracion
            
            consultorios = [
                ('CESFAM-01', 'CESFAM Ultraestación'),
                ('CESFAM-02', 'CESFAM Los Volcanes'),
                ('CESFAM-03', 'CESFAM San Ramón'),
                ('HOSP-01', 'Hospital Herminda Martín'),
                ('PART-01', 'Particular'),
            ]
            
            for codigo, nombre in consultorios:
                CatalogoConsultorioOrigen.objects.get_or_create(
                    codigo=codigo,
                    defaults={'nombre': nombre, 'activo': True}
                )
            
            self.stdout.write(self.style.SUCCESS('   ✅ Consultorios de origen creados'))
            
            vias = [
                ('VO', 'Vía Oral'),
                ('IV', 'Intravenosa'),
                ('IM', 'Intramuscular'),
                ('SC', 'Subcutánea'),
                ('TOP', 'Tópica'),
                ('INH', 'Inhalatoria'),
                ('SL', 'Sublingual'),
            ]
            
            for codigo, nombre in vias:
                CatalogoViaAdministracion.objects.get_or_create(
                    codigo=codigo,
                    defaults={'nombre': nombre, 'activo': True}
                )
            
            self.stdout.write(self.style.SUCCESS('   ✅ Vías de administración creadas'))
            
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'   ⚠️ Error en catálogos matronaApp: {e}'))

        # ============================================
        # RESUMEN FINAL
        # ============================================
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('✅ PROCESO COMPLETADO'))
        self.stdout.write('=' * 50)
        self.stdout.write('\n📋 USUARIOS CREADOS:')
        self.stdout.write('   ┌─────────────┬─────────────┬─────────────┐')
        self.stdout.write('   │ Usuario     │ Contraseña  │ Rol         │')
        self.stdout.write('   ├─────────────┼─────────────┼─────────────┤')
        self.stdout.write('   │ admin       │ pass123     │ Admin       │')
        self.stdout.write('   │ medico      │ pass123     │ Médico      │')
        self.stdout.write('   │ matrona     │ pass123     │ Matrona     │')
        self.stdout.write('   │ tens        │ pass123     │ TENS        │')
        self.stdout.write('   └─────────────┴─────────────┴─────────────┘')
        self.stdout.write('\n🤰 PACIENTES DE PRUEBA: 3 creadas')
        self.stdout.write('📚 CATÁLOGOS: Todos los catálogos base creados\n')