"""
Comando simple para crear usuarios básicos
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    help = 'Crea usuarios básicos del sistema (admin, medico, matrona, tens)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('   CREANDO USUARIOS BÁSICOS DEL SISTEMA'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))

        # 1. Crear grupos
        self.stdout.write('📁 Creando grupos...')
        grupos_nombres = ['Administrador', 'Medico', 'Matrona', 'TENS', 'Paciente']
        for nombre in grupos_nombres:
            grupo, created = Group.objects.get_or_create(name=nombre)
            if created:
                self.stdout.write(self.style.SUCCESS(f"  ✅ Grupo '{nombre}' creado"))
            else:
                self.stdout.write(self.style.WARNING(f"  ⚠️  Grupo '{nombre}' ya existe"))

        # 2. Crear Admin
        self.stdout.write('\n👑 Creando Administrador...')
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@hospital.cl',
                password='pass123',
                first_name='Administrador',
                last_name='Sistema'
            )
            grupo_admin = Group.objects.get(name='Administrador')
            admin.groups.add(grupo_admin)
            self.stdout.write(self.style.SUCCESS("  ✅ Usuario: admin / pass123 (Administrador)"))
        else:
            self.stdout.write(self.style.WARNING("  ⚠️  Usuario 'admin' ya existe"))

        # 3. Crear Médico
        self.stdout.write('\n🩺 Creando Médico...')
        if not User.objects.filter(username='medico').exists():
            medico = User.objects.create_user(
                username='medico',
                email='medico@hospital.cl',
                password='pass123',
                first_name='Carlos',
                last_name='González'
            )
            grupo_medico = Group.objects.get(name='Medico')
            medico.groups.add(grupo_medico)
            self.stdout.write(self.style.SUCCESS("  ✅ Usuario: medico / pass123 (Médico)"))
        else:
            self.stdout.write(self.style.WARNING("  ⚠️  Usuario 'medico' ya existe"))

        # 4. Crear Matrona
        self.stdout.write('\n👩‍⚕️ Creando Matrona...')
        if not User.objects.filter(username='matrona').exists():
            matrona = User.objects.create_user(
                username='matrona',
                email='matrona@hospital.cl',
                password='pass123',
                first_name='María',
                last_name='López'
            )
            grupo_matrona = Group.objects.get(name='Matrona')
            matrona.groups.add(grupo_matrona)
            self.stdout.write(self.style.SUCCESS("  ✅ Usuario: matrona / pass123 (Matrona)"))
        else:
            self.stdout.write(self.style.WARNING("  ⚠️  Usuario 'matrona' ya existe"))

        # 5. Crear TENS
        self.stdout.write('\n🏥 Creando TENS...')
        if not User.objects.filter(username='tens').exists():
            tens = User.objects.create_user(
                username='tens',
                email='tens@hospital.cl',
                password='pass123',
                first_name='Juan',
                last_name='Martínez'
            )
            grupo_tens = Group.objects.get(name='TENS')
            tens.groups.add(grupo_tens)
            self.stdout.write(self.style.SUCCESS("  ✅ Usuario: tens / pass123 (TENS)"))
        else:
            self.stdout.write(self.style.WARNING("  ⚠️  Usuario 'tens' ya existe"))

        # Resumen
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('✅ PROCESO COMPLETADO'))
        self.stdout.write('='*60)
        self.stdout.write('\n📋 CREDENCIALES DE ACCESO:')
        self.stdout.write('   ┌─────────────┬─────────────┬─────────────────┐')
        self.stdout.write('   │ Usuario     │ Contraseña  │ Rol             │')
        self.stdout.write('   ├─────────────┼─────────────┼─────────────────┤')
        self.stdout.write('   │ admin       │ pass123     │ Administrador   │')
        self.stdout.write('   │ medico      │ pass123     │ Médico          │')
        self.stdout.write('   │ matrona     │ pass123     │ Matrona         │')
        self.stdout.write('   │ tens        │ pass123     │ TENS            │')
        self.stdout.write('   └─────────────┴─────────────┴─────────────────┘')
        self.stdout.write('\n🔗 Inicia sesión en: http://localhost:8000/auth/login/\n')
