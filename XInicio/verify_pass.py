import os
import sys
import django
from django.contrib.auth import authenticate

# Path fix
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obstetric_care.settings")
django.setup()

from django.contrib.auth.models import User

try:
    user = User.objects.get(username='Bocchi')
    if user.check_password('Tomas216'):
        print("VERIFICATION SUCCESS: Password is Tomas216")
    else:
        print("VERIFICATION FAILED: Password is NOT Tomas216")
except Exception as e:
    print(f"Error: {e}")
