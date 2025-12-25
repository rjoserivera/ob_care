import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

def revert_db_columns():
    print("Reverting DB columns to match CharField model...")
    with connection.cursor() as cursor:
        try:
            # Check if _id exists
            cursor.execute("SHOW COLUMNS FROM matronaApp_fichaobstetrica LIKE 'parentesco_acompanante_id'")
            if cursor.fetchone():
                print("Found parentesco_acompanante_id. Renaming to parentesco_acompanante...")
                # MySQL 5.7+ syntax: CHANGE old new type
                # Assuming it is VARCHAR or INT. We force it to VARCHAR(50) to match my planned update or original.
                # Original was VARCHAR(20).
                cursor.execute("ALTER TABLE matronaApp_fichaobstetrica CHANGE parentesco_acompanante_id parentesco_acompanante VARCHAR(50) NULL DEFAULT NULL")
                print("Renamed successfully.")
            else:
                print("parentesco_acompanante_id not found.")
                
            # Check if parentesco_acompanante exists now
            cursor.execute("SHOW COLUMNS FROM matronaApp_fichaobstetrica LIKE 'parentesco_acompanante'")
            if cursor.fetchone():
                print("parentesco_acompanante exists.")
            else:
                print("WARNING: parentesco_acompanante STILL MISSING.")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    revert_db_columns()
