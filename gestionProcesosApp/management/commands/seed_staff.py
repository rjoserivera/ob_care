from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils import timezone
from gestionProcesosApp.models import PersonalTurno
import random

class Command(BaseCommand):
    help = 'Creates 60+ dummy staff members (20 per role) with active shifts'

    def handle(self, *args, **options):
        self.stdout.write('Seeding mass staff data...')
        
        roles_config = [
            ('MEDICO', 'Medico', 22),
            ('MATRONA', 'Matrona', 22),
            ('TENS', 'TENS', 22),
        ]

        now = timezone.now()
        end_time = now + timezone.timedelta(hours=24) # 24h coverage

        total_created = 0
        
        for rol_code, group_name, count in roles_config:
            self.stdout.write(f'Processing {group_name}s...')
            
            # Create Group
            group, _ = Group.objects.get_or_create(name=group_name)

            for i in range(1, count + 1):
                username = f"{rol_code.lower()}_{i}"
                first_name = f"{group_name}"
                last_name = f"Test {i}"
                
                # 1. Create User
                user, created = User.objects.get_or_create(username=username)
                if created:
                    user.set_password('test1234')
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    user.groups.add(group)
                
                # 2. Check/Create Shift
                # We want them ALL active now for the dashboard demo as requested
                active_shift = PersonalTurno.objects.filter(
                    usuario=user,
                    fecha_fin_turno__gte=now,
                    estado='DISPONIBLE'
                ).first()

                if not active_shift:
                    PersonalTurno.objects.create(
                        usuario=user,
                        rol=rol_code,
                        estado='DISPONIBLE',
                        fecha_inicio_turno=now,
                        fecha_fin_turno=end_time
                    )
                    total_created += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {total_created} new active shifts! Total staff pool is now large.'))
