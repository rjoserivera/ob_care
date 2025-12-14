"""
Script para crear usuarios de forma rápida desde Django shell
Ejecutar con: python manage.py shell < crear_usuarios_ahora.py
"""

from django.contrib.auth.models import User, Group

print("\n" + "="*60)
print("CREANDO USUARIOS DEL SISTEMA")
print("="*60 + "\n")

# 1. Crear grupos
print("📁 Creando grupos...")
grupos_nombres = ['Administrador', 'Medico', 'Matrona', 'TENS', 'Paciente']
for nombre in grupos_nombres:
    grupo, created = Group.objects.get_or_create(name=nombre)
    if created:
        print(f"  ✅ Grupo '{nombre}' creado")
    else:
        print(f"  ⚠️  Grupo '{nombre}' ya existe")

# 2. Crear Admin
print("\n👑 Creando Administrador...")
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
    print("  ✅ Usuario: admin / pass123 (Administrador)")
else:
    print("  ⚠️  Usuario 'admin' ya existe")

# 3. Crear Médico
print("\n🩺 Creando Médico...")
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
    print("  ✅ Usuario: medico / pass123 (Médico)")
else:
    print("  ⚠️  Usuario 'medico' ya existe")

# 4. Crear Matrona
print("\n👩‍⚕️ Creando Matrona...")
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
    print("  ✅ Usuario: matrona / pass123 (Matrona)")
else:
    print("  ⚠️  Usuario 'matrona' ya existe")

# 5. Crear TENS
print("\n🏥 Creando TENS...")
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
    print("  ✅ Usuario: tens / pass123 (TENS)")
else:
    print("  ⚠️  Usuario 'tens' ya existe")

# Resumen
print("\n" + "="*60)
print("✅ PROCESO COMPLETADO")
print("="*60)
print("\n📋 CREDENCIALES DE ACCESO:")
print("   ┌─────────────┬─────────────┬─────────────────┐")
print("   │ Usuario     │ Contraseña  │ Rol             │")
print("   ├─────────────┼─────────────┼─────────────────┤")
print("   │ admin       │ pass123     │ Administrador   │")
print("   │ medico      │ pass123     │ Médico          │")
print("   │ matrona     │ pass123     │ Matrona         │")
print("   │ tens        │ pass123     │ TENS            │")
print("   └─────────────┴─────────────┴─────────────────┘")
print("\n🔗 Ahora puedes iniciar sesión en: http://localhost:8000/auth/login/\n")
