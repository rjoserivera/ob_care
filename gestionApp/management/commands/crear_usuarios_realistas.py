"""
Comando para crear usuarios realistas para el sistema
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from gestionApp.models import Persona, PerfilUsuario
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Crea usuarios realistas para el sistema'

    def handle(self, *args, **options):
        # Datos realistas
        medicos_data = [
            {'username': 'BocchiMe', 'first_name': 'Joseph', 'last_name': 'Rivera', 'rut': '18.234.567-8'},
            {'username': 'drgarcia', 'first_name': 'Carlos', 'last_name': 'García Mendoza', 'rut': '16.789.234-5'},
            {'username': 'dramorales', 'first_name': 'Ana', 'last_name': 'Morales Silva', 'rut': '17.456.123-9'},
            {'username': 'drlopez', 'first_name': 'Roberto', 'last_name': 'López Fernández', 'rut': '15.987.654-2'},
            {'username': 'drsanchez', 'first_name': 'Patricia', 'last_name': 'Sánchez Rojas', 'rut': '16.234.789-1'},
            {'username': 'drramirez', 'first_name': 'Fernando', 'last_name': 'Ramírez Castro', 'rut': '17.890.123-4'},
            {'username': 'drmartinez', 'first_name': 'Claudia', 'last_name': 'Martínez Vega', 'rut': '18.345.678-0'},
            {'username': 'drherrera', 'first_name': 'Miguel', 'last_name': 'Herrera Díaz', 'rut': '15.678.901-3'},
        ]
        
        matronas_data = [
            {'username': 'BocchiMa', 'first_name': 'Joseph', 'last_name': 'Rivera', 'rut': '19.123.456-7'},
            {'username': 'matronacarla', 'first_name': 'Carla', 'last_name': 'Rojas Pérez', 'rut': '18.654.321-0'},
            {'username': 'matronaisabel', 'first_name': 'Isabel', 'last_name': 'Muñoz Torres', 'rut': '17.234.567-3'},
            {'username': 'matronapaula', 'first_name': 'Paula', 'last_name': 'Soto Vargas', 'rut': '19.876.543-1'},
            {'username': 'matronacamila', 'first_name': 'Camila', 'last_name': 'Fuentes Ríos', 'rut': '18.123.789-5'},
            {'username': 'matronabeatriz', 'first_name': 'Beatriz', 'last_name': 'Navarro Campos', 'rut': '17.789.456-2'},
            {'username': 'matronasofía', 'first_name': 'Sofía', 'last_name': 'Castillo Mora', 'rut': '19.456.123-8'},
            {'username': 'matronagabriela', 'first_name': 'Gabriela', 'last_name': 'Pinto Salazar', 'rut': '18.890.234-6'},
            {'username': 'matronavaleria', 'first_name': 'Valeria', 'last_name': 'Ortiz Bravo', 'rut': '17.567.890-9'},
            {'username': 'matronafernanda', 'first_name': 'Fernanda', 'last_name': 'Guzmán Leiva', 'rut': '19.234.567-4'},
        ]
        
        tens_data = [
            {'username': 'BocchiT', 'first_name': 'Joseph', 'last_name': 'Rivera', 'rut': '20.345.678-9'},
            {'username': 'tensjuan', 'first_name': 'Juan', 'last_name': 'Contreras Díaz', 'rut': '19.456.789-2'},
            {'username': 'tenslucia', 'first_name': 'Lucía', 'last_name': 'Vega Campos', 'rut': '18.567.890-4'},
            {'username': 'tensmaria', 'first_name': 'María', 'last_name': 'Flores Reyes', 'rut': '17.678.901-6'},
            {'username': 'tensandres', 'first_name': 'Andrés', 'last_name': 'Moreno Silva', 'rut': '19.789.012-3'},
            {'username': 'tenscarolina', 'first_name': 'Carolina', 'last_name': 'Riquelme Pérez', 'rut': '18.890.123-7'},
            {'username': 'tensricardo', 'first_name': 'Ricardo', 'last_name': 'Espinoza Muñoz', 'rut': '17.901.234-5'},
            {'username': 'tensveronica', 'first_name': 'Verónica', 'last_name': 'Tapia González', 'rut': '20.012.345-8'},
            {'username': 'tensdiego', 'first_name': 'Diego', 'last_name': 'Cortés Vargas', 'rut': '19.123.456-1'},
            {'username': 'tensnatalia', 'first_name': 'Natalia', 'last_name': 'Bustos Rojas', 'rut': '18.234.567-9'},
        ]
        
        password = 'Tomas216'
        
        # Obtener o crear grupos
        grupo_medicos, _ = Group.objects.get_or_create(name='Medicos')
        grupo_matronas, _ = Group.objects.get_or_create(name='Matronas')
        grupo_tens, _ = Group.objects.get_or_create(name='TENS')
        
        # Crear médicos
        self.stdout.write(self.style.SUCCESS('\n👨‍⚕️ Creando Médicos...'))
        for data in medicos_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': f"{data['username']}@hospital.cl",
                    'is_active': True
                }
            )
            if created:
                user.set_password(password)
                user.save()
            
            user.groups.add(grupo_medicos)
            
            # Crear Persona
            persona, _ = Persona.objects.get_or_create(
                Rut=data['rut'],
                defaults={
                    'Nombre': data['first_name'],
                    'Apellido_Paterno': data['last_name'].split()[0],
                    'Apellido_Materno': data['last_name'].split()[1] if len(data['last_name'].split()) > 1 else '',
                    'Fecha_nacimiento': timezone.now().date().replace(year=1985 + random.randint(0, 15)),
                    'Sexo_id': 1 if data['first_name'] in ['Joseph', 'Carlos', 'Roberto', 'Juan', 'Fernando', 'Miguel', 'Andrés', 'Ricardo', 'Diego'] else 2
                }
            )
            
            # Crear Perfil
            perfil, _ = PerfilUsuario.objects.get_or_create(
                usuario=user,
                defaults={
                    'persona': persona,
                    'cargo': 'Médico Obstetra',
                    'disponible': True
                }
            )
            
            self.stdout.write(f'  ✅ {user.username} - {user.get_full_name()}')
        
        # Crear matronas
        self.stdout.write(self.style.SUCCESS('\n👩‍⚕️ Creando Matronas...'))
        for data in matronas_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': f"{data['username']}@hospital.cl",
                    'is_active': True
                }
            )
            if created:
                user.set_password(password)
                user.save()
            
            user.groups.add(grupo_matronas)
            
            persona, _ = Persona.objects.get_or_create(
                Rut=data['rut'],
                defaults={
                    'Nombre': data['first_name'],
                    'Apellido_Paterno': data['last_name'].split()[0],
                    'Apellido_Materno': data['last_name'].split()[1] if len(data['last_name'].split()) > 1 else '',
                    'Fecha_nacimiento': timezone.now().date().replace(year=1985 + random.randint(0, 15)),
                    'Sexo_id': 1 if data['first_name'] in ['Joseph'] else 2
                }
            )
            
            perfil, _ = PerfilUsuario.objects.get_or_create(
                usuario=user,
                defaults={
                    'persona': persona,
                    'cargo': 'Matrona',
                    'disponible': True
                }
            )
            
            self.stdout.write(f'  ✅ {user.username} - {user.get_full_name()}')
        
        # Crear TENS
        self.stdout.write(self.style.SUCCESS('\n🩺 Creando TENS...'))
        for data in tens_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': f"{data['username']}@hospital.cl",
                    'is_active': True
                }
            )
            if created:
                user.set_password(password)
                user.save()
            
            user.groups.add(grupo_tens)
            
            persona, _ = Persona.objects.get_or_create(
                Rut=data['rut'],
                defaults={
                    'Nombre': data['first_name'],
                    'Apellido_Paterno': data['last_name'].split()[0],
                    'Apellido_Materno': data['last_name'].split()[1] if len(data['last_name'].split()) > 1 else '',
                    'Fecha_nacimiento': timezone.now().date().replace(year=1985 + random.randint(0, 15)),
                    'Sexo_id': 1 if data['first_name'] in ['Joseph'] else 2
                }
            )
            
            perfil, _ = PerfilUsuario.objects.get_or_create(
                usuario=user,
                defaults={
                    'persona': persona,
                    'cargo': 'TENS',
                    'disponible': True
                }
            )
            
            self.stdout.write(f'  ✅ {user.username} - {user.get_full_name()}')
        
        self.stdout.write(self.style.SUCCESS('\n\n🎉 ¡Usuarios creados exitosamente!'))
        self.stdout.write(self.style.WARNING('\n📝 Credenciales:'))
        self.stdout.write(f'   Contraseña para todos: {password}')
        self.stdout.write('\n👤 Usuarios creados:')
        self.stdout.write('   Médicos: BocchiMe, drgarcia, dramorales, drlopez')
        self.stdout.write('   Matronas: BocchiMa, matronacarla, matronaisabel, matronapaula')
        self.stdout.write('   TENS: BocchiT, tensjuan, tenslucia, tensmaria')
