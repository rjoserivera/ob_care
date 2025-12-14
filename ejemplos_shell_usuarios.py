"""
EJEMPLOS DE USO - Django Shell
Archivo con ejemplos prácticos para gestionar usuarios desde Django shell

Uso:
    python manage.py shell
    >>> exec(open('ejemplos_shell_usuarios.py').read())

O copiar y pegar los bloques de código individualmente
"""

# ══════════════════════════════════════════════════════════════════
# IMPORTACIONES NECESARIAS
# ══════════════════════════════════════════════════════════════════

from django.contrib.auth.models import User, Group
from gestionApp.models import (
    Persona, Medico, Matrona, Tens, Paciente,
    CatalogoSexo, CatalogoNacionalidad, CatalogoPuebloOriginario,
    CatalogoTurno, CatalogoEspecialidad, CatalogoNivelTens
)
from datetime import date

# ══════════════════════════════════════════════════════════════════
# EJEMPLO 1: CREAR GRUPOS DEL SISTEMA
# ══════════════════════════════════════════════════════════════════

def ejemplo_crear_grupos():
    """Crea todos los grupos del sistema"""
    grupos = ['Administrador', 'Medico', 'Matrona', 'TENS', 'Paciente']
    
    for nombre in grupos:
        grupo, created = Group.objects.get_or_create(name=nombre)
        if created:
            print(f'✅ Grupo "{nombre}" creado')
        else:
            print(f'⚠️ Grupo "{nombre}" ya existe')


# ══════════════════════════════════════════════════════════════════
# EJEMPLO 2: CREAR UN ADMINISTRADOR
# ══════════════════════════════════════════════════════════════════

def ejemplo_crear_admin():
    """Crea un usuario administrador"""
    username = 'admin_sistema'
    
    if User.objects.filter(username=username).exists():
        print(f'⚠️ Usuario "{username}" ya existe')
        return
    
    # Crear superusuario
    user = User.objects.create_superuser(
        username=username,
        email='admin@hospital.cl',
        password='pass123',
        first_name='Administrador',
        last_name='Sistema'
    )
    
    # Asignar al grupo Administrador
    grupo_admin, _ = Group.objects.get_or_create(name='Administrador')
    user.groups.add(grupo_admin)
    
    print(f'✅ Administrador "{username}" creado')
    print(f'   Email: {user.email}')
    print(f'   Contraseña: pass123')


# ══════════════════════════════════════════════════════════════════
# EJEMPLO 3: CREAR UN MÉDICO COMPLETO (Usuario + Persona + Médico)
# ══════════════════════════════════════════════════════════════════

def ejemplo_crear_medico_completo():
    """Crea un médico con todos sus datos"""
    username = 'dr_gonzalez'
    
    if User.objects.filter(username=username).exists():
        print(f'⚠️ Usuario "{username}" ya existe')
        return
    
    # 1. Crear usuario Django
    user = User.objects.create_user(
        username=username,
        email='gonzalez@hospital.cl',
        password='pass123',
        first_name='Carlos',
        last_name='González'
    )
    
    # 2. Asignar al grupo Medico
    grupo_medico, _ = Group.objects.get_or_create(name='Medico')
    user.groups.add(grupo_medico)
    
    # 3. Obtener catálogos
    sexo_m = CatalogoSexo.objects.get(codigo='M')
    nac_chile = CatalogoNacionalidad.objects.get(codigo='CL')
    pueblo_no = CatalogoPuebloOriginario.objects.get(codigo='NO')
    turno_dia = CatalogoTurno.objects.get(codigo='DIA')
    esp_go = CatalogoEspecialidad.objects.get(codigo='GO')
    
    # 4. Crear Persona
    persona = Persona.objects.create(
        Rut='15123456-7',
        Nombre='Carlos',
        Apellido_Paterno='González',
        Apellido_Materno='Pérez',
        Fecha_nacimiento=date(1985, 3, 15),
        Sexo=sexo_m,
        Nacionalidad=nac_chile,
        Pueblos_originarios=pueblo_no,
        Telefono='912345678',
        Direccion='Av. Libertador 1234',
        Email='gonzalez@hospital.cl'
    )
    
    # 5. Crear Médico
    medico = Medico.objects.create(
        persona=persona,
        Especialidad=esp_go,
        Registro_medico='RM-15123',
        Años_experiencia=10,
        Turno=turno_dia,
        Activo=True
    )
    
    print(f'✅ Médico "{username}" creado completamente')
    print(f'   RUT: {persona.Rut}')
    print(f'   Especialidad: {medico.Especialidad.nombre}')
    print(f'   Contraseña: pass123')


