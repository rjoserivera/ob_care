import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obstetric_care.settings")
django.setup()

from django.contrib.auth.models import User
from django.conf import settings
from gestionProcesosApp.telegram_utils import enviar_telegram

def check_telegram():
    print(f"Bot Token Configured: {'Yes' if settings.TELEGRAM_BOT_TOKEN else 'No'}")
    if settings.TELEGRAM_BOT_TOKEN:
         print(f"Token ending in: ...{settings.TELEGRAM_BOT_TOKEN[-5:]}")

    # Find user 'Bocchi' or the one used in screenshots
    # Screenshot showed "Bocchi Rivera Medico" -> username likely 'Bocchi' (based on path) or similar.
    # I'll search for users with 'Bocchi' or 'medico'
    users = User.objects.filter(username__icontains='Bocchi')
    if not users.exists():
        print("User 'Bocchi' not found. Listing all users:")
        for u in User.objects.all()[:10]:
            print(f"- {u.username}")
            
    for u in users:
        print(f"Checking User: {u.username} ({u.get_full_name()})")
        if hasattr(u, 'perfil'):
            chat_id = u.perfil.telegram_chat_id
            print(f"  Telegram Chat ID: {chat_id}")
            
            if chat_id:
                print("  Attempting to send test message...")
                try:
                    success = enviar_telegram(chat_id, "Test message from AntiGravity Debugger.")
                    print(f"  Send Result: {success}")
                except Exception as e:
                    print(f"  Send Failed: {e}")
            else:
                print("  No Chat ID set. Notifications will fail.")
        else:
            print("  No Profile (Perfil) found.")

if __name__ == "__main__":
    check_telegram()
