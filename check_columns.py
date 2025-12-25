import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

def check_columns():
    with connection.cursor() as cursor:
        cursor.execute("DESCRIBE matronaApp_fichaobstetrica")
        rows = cursor.fetchall()
        for row in rows:
            if 'parentesco' in row[0]:
                print(f"COLUMN FOUND: {row[0]}")

if __name__ == '__main__':
    check_columns()
