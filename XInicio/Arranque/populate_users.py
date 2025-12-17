import os
import sys
import django
import random
from datetime import date

# Agregar el directorio raíz al path para importar settings
# Agregar el directorio raíz al path para importar settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')

django.setup()

from django.contrib.auth.models import User, Group
from gestionApp.models import Persona, PerfilUsuario, CatalogoSexo, CatalogoNacionalidad, CatalogoPuebloOriginario
from django.utils import timezone

# ==========================================
# CONFIGURACIÓN
# ==========================================

PASSWORD_BOCCHI = "216"
PASSWORD_DEFAULT = "1234"  # Contraseña para los usuarios generados
EMAIL_BOCCHI = "rjoserivera@gmail.com"

# Grupos esperados en PerfilUsuario (Asegurar que existan)
ROLES = {
    'ADMIN': 'Administradores',
    'MEDICO': 'Medicos',
    'MATRONA': 'Matronas',
    'TENS': 'TENS'
}

# Crear grupos si no existen (versión Plural para compatibilidad con PerfilUsuario)
for key, role_name in ROLES.items():
    Group.objects.get_or_create(name=role_name)

# ==========================================
# GENERADORES DE DATOS
# ==========================================

NOMBRES_HOMBRES = [
    "Juan", "Pedro", "Diego", "Jose", "Luis", "Carlos", "Jorge", "Manuel", "Victor", "Francisco",
    "Antonio", "Miguel", "David", "Daniel", "Javier", "Ricardo", "Fernando", "Roberto", "Pablo", "Alejandro"
]
NOMBRES_MUJERES = [
    "Maria", "Ana", "Isabel", "Laura", "Carolina", "Andrea", "Camila", "Daniela", "Valentina", "Sofia",
    "Fernanda", "Gabriela", "Patricia", "Carmen", "Rosa", "Claudia", "Paula", "Loreto", "Veronica", "Teresa"
]
APELLIDOS = [
    "Gonzalez", "Muñoz", "Rojas", "Diaz", "Perez", "Soto", "Contreras", "Silva", "Martinez", "Sepulveda",
    "Morales", "Rodriguez", "Lopez", "Fuentes", "Hernandez", "Torres", "Araya", "Flores", "Espinoza", "Valenzuela",
    "Castillo", "Tapia", "Reyes", "Gutierrez", "Castro", "Pizarro", "Alvarez", "Vasquez", "Sanchez", "Fernandez"
]

def generar_rut():
    """Genera un RUT válido"""
    numero = random.randint(10000000, 25000000)
    cuerpo = str(numero)
    
    # Calcular DV
    suma = 0
    multiplo = 2
    for d in reversed(cuerpo):
        suma += int(d) * multiplo
        multiplo += 1
        if multiplo > 7: multiplo = 2
    
    resto = suma % 11
    dv_calc = 11 - resto
    if dv_calc == 11: dv = '0'
    elif dv_calc == 10: dv = 'K'
    else: dv = str(dv_calc)
    
    return f"{cuerpo}-{dv}"

def obtener_sexo_random():
    sexos = CatalogoSexo.objects.filter(activo=True)
    if sexos.exists():
        return random.choice(sexos)
    return None

def create_user_complete(username, password, email, nombre, apellido_p, apellido_m, role_name, cargo_titulo):
    """Crea Usuario, Persona, PerfilUsuario y asigna Grupo"""
    
    # 1. Crear Usuario Django
    if User.objects.filter(username=username).exists():
        print(f"⚠️ Usuario {username} ya existe. Saltando...")
        user = User.objects.get(username=username)
    else:
        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = nombre
        user.last_name = f"{apellido_p} {apellido_m}"
        user.save()
        print(f"✅ Usuario creado: {username}")

    # 2. Asignar Grupo
    group, _ = Group.objects.get_or_create(name=role_name)
    user.groups.add(group)
    
    # Flags de superusuario si es Admin
    if role_name == ROLES['ADMIN']:
        user.is_staff = True
        user.is_superuser = True
        user.save()

    # 3. Crear Persona vinculada
    # Verificar si ya existe persona con ese nombre/rut (simulado)
    # Para evitar colisión de RUTs generados random, intentamos hasta que salga uno único
    rut = generar_rut()
    while Persona.objects.filter(Rut=rut).exists():
        rut = generar_rut()
        
    # Rutina especial para 'Bocchi Rivera' para no duplicar si corro el script de nuevo y borré usuario pero no persona
    # Pero aquí asumimos carga limpia o incremental segura
    
    sexo = obtener_sexo_random()
    
    persona = Persona.objects.create(
        Rut=rut,
        Nombre=nombre,
        Apellido_Paterno=apellido_p,
        Apellido_Materno=apellido_m,
        Fecha_nacimiento=date(random.randint(1970, 2000), random.randint(1, 12), random.randint(1, 28)),
        Sexo=sexo,
        Telefono=f"+569{random.randint(10000000, 99999999)}",
        Email=email,
        usuario=user # Link directo User-Persona
    )
    
    # 4. Crear PerfilUsuario (Para lógica de turnos y roles extendida)
    perfil, created = PerfilUsuario.objects.get_or_create(usuario=user)
    perfil.persona = persona
    perfil.cargo = cargo_titulo
    perfil.disponible = True
    perfil.save()
    
    return user

