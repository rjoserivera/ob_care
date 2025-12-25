import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

def nuke_parentesco_strings():
    print("Clearing old parentesco strings to allow FK conversion...")
    with connection.cursor() as cursor:
        # Try both names just in case, though likely it's the model field name
        # In MySQL/SQLite, Django maps field 'parentesco_acompanante' to column 'parentesco_acompanante' initially.
        cursor.execute("UPDATE matronaApp_fichaobstetrica SET parentesco_acompanante = NULL")
        cursor.execute("UPDATE matronaApp_fichaobstetrica SET parentesco_contacto_emergencia = NULL")
    print("Done.")

if __name__ == '__main__':
    nuke_parentesco_strings()
