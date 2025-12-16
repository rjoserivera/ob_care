
import os
import sys

# Agregar root del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
import random
from datetime import date

# Configurar entorno Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obstetric_care.settings")
django.setup()

from django.contrib.auth.models import User, Group
from django.db import transaction
from gestionApp.models import (
    Persona, PerfilUsuario, CatalogoSexo, CatalogoNacionalidad, 
    CatalogoPrevision, CatalogoEstadoCivil, CatalogoTurno
)

# Configuración
COMMON_PASS = "Tomas216"

def print_header(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def print_created(role, username, name):
    print(f"  👤 [{role}] {username} - {name}")

# Generador de datos random simple
NOMBRES_M = ["Juan", "Pedro", "Luis", "Carlos", "Jose", "Manuel", "Jorge", "Francisco", "David", "Miguel", "Diego", "Javier", "Ricardo", "Daniel", "Fernando", "Roberto", "Andres", "Hector", "Sergio", "Pablo"]
NOMBRES_F = ["Maria", "Ana", "Carmen", "Rosa", "Francisca", "Claudia", "Patricia", "Camila", "Daniela", "Valentina", "Carolina", "Andrea", "Fernanda", "Javiera", "Constanza", "Paulina", "Marcela", "Catalina", "Gabriela", "Rocio"]
APELLIDOS = ["González", "Muñoz", "Rojas", "Díaz", "Pérez", "Soto", "Contreras", "Silva", "Martínez", "Sepúlveda", "Morales", "Rodríguez", "López", "Fuentes", "Hernández", "Torres", "Araya", "Flores", "Espinoza", "Valenzuela", "Castillo", "Tapia", "Reyes", "Gutiérrez", "Castro", "Pizarro", "Álvarez", "Vásquez", "Sánchez", "Fernández"]

def generar_rut(index):
    # Genera un RUT válido simple basado en un índice para evitar colisiones
    base = 10000000 + index
    rut_str = str(base)
    # Calculo DV
    multiplo = 2
    suma = 0
    for digit in reversed(rut_str):
        suma += int(digit) * multiplo
        multiplo = multiplo + 1 if multiplo < 7 else 2
    resto = suma % 11
    dv = str(11 - resto)
    if dv == "11": dv = "0"
    if dv == "10": dv = "K"
    return f"{base}-{dv}"

def get_random_item(model):
    count = model.objects.count()
    if count == 0: return None
    random_index = random.randint(0, count - 1)
    return model.objects.all()[random_index]

def create_staff_user(username, first_name, last_name, role_name, rut, turno_code=None, is_superuser=False):
    # 1. Crear Usuario
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        print(f"  ℹ️  Usuario {username} ya existe (Actualizando...)")
        user.set_password(COMMON_PASS)
        user.first_name = first_name
        user.last_name = last_name
        user.is_superuser = is_superuser
        user.is_staff = True
        user.save()
    else:
        user = User.objects.create_user(
            username=username,
            password=COMMON_PASS,
            first_name=first_name,
            last_name=last_name,
            email=f"{username.lower()}@obcare.cl",
            is_staff=True,
            is_superuser=is_superuser
        )

    # 2. Asignar Grupo
    group, _ = Group.objects.get_or_create(name=role_name)
    user.groups.add(group)

    # 3. Crear Persona
    sexo_obj = CatalogoSexo.objects.first() # Default
    nac_obj = CatalogoNacionalidad.objects.first()
    
    # Intentar buscar persona por RUT o crear
    persona, created = Persona.objects.update_or_create(
        Rut=rut,
        defaults={
            'Nombre': first_name,
            'Apellido_Paterno': last_name,
            'Apellido_Materno': random.choice(APELLIDOS),
            'Fecha_nacimiento': date(1980 + random.randint(0, 20), 1, 1),
            'Sexo': sexo_obj,
            'Nacionalidad': nac_obj,
            'Telefono': "912345678",
            'usuario': user
        }
    )

    # 4. Crear PerfilUsuario
    if turno_code:
        turno = CatalogoTurno.objects.filter(codigo=turno_code).first()
    else:
        turnos = CatalogoTurno.objects.exclude(codigo='24HRS') # Rotativos no suelen ser 24hrs fijos en este contexto ficticio, o sí.
        if turnos.exists():
            turno = random.choice(turnos)
        else:
            turno = None

    PerfilUsuario.objects.update_or_create(
        usuario=user,
        defaults={
            'persona': persona,
            'cargo': role_name,
            'turno_actual': turno,
            'disponible': True, # Asumimos entran disponibles
            'telefono_institucional': f"ANEXO-{random.randint(100,999)}"
        }
    )
    
    return user

@transaction.atomic
def populate_users():
    print_header("CREANDO USUARIOS DEL SISTEMA")
    
    # Reset contador RUT ficticio
    rut_counter = 1
    
    # ---------------------------------------------------------
    # 1. USUARIOS CORE (Los Bocchi)
    # ---------------------------------------------------------
    print("--- Usuarios Principales (24/7) ---")
    
    # Admin
    create_staff_user(
        'Bocchi', 'Bocchi', 'Admin', 'Administradores', 
        generar_rut(rut_counter), turno_code='24HRS', is_superuser=True
    )
    print_created("Admin", "Bocchi", "Bocchi Admin")
    rut_counter += 1
    
    # Medico
    create_staff_user(
        'BocchiMe', 'Bocchi', 'Medico', 'Medicos', 
        generar_rut(rut_counter), turno_code='24HRS'
    )
    print_created("Médico", "BocchiMe", "Bocchi Medico")
    rut_counter += 1

    # Matrona
    create_staff_user(
        'BocchiMa', 'Bocchi', 'Matrona', 'Matronas', 
        generar_rut(rut_counter), turno_code='24HRS'
    )
    print_created("Matrona", "BocchiMa", "Bocchi Matrona")
    rut_counter += 1
    
    # TENS
    create_staff_user(
        'BocchiT', 'Bocchi', 'TENS', 'TENS', 
        generar_rut(rut_counter), turno_code='24HRS'
    )
    print_created("TENS", "BocchiT", "Bocchi TENS")
    rut_counter += 1

    # ---------------------------------------------------------
    # 2. PERSONAL ROTATIVO
    # ---------------------------------------------------------
    print("\n--- Generando Personal Rotativo ---")
    
    # Configuración de cantidades
    CANT_MEDICOS = 15
    CANT_MATRONAS = 24
    CANT_TENS = 30
    
    # Listas para username generation
    used_usernames = set(['bocchi', 'bocchime', 'bocchima', 'bocchit'])

    def generate_staff_batch(role_name, count, prefix):
        nonlocal rut_counter
        print(f"\nGenerando {count} {role_name}...")
        
        for i in range(count):
            is_female = random.choice([True, False])
            first = random.choice(NOMBRES_F if is_female else NOMBRES_M)
            last = random.choice(APELLIDOS)
            
            # Username unico
            base_username = f"{prefix}_{first[:3].lower()}{last.lower()}"
            username = base_username
            num = 1
            while username in used_usernames:
                username = f"{base_username}{num}"
                num += 1
            used_usernames.add(username)
            
            create_staff_user(
                username, first, last, role_name, 
                generar_rut(rut_counter)
            )
            if i < 3: # Solo imprimir los primeros para no saturar
                print_created(role_name, username, f"{first} {last}")
            elif i == 3:
                print("  ...")
            
            rut_counter += 1

    # Crear Grupos Plurales si no existen
    for g in ['Medicos', 'Matronas', 'TENS', 'Administradores']:
        Group.objects.get_or_create(name=g)

    # --- MEDICOS ---
    # generate_staff_batch('Medicos', CANT_MEDICOS, 'dr')
    
    # --- MATRONAS ---
    # generate_staff_batch('Matronas', CANT_MATRONAS, 'mat')
    
    # --- TENS ---
    # generate_staff_batch('TENS', CANT_TENS, 'tens')

    print_header("✅ USUARIOS CREADOS EXITOSAMENTE")
    print(f"Contraseña para todos: {COMMON_PASS}")

if __name__ == '__main__':
    populate_users()