# ==========================================
# EJECUCIÓN
# ==========================================

def populate_users():
    print("🚀 INICIANDO CREACIÓN DE USUARIOS...")
    
    # CATALOGOS PREVIOS NECESARIOS
    # Aseguramos que haya sexos (si populate_full_system corrió, deberían estar)
    if not CatalogoSexo.objects.exists():
        CatalogoSexo.objects.create(codigo='F', nombre='Femenino')
        CatalogoSexo.objects.create(codigo='M', nombre='Masculino')

    # ------------------------------------------
    # 1. CUENTAS 'BOCCHI' (ADMIN, MEDICO, MATRONA, TENS)
    # ------------------------------------------
    print("\n--- Creando Cuentas Personales (Bocchi) ---")
    
    # Admin Principal
    create_user_complete(
        username="Bocchi",
        password=PASSWORD_BOCCHI,
        email=EMAIL_BOCCHI,
        nombre="Bocchi",
        apellido_p="Rivera",
        apellido_m="Admin",
        role_name=ROLES['ADMIN'],
        cargo_titulo="Administrador de Sistemas"
    )
    
    # Medico
    create_user_complete(
        username="BocchiMe",
        password=PASSWORD_BOCCHI,
        email=EMAIL_BOCCHI,
        nombre="Bocchi",
        apellido_p="Rivera",
        apellido_m="Medico",
        role_name=ROLES['MEDICO'],
        cargo_titulo="Médico Obstetra"
    )
    
    # Matrona
    create_user_complete(
        username="BocchiMa",
        password=PASSWORD_BOCCHI,
        email=EMAIL_BOCCHI,
        nombre="Bocchi",
        apellido_p="Rivera",
        apellido_m="Matrona",
        role_name=ROLES['MATRONA'],
        cargo_titulo="Matrona Supervisora"
    )
    
    # TENS
    create_user_complete(
        username="BocchiT",
        password=PASSWORD_BOCCHI,
        email=EMAIL_BOCCHI,
        nombre="Bocchi",
        apellido_p="Rivera",
        apellido_m="Tens",
        role_name=ROLES['TENS'],
        cargo_titulo="TENS de Turno"
    )

    # ------------------------------------------
    # 2. CUENTAS FICTICIAS REALISTAS
    # ------------------------------------------
    
    # --- ADMINS (2 adicionales) ---
    print("\n--- Generando Administradores Adicionales (2) ---")
    for i in range(2):
        nombre = random.choice(NOMBRES_HOMBRES + NOMBRES_MUJERES)
        ape_p = random.choice(APELLIDOS)
        ape_m = random.choice(APELLIDOS)
        username = f"admin{i+1}"
        
        create_user_complete(
            username=username,
            password=PASSWORD_DEFAULT,
            email=f"{username}@hospital.cl",
            nombre=nombre,
            apellido_p=ape_p,
            apellido_m=ape_m,
            role_name=ROLES['ADMIN'],
            cargo_titulo="Administrativo"
        )

    # --- MEDICOS (10) ---
    print("\n--- Generando Médicos (10) ---")
    for i in range(10):
        nombre = random.choice(NOMBRES_HOMBRES + NOMBRES_MUJERES)
        ape_p = random.choice(APELLIDOS)
        ape_m = random.choice(APELLIDOS)
        username = f"medico{i+1}"
        
        create_user_complete(
            username=username,
            password=PASSWORD_DEFAULT,
            email=f"{username}@hospital.cl",
            nombre=nombre,
            apellido_p=ape_p,
            apellido_m=ape_m,
            role_name=ROLES['MEDICO'],
            cargo_titulo="Ginecólogo Obstetra"
        )

    # --- MATRONAS (15) ---
    print("\n--- Generando Matronas (15) ---")
    for i in range(15):
        nombre = random.choice(NOMBRES_MUJERES) # Mayoría mujeres común en profesión, pero random mixto posible
        ape_p = random.choice(APELLIDOS)
        ape_m = random.choice(APELLIDOS)
        username = f"matrona{i+1}"
        
        create_user_complete(
            username=username,
            password=PASSWORD_DEFAULT,
            email=f"{username}@hospital.cl",
            nombre=nombre,
            apellido_p=ape_p,
            apellido_m=ape_m,
            role_name=ROLES['MATRONA'],
            cargo_titulo="Matrona Clínica"
        )

    # --- TENS (20) ---
    print("\n--- Generando TENS (20) ---")
    for i in range(20):
        nombre = random.choice(NOMBRES_HOMBRES + NOMBRES_MUJERES)
        ape_p = random.choice(APELLIDOS)
        ape_m = random.choice(APELLIDOS)
        username = f"tens{i+1}"
        
        create_user_complete(
            username=username,
            password=PASSWORD_DEFAULT,
            email=f"{username}@hospital.cl",
            nombre=nombre,
            apellido_p=ape_p,
            apellido_m=ape_m,
            role_name=ROLES['TENS'],
            cargo_titulo="Técnico en Enfermería"
        )

    print("\n✨ POBLACIÓN DE USUARIOS FINALIZADA ✨")
    print(f"  -> Contraseña Bocchi: {PASSWORD_BOCCHI}")
    print(f"  -> Contraseña Otros: {PASSWORD_DEFAULT}")

if __name__ == '__main__':
    populate_users()
