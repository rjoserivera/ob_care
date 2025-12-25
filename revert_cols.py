import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

def revert_cols():
    print("Reverting column state...")
    with connection.cursor() as cursor:
        try:
            print("Dropping parentesco_acompanante_id...")
            cursor.execute("ALTER TABLE matronaApp_fichaobstetrica DROP COLUMN parentesco_acompanante_id")
        except Exception as e:
            print(f"Drop error (ignorable if not exists): {e}")

        try:
            print("Adding parentesco_acompanante...")
            cursor.execute("ALTER TABLE matronaApp_fichaobstetrica ADD COLUMN parentesco_acompanante VARCHAR(20)")
        except Exception as e:
            print(f"Add error: {e}")

        try:
            print("Cleaning parentesco_contacto_emergencia...")
            cursor.execute("UPDATE matronaApp_fichaobstetrica SET parentesco_contacto_emergencia = NULL")
        except Exception as e:
            print(f"Clean error: {e}")

if __name__ == '__main__':
    revert_cols()
