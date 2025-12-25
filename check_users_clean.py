import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obstetric_care.settings")
django.setup()

from django.contrib.auth.models import User

def check_users():
    print("Listing Medical Users matching 'Bocchi' or 'Medico':")
    users = User.objects.filter(username__icontains='Bocchi') | User.objects.filter(username__icontains='Medico')
    
    for u in users:
        chat_id = "NOT SET"
        if hasattr(u, 'perfil'):
            chat_id = u.perfil.telegram_chat_id or "None"
        
        print(f"User: {u.username} | Name: {u.get_full_name()} | Chat ID: {chat_id}")

if __name__ == "__main__":
    check_users()
