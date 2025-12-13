from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Actualiza el email de TODOS los usuarios para pruebas'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='El correo electrónico para asignar a todos los usuarios')

    def handle(self, *args, **options):
        email = options['email']
        users = User.objects.all()
        count = users.count()
        
        self.stdout.write(f'Actualizando {count} usuarios con el correo: {email}...')
        
        # Update all users
        User.objects.all().update(email=email)
        
        self.stdout.write(self.style.SUCCESS(f'¡Listo! Correos actualizados.'))
