import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from django.contrib.auth.models import Group

print("Grupos existentes:")
for g in Group.objects.all():
    print(f"- '{g.name}'")