# ══════════════════════════════════════════════════════════════════
# EJEMPLO 4: CREAR UNA MATRONA COMPLETA
# ══════════════════════════════════════════════════════════════════

def ejemplo_crear_matrona_completa():
    """Crea una matrona con todos sus datos"""
    username = 'matrona_lopez'
    
    if User.objects.filter(username=username).exists():
        print(f'⚠️ Usuario "{username}" ya existe')
        return
    
    # 1. Crear usuario Django
    user = User.objects.create_user(
        username=username,
        email='lopez@hospital.cl',
        password='pass123',
        first_name='María',
        last_name='López'
    )
    
    # 2. Asignar al grupo Matrona
    grupo_matrona, _ = Group.objects.get_or_create(name='Matrona')
    user.groups.add(grupo_matrona)
    
    # 3. Obtener catálogos
    sexo_f = CatalogoSexo.objects.get(codigo='F')
    nac_chile = CatalogoNacionalidad.objects.get(codigo='CL')
    pueblo_no = CatalogoPuebloOriginario.objects.get(codigo='NO')
    turno_dia = CatalogoTurno.objects.get(codigo='DIA')
    esp_go = CatalogoEspecialidad.objects.get(codigo='GO')
    
    # 4. Crear Persona
    persona = Persona.objects.create(
        Rut='16234567-8',
        Nombre='María',
        Apellido_Paterno='López',
        Apellido_Materno='Silva',
        Fecha_nacimiento=date(1988, 7, 20),
        Sexo=sexo_f,
        Nacionalidad=nac_chile,
        Pueblos_originarios=pueblo_no,
        Telefono='923456789',
        Direccion='Calle Los Aromos 567',
        Email='lopez@hospital.cl'
    )
    
    # 5. Crear Matrona
    matrona = Matrona.objects.create(
        persona=persona,
        Especialidad=esp_go,
        Registro_medico='MAT-16234',
        Años_experiencia=7,
        Turno=turno_dia,
        Activo=True
    )
    
    print(f'✅ Matrona "{username}" creada completamente')
    print(f'   RUT: {persona.Rut}')
    print(f'   Años experiencia: {matrona.Años_experiencia}')
    print(f'   Contraseña: pass123')


# ══════════════════════════════════════════════════════════════════
# EJEMPLO 5: CREAR UN TENS
# ══════════════════════════════════════════════════════════════════

def ejemplo_crear_tens():
    """Crea un TENS con todos sus datos"""
    username = 'tens_martinez'
    
    if User.objects.filter(username=username).exists():
        print(f'⚠️ Usuario "{username}" ya existe')
        return
    
    # 1. Crear usuario Django
    user = User.objects.create_user(
        username=username,
        email='martinez@hospital.cl',
        password='pass123',
        first_name='Juan',
        last_name='Martínez'
    )
    
    # 2. Asignar al grupo TENS
    grupo_tens, _ = Group.objects.get_or_create(name='TENS')
    user.groups.add(grupo_tens)
    
    # 3. Obtener catálogos
    sexo_m = CatalogoSexo.objects.get(codigo='M')
    nac_chile = CatalogoNacionalidad.objects.get(codigo='CL')
    pueblo_no = CatalogoPuebloOriginario.objects.get(codigo='NO')
    turno_noc = CatalogoTurno.objects.get(codigo='NOC')
    nivel_n2 = CatalogoNivelTens.objects.get(codigo='N2')
    
    # 4. Crear Persona
    persona = Persona.objects.create(
        Rut='17345678-9',
        Nombre='Juan',
        Apellido_Paterno='Martínez',
        Apellido_Materno='Rojas',
        Fecha_nacimiento=date(1992, 11, 5),
        Sexo=sexo_m,
        Nacionalidad=nac_chile,
        Pueblos_originarios=pueblo_no,
        Telefono='934567890',
        Direccion='Pasaje El Bosque 890',
        Email='martinez@hospital.cl'
    )
    
    # 5. Crear TENS
    tens = Tens.objects.create(
        persona=persona,
        Nivel=nivel_n2,
        Años_experiencia=4,
        Turno=turno_noc,
        Activo=True
    )
    
    print(f'✅ TENS "{username}" creado completamente')
    print(f'   RUT: {persona.Rut}')
    print(f'   Nivel: {tens.Nivel.nombre}')
    print(f'   Contraseña: pass123')


