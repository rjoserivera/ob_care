"""
gestionApp/management/commands/gestionar_usuarios_roles.py

Script interactivo para gestionar usuarios y roles del sistema.

Uso:
    python manage.py gestionar_usuarios_roles

Características:
    - Crear nuevos usuarios con roles específicos
    - Asignar/remover roles a usuarios existentes
    - Listar usuarios por rol
    - Cambiar contraseñas
    - Activar/desactivar usuarios
    - Crear usuarios masivamente
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from gestionApp.models import (
    Persona, Medico, Matrona, Tens, Paciente,
    CatalogoSexo, CatalogoNacionalidad, CatalogoPuebloOriginario,
    CatalogoTurno, CatalogoEspecialidad, CatalogoNivelTens, CatalogoCertificacion
)
from datetime import date, datetime
import getpass


class Command(BaseCommand):
    help = 'Script interactivo para gestionar usuarios y roles del sistema'

    def add_arguments(self, parser):
        parser.add_argument(
            '--listar',
            type=str,
            choices=['todos', 'administrador', 'medico', 'matrona', 'tens', 'paciente'],
            help='Listar usuarios por rol'
        )
        parser.add_argument(
            '--crear',
            action='store_true',
            help='Crear un nuevo usuario (modo interactivo)'
        )
        parser.add_argument(
            '--rol',
            type=str,
            help='Asignar rol a un usuario existente'
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Nombre de usuario'
        )

    def handle(self, *args, **options):
        # Banner de bienvenida
        self.mostrar_banner()

        # Si se pasan argumentos, ejecutar la acción correspondiente
        if options['listar']:
            self.listar_usuarios(options['listar'])
            return

        if options['rol'] and options['username']:
            self.asignar_rol(options['username'], options['rol'])
            return

        # Modo interactivo
        while True:
            self.mostrar_menu_principal()
            opcion = input("\n👉 Selecciona una opción: ").strip()

            if opcion == '1':
                self.crear_usuario_interactivo()
            elif opcion == '2':
                self.asignar_rol_interactivo()
            elif opcion == '3':
                self.listar_usuarios_menu()
            elif opcion == '4':
                self.cambiar_password_interactivo()
            elif opcion == '5':
                self.activar_desactivar_usuario()
            elif opcion == '6':
                self.eliminar_usuario_interactivo()
            elif opcion == '7':
                self.crear_usuarios_masivos()
            elif opcion == '8':
                self.crear_grupos_sistema()
            elif opcion == '0':
                self.stdout.write(self.style.SUCCESS('\n👋 ¡Hasta luego!\n'))
                break
            else:
                self.stdout.write(self.style.ERROR('\n❌ Opción inválida. Intenta de nuevo.\n'))

    def mostrar_banner(self):
        """Muestra el banner de bienvenida"""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║      🏥  GESTOR DE USUARIOS Y ROLES - OB CARE  🏥       ║
║                                                           ║
║          Sistema de Gestión Hospitalaria                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """
        self.stdout.write(self.style.SUCCESS(banner))

    def mostrar_menu_principal(self):
        """Muestra el menú principal"""
        menu = """
╔═══════════════════════════════════════════════════════════╗
║                    MENÚ PRINCIPAL                         ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  1️⃣  Crear nuevo usuario                                 ║
║  2️⃣  Asignar/Remover rol a usuario existente             ║
║  3️⃣  Listar usuarios                                      ║
║  4️⃣  Cambiar contraseña                                   ║
║  5️⃣  Activar/Desactivar usuario                           ║
║  6️⃣  Eliminar usuario                                     ║
║  7️⃣  Crear usuarios masivos (demo)                        ║
║  8️⃣  Crear grupos del sistema                             ║
║  0️⃣  Salir                                                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """
        self.stdout.write(menu)

    def crear_usuario_interactivo(self):
        """Crea un usuario de forma interactiva"""
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('           CREAR NUEVO USUARIO'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))

        try:
            # Datos básicos del usuario Django
            username = input("👤 Nombre de usuario: ").strip()
            if not username:
                raise ValueError("El nombre de usuario no puede estar vacío")

            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.ERROR(f'\n❌ El usuario "{username}" ya existe.\n'))
                return

            email = input("📧 Email: ").strip()
            first_name = input("👤 Nombre: ").strip()
            last_name = input("👤 Apellido: ").strip()
            password = getpass.getpass("🔒 Contraseña: ")
            password_confirm = getpass.getpass("🔒 Confirmar contraseña: ")

            if password != password_confirm:
                self.stdout.write(self.style.ERROR('\n❌ Las contraseñas no coinciden.\n'))
                return

            # Seleccionar rol
            self.stdout.write('\n📋 Roles disponibles:')
            self.stdout.write('  1. Administrador')
            self.stdout.write('  2. Médico')
            self.stdout.write('  3. Matrona')
            self.stdout.write('  4. TENS')
            self.stdout.write('  5. Paciente')
            
            rol_opcion = input('\n👉 Selecciona el rol (1-5): ').strip()
            roles_map = {
                '1': 'Administrador',
                '2': 'Medico',
                '3': 'Matrona',
                '4': 'TENS',
                '5': 'Paciente'
            }

            if rol_opcion not in roles_map:
                self.stdout.write(self.style.ERROR('\n❌ Opción de rol inválida.\n'))
                return

            rol_nombre = roles_map[rol_opcion]

            # Crear usuario
            if rol_opcion == '1':
                # Administrador como superusuario
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )

            # Asignar grupo
            grupo, _ = Group.objects.get_or_create(name=rol_nombre)
            user.groups.add(grupo)

            self.stdout.write(self.style.SUCCESS(f'\n✅ Usuario "{username}" creado exitosamente con rol "{rol_nombre}"!'))
            
            # Preguntar si desea crear el perfil completo (Persona + Médico/Matrona/TENS/Paciente)
            if rol_opcion in ['2', '3', '4', '5']:
                crear_perfil = input('\n¿Deseas crear el perfil completo para este usuario? (s/n): ').strip().lower()
                if crear_perfil == 's':
                    self.crear_perfil_completo(user, rol_nombre)

        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Error: {e}\n'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Error inesperado: {e}\n'))

    def crear_perfil_completo(self, user, rol):
        """Crea el perfil completo (Persona + Médico/Matrona/TENS/Paciente)"""
        self.stdout.write(self.style.WARNING('\n📝 Creando perfil completo...\n'))

        try:
            # Datos de la persona
            rut = input("🆔 RUT (ej: 12345678-9): ").strip()
            nombre = input("👤 Nombre: ").strip() or user.first_name
            ap_paterno = input("👤 Apellido Paterno: ").strip()
            ap_materno = input("👤 Apellido Materno: ").strip()
            
            # Fecha de nacimiento
            fecha_nac_str = input("📅 Fecha de nacimiento (DD/MM/AAAA): ").strip()
            try:
                fecha_nac = datetime.strptime(fecha_nac_str, '%d/%m/%Y').date()
            except:
                fecha_nac = date(1990, 1, 1)
                self.stdout.write(self.style.WARNING(f'⚠️ Fecha inválida, usando: {fecha_nac}'))

            # Sexo
            self.stdout.write('\n⚥ Sexo:')
            self.stdout.write('  1. Masculino')
            self.stdout.write('  2. Femenino')
            sexo_opcion = input('👉 Selecciona (1-2): ').strip()
            sexo = CatalogoSexo.objects.filter(codigo='M' if sexo_opcion == '1' else 'F').first()
            if not sexo:
                sexo = CatalogoSexo.objects.first()

            # Nacionalidad
            nacionalidad = CatalogoNacionalidad.objects.filter(codigo='CL').first()
            if not nacionalidad:
                nacionalidad = CatalogoNacionalidad.objects.first()

            # Pueblo originario
            pueblo = CatalogoPuebloOriginario.objects.filter(codigo='NO').first()
            if not pueblo:
                pueblo = CatalogoPuebloOriginario.objects.first()

            telefono = input("📱 Teléfono: ").strip()
            direccion = input("🏠 Dirección: ").strip()

            # Crear Persona
            persona = Persona.objects.create(
                Rut=rut,
                Nombre=nombre,
                Apellido_Paterno=ap_paterno,
                Apellido_Materno=ap_materno,
                Fecha_nacimiento=fecha_nac,
                Sexo=sexo,
                Nacionalidad=nacionalidad,
                Pueblos_originarios=pueblo,
                Telefono=telefono,
                Direccion=direccion,
                Email=user.email
            )

            self.stdout.write(self.style.SUCCESS(f'✅ Persona creada con RUT: {rut}'))

            # Crear según el rol
            if rol == 'Medico':
                self._crear_medico(persona)
            elif rol == 'Matrona':
                self._crear_matrona(persona)
            elif rol == 'TENS':
                self._crear_tens(persona)
            elif rol == 'Paciente':
                self._crear_paciente(persona)

        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Error de integridad: {e}\n'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Error al crear perfil: {e}\n'))

    def _crear_medico(self, persona):
        """Crea un registro de Médico"""
        especialidad = CatalogoEspecialidad.objects.first()
        turno = CatalogoTurno.objects.first()
        
        registro = input("📋 Registro médico: ").strip() or f"RM-{persona.Rut[:8]}"
        experiencia = input("📅 Años de experiencia: ").strip() or '5'

        Medico.objects.create(
            persona=persona,
            Especialidad=especialidad,
            Registro_medico=registro,
            Años_experiencia=int(experiencia),
            Turno=turno,
            Activo=True
        )
        self.stdout.write(self.style.SUCCESS('✅ Perfil de Médico creado'))

    def _crear_matrona(self, persona):
        """Crea un registro de Matrona"""
        especialidad = CatalogoEspecialidad.objects.first()
        turno = CatalogoTurno.objects.first()
        
        registro = input("📋 Registro médico: ").strip() or f"MAT-{persona.Rut[:8]}"
        experiencia = input("📅 Años de experiencia: ").strip() or '5'

        Matrona.objects.create(
            persona=persona,
            Especialidad=especialidad,
            Registro_medico=registro,
            Años_experiencia=int(experiencia),
            Turno=turno,
            Activo=True
        )
        self.stdout.write(self.style.SUCCESS('✅ Perfil de Matrona creado'))

    def _crear_tens(self, persona):
        """Crea un registro de TENS"""
        nivel = CatalogoNivelTens.objects.first()
        turno = CatalogoTurno.objects.first()
        certificacion = CatalogoCertificacion.objects.first()
        
        experiencia = input("📅 Años de experiencia: ").strip() or '3'

        Tens.objects.create(
            persona=persona,
            Nivel=nivel,
            Años_experiencia=int(experiencia),
            Turno=turno,
            Certificaciones=certificacion,
            Activo=True
        )
        self.stdout.write(self.style.SUCCESS('✅ Perfil de TENS creado'))

    def _crear_paciente(self, persona):
        """Crea un registro de Paciente"""
        Paciente.objects.create(
            persona=persona,
            activo=True
        )
        self.stdout.write(self.style.SUCCESS('✅ Perfil de Paciente creado'))

    def asignar_rol_interactivo(self):
        """Asigna o remueve roles de forma interactiva"""
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('        ASIGNAR/REMOVER ROL'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))

        username = input("👤 Nombre de usuario: ").strip()
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'\n❌ Usuario "{username}" no encontrado.\n'))
            return

        # Mostrar roles actuales
        roles_actuales = user.groups.values_list('name', flat=True)
        self.stdout.write(f'\n📋 Roles actuales: {", ".join(roles_actuales) if roles_actuales else "Ninguno"}')

        # Menú de opciones
        self.stdout.write('\n¿Qué deseas hacer?')
        self.stdout.write('  1. Asignar nuevo rol')
        self.stdout.write('  2. Remover rol existente')
        
        accion = input('\n👉 Selecciona (1-2): ').strip()

        if accion == '1':
            self.stdout.write('\n📋 Roles disponibles:')
            self.stdout.write('  1. Administrador')
            self.stdout.write('  2. Médico')
            self.stdout.write('  3. Matrona')
            self.stdout.write('  4. TENS')
            self.stdout.write('  5. Paciente')
            
            rol_opcion = input('\n👉 Selecciona el rol a asignar (1-5): ').strip()
            roles_map = {
                '1': 'Administrador',
                '2': 'Medico',
                '3': 'Matrona',
                '4': 'TENS',
                '5': 'Paciente'
            }

            if rol_opcion not in roles_map:
                self.stdout.write(self.style.ERROR('\n❌ Opción inválida.\n'))
                return

            rol_nombre = roles_map[rol_opcion]
            grupo, _ = Group.objects.get_or_create(name=rol_nombre)
            user.groups.add(grupo)
            
            self.stdout.write(self.style.SUCCESS(f'\n✅ Rol "{rol_nombre}" asignado a "{username}"!\n'))

        elif accion == '2':
            if not roles_actuales:
                self.stdout.write(self.style.WARNING('\n⚠️ Este usuario no tiene roles asignados.\n'))
                return

            self.stdout.write('\n📋 Roles actuales:')
            for idx, rol in enumerate(roles_actuales, 1):
                self.stdout.write(f'  {idx}. {rol}')

            rol_idx = input('\n👉 Selecciona el rol a remover: ').strip()
            try:
                rol_idx = int(rol_idx) - 1
                rol_nombre = roles_actuales[rol_idx]
                grupo = Group.objects.get(name=rol_nombre)
                user.groups.remove(grupo)
                self.stdout.write(self.style.SUCCESS(f'\n✅ Rol "{rol_nombre}" removido de "{username}"!\n'))
            except (ValueError, IndexError, Group.DoesNotExist):
                self.stdout.write(self.style.ERROR('\n❌ Opción inválida.\n'))

    def listar_usuarios_menu(self):
        """Menú para listar usuarios"""
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('           LISTAR USUARIOS'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))

        self.stdout.write('📋 Filtrar por:')
        self.stdout.write('  1. Todos los usuarios')
        self.stdout.write('  2. Administradores')
        self.stdout.write('  3. Médicos')
        self.stdout.write('  4. Matronas')
        self.stdout.write('  5. TENS')
        self.stdout.write('  6. Pacientes')
        self.stdout.write('  7. Usuarios sin rol')
        
        opcion = input('\n👉 Selecciona (1-7): ').strip()
        
        opciones_map = {
            '1': 'todos',
            '2': 'administrador',
            '3': 'medico',
            '4': 'matrona',
            '5': 'tens',
            '6': 'paciente',
            '7': 'sin_rol'
        }

        if opcion in opciones_map:
            self.listar_usuarios(opciones_map[opcion])
        else:
            self.stdout.write(self.style.ERROR('\n❌ Opción inválida.\n'))

    def listar_usuarios(self, filtro='todos'):
        """Lista usuarios según el filtro"""
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        
        if filtro == 'todos':
            usuarios = User.objects.all().order_by('username')
            self.stdout.write(self.style.SUCCESS(f'        TODOS LOS USUARIOS ({usuarios.count()})'))
        elif filtro == 'sin_rol':
            usuarios = User.objects.filter(groups__isnull=True).order_by('username')
            self.stdout.write(self.style.SUCCESS(f'      USUARIOS SIN ROL ({usuarios.count()})'))
        else:
            rol_map = {
                'administrador': 'Administrador',
                'medico': 'Medico',
                'matrona': 'Matrona',
                'tens': 'TENS',
                'paciente': 'Paciente'
            }
            rol_nombre = rol_map.get(filtro, filtro)
            usuarios = User.objects.filter(groups__name=rol_nombre).order_by('username')
            self.stdout.write(self.style.SUCCESS(f'        {rol_nombre.upper()}S ({usuarios.count()})'))
        
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))

        if not usuarios.exists():
            self.stdout.write(self.style.WARNING('⚠️ No se encontraron usuarios.\n'))
            return

        # Encabezado de tabla
        self.stdout.write('┌─────────────────────┬───────────────────────────┬──────────────────────────┬────────────┐')
        self.stdout.write('│ Username            │ Nombre Completo           │ Roles                    │ Estado     │')
        self.stdout.write('├─────────────────────┼───────────────────────────┼──────────────────────────┼────────────┤')

        for user in usuarios:
            username = user.username[:19].ljust(19)
            full_name = f"{user.first_name} {user.last_name}"[:25].ljust(25)
            roles = ", ".join(user.groups.values_list('name', flat=True))[:24].ljust(24)
            estado = "✅ Activo" if user.is_active else "❌ Inactivo"
            
            self.stdout.write(f'│ {username} │ {full_name} │ {roles} │ {estado}  │')

        self.stdout.write('└─────────────────────┴───────────────────────────┴──────────────────────────┴────────────┘\n')

    def cambiar_password_interactivo(self):
        """Cambia la contraseña de un usuario"""
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('         CAMBIAR CONTRASEÑA'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))

        username = input("👤 Nombre de usuario: ").strip()
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'\n❌ Usuario "{username}" no encontrado.\n'))
            return

        password = getpass.getpass("🔒 Nueva contraseña: ")
        password_confirm = getpass.getpass("🔒 Confirmar contraseña: ")

        if password != password_confirm:
            self.stdout.write(self.style.ERROR('\n❌ Las contraseñas no coinciden.\n'))
            return

        user.set_password(password)
        user.save()
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Contraseña actualizada para "{username}"!\n'))

    def activar_desactivar_usuario(self):
        """Activa o desactiva un usuario"""
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('      ACTIVAR/DESACTIVAR USUARIO'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))

        username = input("👤 Nombre de usuario: ").strip()
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'\n❌ Usuario "{username}" no encontrado.\n'))
            return

        estado_actual = "Activo" if user.is_active else "Inactivo"
        self.stdout.write(f'\n📊 Estado actual: {estado_actual}')

        if user.is_active:
            confirmar = input('\n¿Deseas DESACTIVAR este usuario? (s/n): ').strip().lower()
            if confirmar == 's':
                user.is_active = False
                user.save()
                self.stdout.write(self.style.WARNING(f'\n⚠️ Usuario "{username}" desactivado.\n'))
        else:
            confirmar = input('\n¿Deseas ACTIVAR este usuario? (s/n): ').strip().lower()
            if confirmar == 's':
                user.is_active = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f'\n✅ Usuario "{username}" activado.\n'))

    def eliminar_usuario_interactivo(self):
        """Elimina un usuario del sistema"""
        self.stdout.write(self.style.ERROR('\n' + '='*60))
        self.stdout.write(self.style.ERROR('           ELIMINAR USUARIO'))
        self.stdout.write(self.style.ERROR('='*60 + '\n'))
        self.stdout.write(self.style.WARNING('⚠️  ADVERTENCIA: Esta acción es IRREVERSIBLE ⚠️\n'))

        username = input("👤 Nombre de usuario a eliminar: ").strip()
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'\n❌ Usuario "{username}" no encontrado.\n'))
            return

        # Mostrar información del usuario
        roles = ", ".join(user.groups.values_list('name', flat=True))
        self.stdout.write(f'\n📋 Usuario: {user.username}')
        self.stdout.write(f'📧 Email: {user.email}')
        self.stdout.write(f'👤 Nombre: {user.first_name} {user.last_name}')
        self.stdout.write(f'🎭 Roles: {roles}')

        confirmar = input(f'\n¿Estás SEGURO de eliminar a "{username}"? Escribe "ELIMINAR" para confirmar: ').strip()
        
        if confirmar == 'ELIMINAR':
            user.delete()
            self.stdout.write(self.style.SUCCESS(f'\n✅ Usuario "{username}" eliminado permanentemente.\n'))
        else:
            self.stdout.write(self.style.WARNING('\n⚠️ Eliminación cancelada.\n'))

    def crear_usuarios_masivos(self):
        """Crea usuarios de demostración masivamente"""
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('       CREAR USUARIOS MASIVOS (DEMO)'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))

        confirmar = input('¿Deseas crear 10 usuarios de demostración? (s/n): ').strip().lower()
        if confirmar != 's':
            self.stdout.write(self.style.WARNING('\n⚠️ Operación cancelada.\n'))
            return

        # Crear grupos si no existen
        self.crear_grupos_sistema(silencioso=True)

        usuarios_demo = [
            ('medico1', 'Dr. Juan', 'Pérez', 'Medico'),
            ('medico2', 'Dra. María', 'González', 'Medico'),
            ('matrona1', 'Ana', 'López', 'Matrona'),
            ('matrona2', 'Carmen', 'Rodríguez', 'Matrona'),
            ('tens1', 'Pedro', 'Martínez', 'TENS'),
            ('tens2', 'Luis', 'Sánchez', 'TENS'),
            ('admin1', 'Admin', 'Sistema', 'Administrador'),
            ('paciente1', 'Sofía', 'Ramírez', 'Paciente'),
            ('paciente2', 'Valentina', 'Torres', 'Paciente'),
            ('paciente3', 'Isabella', 'Flores', 'Paciente'),
        ]

        creados = 0
        for username, first_name, last_name, rol in usuarios_demo:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@hospital.cl',
                    password='pass123',
                    first_name=first_name,
                    last_name=last_name
                )
                grupo, _ = Group.objects.get_or_create(name=rol)
                user.groups.add(grupo)
                creados += 1
                self.stdout.write(self.style.SUCCESS(f'   ✅ {username} ({rol})'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ {creados} usuarios de demostración creados.'))
        self.stdout.write(self.style.WARNING('🔒 Contraseña para todos: pass123\n'))

    def crear_grupos_sistema(self, silencioso=False):
        """Crea los grupos del sistema"""
        if not silencioso:
            self.stdout.write(self.style.SUCCESS('\n' + '='*60))
            self.stdout.write(self.style.SUCCESS('        CREAR GRUPOS DEL SISTEMA'))
            self.stdout.write(self.style.SUCCESS('='*60 + '\n'))

        grupos = ['Administrador', 'Medico', 'Matrona', 'TENS', 'Paciente']
        
        for nombre in grupos:
            grupo, created = Group.objects.get_or_create(name=nombre)
            if created:
                if not silencioso:
                    self.stdout.write(self.style.SUCCESS(f'✅ Grupo "{nombre}" creado'))
            else:
                if not silencioso:
                    self.stdout.write(self.style.WARNING(f'⚠️ Grupo "{nombre}" ya existe'))
        
        if not silencioso:
            self.stdout.write(self.style.SUCCESS('\n✅ Todos los grupos verificados.\n'))

    def asignar_rol(self, username, rol):
        """Asigna un rol a un usuario (modo comando)"""
        try:
            user = User.objects.get(username=username)
            grupo, _ = Group.objects.get_or_create(name=rol)
            user.groups.add(grupo)
            self.stdout.write(self.style.SUCCESS(f'✅ Rol "{rol}" asignado a "{username}"'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ Usuario "{username}" no encontrado'))
