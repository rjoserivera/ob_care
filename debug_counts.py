import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from django.contrib.auth.models import User, Group

print("--- DEBUG COUNTS ---")

groups = ['Administrador', 'Matrona', 'Medico', 'TENS']

for g_name in groups:
    count_active = User.objects.filter(groups__name=g_name, is_active=True).count()
    count_total = User.objects.filter(groups__name=g_name).count()
    print(f"Group '{g_name}': Total={count_total}, Active={count_active}")
    
    # List active users in group
    users = User.objects.filter(groups__name=g_name, is_active=True)
    for u in users:
        print(f"  - {u.username} (Active: {u.is_active})")
