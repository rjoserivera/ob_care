import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

def check_values():
    with connection.cursor() as cursor:
        cursor.execute("SELECT parentesco_acompanante, parentesco_contacto_emergencia FROM matronaApp_fichaobstetrica LIMIT 5")
        rows = cursor.fetchall()
        print("Values:")
        for row in rows:
            print(row)

if __name__ == '__main__':
    check_values()