# ══════════════════════════════════════════════════════════════════
# EJEMPLO 6: LISTAR USUARIOS POR ROL
# ══════════════════════════════════════════════════════════════════

def listar_por_rol(rol_nombre):
    """Lista usuarios de un rol específico"""
    print(f'\n{"="*70}')
    print(f'  USUARIOS CON ROL: {rol_nombre}')
    print(f'{"="*70}')
    
    usuarios = User.objects.filter(groups__name=rol_nombre)
    
    if not usuarios.exists():
        print('⚠️ No hay usuarios con este rol')
        return
    
    print(f'{"Username":<20} {"Nombre":<30} {"Email":<30}')
    print(f'{"-"*70}')
    
    for user in usuarios:
        full_name = f"{user.first_name} {user.last_name}"
        estado = "✅" if user.is_active else "❌"
        print(f'{user.username:<20} {full_name:<30} {user.email:<30} {estado}')
    
    print(f'{"="*70}')
    print(f'Total: {usuarios.count()} usuario(s)\n')


def listar_todos_los_usuarios():
    """Lista todos los usuarios del sistema"""
    print(f'\n{"="*80}')
    print(f'  TODOS LOS USUARIOS DEL SISTEMA')
    print(f'{"="*80}')
    
    usuarios = User.objects.all().order_by('username')
    
    print(f'{"Username":<20} {"Nombre":<25} {"Roles":<25} {"Estado":<10}')
    print(f'{"-"*80}')
    
    for user in usuarios:
        full_name = f"{user.first_name} {user.last_name}"
        roles = ", ".join(user.groups.values_list('name', flat=True))
        estado = "✅ Activo" if user.is_active else "❌ Inactivo"
        print(f'{user.username:<20} {full_name:<25} {roles:<25} {estado:<10}')
    
    print(f'{"="*80}')
    print(f'Total: {usuarios.count()} usuario(s)\n')


# ══════════════════════════════════════════════════════════════════
# EJEMPLO 7: ASIGNAR/REMOVER ROLES
# ══════════════════════════════════════════════════════════════════

def asignar_rol_a_usuario(username, rol_nombre):
    """Asigna un rol a un usuario existente"""
    try:
        user = User.objects.get(username=username)
        grupo, _ = Group.objects.get_or_create(name=rol_nombre)
        user.groups.add(grupo)
        print(f'✅ Rol "{rol_nombre}" asignado a "{username}"')
        
        # Mostrar roles actuales
        roles = list(user.groups.values_list('name', flat=True))
        print(f'   Roles actuales: {", ".join(roles)}')
        
    except User.DoesNotExist:
        print(f'❌ Usuario "{username}" no encontrado')


def remover_rol_de_usuario(username, rol_nombre):
    """Remueve un rol de un usuario"""
    try:
        user = User.objects.get(username=username)
        grupo = Group.objects.get(name=rol_nombre)
        user.groups.remove(grupo)
        print(f'✅ Rol "{rol_nombre}" removido de "{username}"')
        
        # Mostrar roles actuales
        roles = list(user.groups.values_list('name', flat=True))
        print(f'   Roles actuales: {", ".join(roles) if roles else "Ninguno"}')
        
    except User.DoesNotExist:
        print(f'❌ Usuario "{username}" no encontrado')
    except Group.DoesNotExist:
        print(f'❌ Rol "{rol_nombre}" no existe')


# ══════════════════════════════════════════════════════════════════
# EJEMPLO 8: CAMBIAR CONTRASEÑA
# ══════════════════════════════════════════════════════════════════

def cambiar_password(username, nueva_password):
    """Cambia la contraseña de un usuario"""
    try:
        user = User.objects.get(username=username)
        user.set_password(nueva_password)
        user.save()
        print(f'✅ Contraseña actualizada para "{username}"')
    except User.DoesNotExist:
        print(f'❌ Usuario "{username}" no encontrado')


