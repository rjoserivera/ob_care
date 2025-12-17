import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from gestionApp.models import Persona

print("Fields in Persona model:")
for field in Persona._meta.get_fields():
    print(field.name)
