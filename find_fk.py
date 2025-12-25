import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

def find_fk():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT CONSTRAINT_NAME 
            FROM information_schema.KEY_COLUMN_USAGE 
            WHERE TABLE_NAME = 'matronaApp_fichaobstetrica' 
            AND COLUMN_NAME = 'parentesco_acompanante_id'
            AND TABLE_SCHEMA = DATABASE()
        """)
        rows = cursor.fetchall()
        print("Constraints found:")
        for row in rows:
            print(row[0])

if __name__ == '__main__':
    find_fk()