# ══════════════════════════════════════════════════════════════════
# EJEMPLO 9: ACTIVAR/DESACTIVAR USUARIOS
# ══════════════════════════════════════════════════════════════════

def desactivar_usuario(username):
    """Desactiva un usuario (no puede iniciar sesión)"""
    try:
        user = User.objects.get(username=username)
        user.is_active = False
        user.save()
        print(f'⚠️ Usuario "{username}" desactivado')
    except User.DoesNotExist:
        print(f'❌ Usuario "{username}" no encontrado')


def activar_usuario(username):
    """Activa un usuario"""
    try:
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
        print(f'✅ Usuario "{username}" activado')
    except User.DoesNotExist:
        print(f'❌ Usuario "{username}" no encontrado')


# ══════════════════════════════════════════════════════════════════
# EJEMPLO 10: ESTADÍSTICAS DEL SISTEMA
# ══════════════════════════════════════════════════════════════════

def mostrar_estadisticas():
    """Muestra estadísticas generales del sistema"""
    print(f'\n{"="*60}')
    print(f'  📊 ESTADÍSTICAS DEL SISTEMA')
    print(f'{"="*60}')
    
    total_usuarios = User.objects.count()
    usuarios_activos = User.objects.filter(is_active=True).count()
    
    print(f'\n👥 Usuarios totales: {total_usuarios}')
    print(f'✅ Usuarios activos: {usuarios_activos}')
    print(f'❌ Usuarios inactivos: {total_usuarios - usuarios_activos}')
    
    print(f'\n🎭 Por Rol:')
    for grupo in Group.objects.all():
        count = User.objects.filter(groups=grupo, is_active=True).count()
        print(f'   {grupo.name}: {count}')
    
    print(f'\n📋 Perfiles completos:')
    print(f'   Médicos: {Medico.objects.filter(Activo=True).count()}')
    print(f'   Matronas: {Matrona.objects.filter(Activo=True).count()}')
    print(f'   TENS: {Tens.objects.filter(Activo=True).count()}')
    print(f'   Pacientes: {Paciente.objects.filter(activo=True).count()}')
    
    print(f'{"="*60}\n')


# ══════════════════════════════════════════════════════════════════
# MENÚ PRINCIPAL
# ══════════════════════════════════════════════════════════════════

def menu_ejemplos():
    """Muestra el menú de ejemplos disponibles"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║              EJEMPLOS DE USO - Django Shell                    ║
╚════════════════════════════════════════════════════════════════╝

📋 FUNCIONES DISPONIBLES:

1️⃣ CREACIÓN:
   ejemplo_crear_grupos()
   ejemplo_crear_admin()
   ejemplo_crear_medico_completo()
   ejemplo_crear_matrona_completa()
   ejemplo_crear_tens()

2️⃣ LISTADO:
   listar_todos_los_usuarios()
   listar_por_rol('Medico')
   listar_por_rol('Matrona')
   listar_por_rol('TENS')
   listar_por_rol('Administrador')

3️⃣ GESTIÓN DE ROLES:
   asignar_rol_a_usuario('username', 'Medico')
   remover_rol_de_usuario('username', 'Medico')

4️⃣ SEGURIDAD:
   cambiar_password('username', 'nueva_pass')
   activar_usuario('username')
   desactivar_usuario('username')

5️⃣ ESTADÍSTICAS:
   mostrar_estadisticas()

════════════════════════════════════════════════════════════════

💡 EJEMPLOS DE USO:

# Crear todos los grupos
>>> ejemplo_crear_grupos()

# Crear un administrador
>>> ejemplo_crear_admin()

# Ver estadísticas
>>> mostrar_estadisticas()

# Listar todos los médicos
>>> listar_por_rol('Medico')

# Cambiar contraseña
>>> cambiar_password('dr_gonzalez', 'nueva_pass123')

════════════════════════════════════════════════════════════════
    """)


# ══════════════════════════════════════════════════════════════════
# AUTO-EJECUCIÓN
# ══════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    menu_ejemplos()


# Al cargar el archivo, mostrar el menú
menu_ejemplos()
