import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

def brute_revert():
    print("Brute force revert...")
    with connection.cursor() as cursor:
        # 1. Try to drop ID column
        try:
            print("Dropping parentesco_acompanante_id...")
            cursor.execute("ALTER TABLE matronaApp_fichaobstetrica DROP COLUMN parentesco_acompanante_id")
            print("Dropped ID col.")
        except Exception as e:
            print(f"Error dropping ID col: {e}")
            # Identify constraint?

        # 2. Try to drop standard column (if exists duplicate)
        try:
            print("Dropping parentesco_acompanante...")
            cursor.execute("ALTER TABLE matronaApp_fichaobstetrica DROP COLUMN parentesco_acompanante")
            print("Dropped normal col.")
        except Exception as e:
            print(f"Error dropping normal col: {e}")

        # 3. Add column back
        try:
            print("Adding parentesco_acompanante back...")
            cursor.execute("ALTER TABLE matronaApp_fichaobstetrica ADD COLUMN parentesco_acompanante VARCHAR(20) NULL")
            print("Added back.")
        except Exception as e:
            print(f"Error adding back: {e}")

        # 4. Clean other column
        try:
            print("Cleaning parentesco_contacto_emergencia...")
            cursor.execute("UPDATE matronaApp_fichaobstetrica SET parentesco_contacto_emergencia = NULL")
        except Exception as e:
            print(f"Error cleaning contact: {e}")

if __name__ == '__main__':
    brute_revert()
