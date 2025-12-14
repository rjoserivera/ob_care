"""
SCRIPT DE INICIALIZACIÓN DEL PROYECTO OBSTETRIC CARE
----------------------------------------------------
Este script configura automáticamente:
1. Roles (Grupos) de Usuario
2. Usuarios Iniciales (Admin, Matrona, Médico, TENS)
3. Catálogos Base (Vías de Administración, Consultorios, Medicamentos)

Uso: python setup_project.py
"""

import os
import django
import sys

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.db import transaction
from matronaApp.models import (
    CatalogoViaAdministracion, 
    CatalogoConsultorioOrigen, 
    CatalogoMedicamento
)

def print_step(title):
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")

def print_ok(msg):
    print(f"  ✅ {msg}")

def print_info(msg):
    print(f"  ℹ️  {msg}")

@transaction.atomic
def run_setup():
    # 1. ROLES (GRUPOS)
    print_step("CREANDO ROLES DE USUARIO")
    roles = ['Matrona', 'Médico', 'TENS', 'Administrativo']
    for role_name in roles:
        group, created = Group.objects.get_or_create(name=role_name)
        if created:
            print_ok(f"Grupo '{role_name}' creado.")
        else:
            print_info(f"Grupo '{role_name}' ya existe.")

    # 2. USUARIOS
    print_step("CREANDO USUARIOS INICIALES")
    users_data = [
        {
            'username': 'admin', 'email': 'admin@obcare.cl', 'pass': 'admin123', 
            'first': 'Administrador', 'last': 'Sistema', 'is_superuser': True, 'group': None
        },
        {
            'username': 'matrona', 'email': 'matrona@obcare.cl', 'pass': 'matrona123', 
            'first': 'María', 'last': 'López', 'is_superuser': False, 'group': 'Matrona'
        },
        {
            'username': 'medico', 'email': 'medico@obcare.cl', 'pass': 'medico123', 
            'first': 'Carlos', 'last': 'González', 'is_superuser': False, 'group': 'Médico'
        },
        {
            'username': 'tens', 'email': 'tens@obcare.cl', 'pass': 'tens123', 
            'first': 'Juan', 'last': 'Martínez', 'is_superuser': False, 'group': 'TENS'
        },
    ]

    for u_data in users_data:
        try:
            if User.objects.filter(username=u_data['username']).exists():
                user = User.objects.get(username=u_data['username'])
                print_info(f"Usuario '{u_data['username']}' ya existe. (Actualizando datos básicos)")
                user.first_name = u_data['first']
                user.last_name = u_data['last']
                user.email = u_data['email']
                # Nota: No reseteamos la password si ya existe para no bloquear al usuario, 
                # a menos que sea una instalación limpia.
            else:
                user = User.objects.create_user(
                    username=u_data['username'],
                    email=u_data['email'],
                    password=u_data['pass']
                )
                print_ok(f"Usuario '{u_data['username']}' creado.")

            user.is_staff = True  # Todos pueden entrar al admin por defecto en dev
            user.is_superuser = u_data['is_superuser']
            user.first_name = u_data['first']
            user.last_name = u_data['last']
            user.save()

            if u_data['group']:
                group = Group.objects.get(name=u_data['group'])
                user.groups.add(group)
                print_ok(f"Rol '{u_data['group']}' asignado a {u_data['username']}.")
        
        except Exception as e:
            print(f"  ❌ Error creando usuario {u_data['username']}: {e}")

    # 3. CATÁLOGOS - VÍAS DE ADMINISTRACIÓN
    print_step("POBLANDO CATÁLOGO: VÍAS DE ADMINISTRACIÓN")
    vias = [
        ('ORAL', 'Vía Oral', 'Administración por boca'),
        ('IV', 'Endovenosa (I.V.)', 'Inyección directa en vena'),
        ('IM', 'Intramuscular (I.M.)', 'Inyección en músculo'),
        ('SC', 'Subcutánea (S.C.)', 'Inyección bajo la piel'),
        ('SUBL', 'Sublingual', 'Debajo de la lengua'),
        ('TOP', 'Tópica', 'Sobre la piel'),
        ('VAG', 'Vaginal', 'Administración vaginal'),
        ('REC', 'Rectal', 'Administración rectal'),
    ]
    
    for i, (codigo, nombre, desc) in enumerate(vias):
        obj, created = CatalogoViaAdministracion.objects.update_or_create(
            codigo=codigo,
            defaults={'nombre': nombre, 'descripcion': desc, 'orden': i+1, 'activo': True}
        )
        if created:
            print_ok(f"Vía '{nombre}' creada.")

    # 4. CATÁLOGOS - CONSULTORIOS
    print_step("POBLANDO CATÁLOGO: CONSULTORIOS")
    consultorios = [
        ('CESFAM1', 'CESFAM Dr. Juan A.', 'Consultorio zona norte'),
        ('CESFAM2', 'CESFAM Santa Cecilia', 'Consultorio zona centro'),
        ('HOSP1', 'Hospital Regional', 'Derivación interna'),
        ('PRIV1', 'Clínica Privada', 'Externo'),
    ]
    
    for i, (codigo, nombre, desc) in enumerate(consultorios):
        obj, created = CatalogoConsultorioOrigen.objects.update_or_create(
            codigo=codigo,
            defaults={'nombre': nombre, 'descripcion': desc, 'orden': i+1, 'activo': True}
        )
        if created:
            print_ok(f"Consultorio '{nombre}' creado.")

    # 5. CATÁLOGOS - MEDICAMENTOS (BÁSICOS)
    print_step("POBLANDO CATÁLOGO: MEDICAMENTOS BÁSICOS")
    medicamentos = [
        ('PARACETAMOL', 'Paracetamol', '500mg', 'Comprimido', 'mg'),
        ('IBUPROFENO', 'Ibuprofeno', '400mg', 'Comprimido', 'mg'),
        ('OXITOCINA', 'Oxitocina', '10 UI', 'Ampolla', 'UI'),
        ('LIDOCAINA', 'Lidocaína', '2%', 'Ampolla', '%'),
        ('PENICILINA', 'Penicilina G Sódica', '2.000.000 UI', 'Frasco Ampolla', 'UI'),
        ('AMPICILINA', 'Ampicilina', '500mg', 'Comprimido', 'mg'),
        ('SULFAFERROSO', 'Sulfato Ferroso', '200mg', 'Gragea', 'mg'),
        ('CALCIO', 'Calcio', '500mg', 'Comprimido', 'mg'),
    ]

    for codigo, nombre, conc, pres, unidad in medicamentos:
        obj, created = CatalogoMedicamento.objects.update_or_create(
            codigo=codigo,
            defaults={
                'nombre': nombre, 
                'concentracion': conc, 
                'presentacion': pres, 
                'unidad': unidad,
                'activo': True
            }
        )
        if created:
            print_ok(f"Medicamento '{nombre}' creado.")

    print_step("✅ CONFIGURACIÓN FINALIZADA CON ÉXITO")
    print("\nCredenciales iniciales:")
    print("  - Admin:   admin   / admin123")
    print("  - Matrona: matrona / matrona123")
    print("  - Médico:  medico  / medico123")
    print("  - TENS:    tens    / tens123")
    print("\nYa puedes ejecutar el servidor: python manage.py runserver")

if __name__ == '__main__':
    try:
        run_setup()
    except Exception as e:
        print(f"\n❌ Error fatal durante la configuración: {e}")
        sys.exit(1)
