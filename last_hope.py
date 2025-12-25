import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

def last_hope_final():
    print("Optimization: Resetting everything to NULL (FINAL)...")
    
    with connection.cursor() as cursor:
        # 1. Drop bad ID column
        try:
            cursor.execute("ALTER TABLE matronaApp_fichaobstetrica DROP COLUMN parentesco_acompanante_id")
            print("Dropped ID col.")
        except: pass

        # 2. Ensure parentesco_acompanante is cleaned
        try:
            cursor.execute("ALTER TABLE matronaApp_fichaobstetrica DROP COLUMN parentesco_acompanante")
        except: pass
        try:
            cursor.execute("ALTER TABLE matronaApp_fichaobstetrica ADD COLUMN parentesco_acompanante VARCHAR(20) NULL DEFAULT NULL")
            print("Recreated acompanante col.")
        except Exception as e:
            print(f"Error recreating acompanante: {e}")

        # 3. Ensure parentesco_contacto_emergencia is NULLable
        try:
            # MySQL syntax: MODIFY [COLUMN] col_name column_definition
            cursor.execute("ALTER TABLE matronaApp_fichaobstetrica MODIFY COLUMN parentesco_contacto_emergencia VARCHAR(20) NULL DEFAULT NULL")
            print("Modified contacto col to allow NULL.")
        except Exception as e:
            print(f"Error modifying contacto: {e}")

        # 4. FORCE NULL
        cursor.execute("UPDATE matronaApp_fichaobstetrica SET parentesco_acompanante = NULL")
        cursor.execute("UPDATE matronaApp_fichaobstetrica SET parentesco_contacto_emergencia = NULL")
        
        # 5. COMMIT
        connection.commit() # Important for DML
        
        # 6. Verify
        cursor.execute("SELECT count(*) FROM matronaApp_fichaobstetrica WHERE parentesco_contacto_emergencia IS NOT NULL")
        rem = cursor.fetchone()[0]
        print(f"Remaining Non-NULL contacts: {rem}")
        
        cursor.execute("SELECT count(*) FROM matronaApp_fichaobstetrica WHERE parentesco_acompanante IS NOT NULL")
        rem2 = cursor.fetchone()[0]
        print(f"Remaining Non-NULL acompanante: {rem2}")

if __name__ == '__main__':
    last_hope_final()
