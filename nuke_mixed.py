import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

def nuke_mixed():
    print("Clearing columns...")
    with connection.cursor() as cursor:
        try:
            print("Cleaning parentesco_acompanante_id...")
            cursor.execute("UPDATE matronaApp_fichaobstetrica SET parentesco_acompanante_id = NULL")
        except Exception as e:
            print(f"Error 1: {e}")
            
        try:
            print("Cleaning parentesco_contacto_emergencia...")
            cursor.execute("UPDATE matronaApp_fichaobstetrica SET parentesco_contacto_emergencia = NULL")
        except Exception as e:
            print(f"Error 2: {e}")

if __name__ == '__main__':
    nuke_mixed()
