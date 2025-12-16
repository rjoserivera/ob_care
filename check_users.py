import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obstetric_care.settings")
django.setup()

from django.contrib.auth.models import User
from authentication.utils import user_has_role

print("--- Checking Users & Roles ---")
users = User.objects.all()
for u in users:
    groups = [g.name for g in u.groups.all()]
    if not groups: continue
    
    print(f"User: {u.username} | Groups: {groups}")
    print(f"  -> Has role 'medico' (singular)? {user_has_role(u, 'medico')}")
    print(f"  -> Has role 'medicos' (plural)? {user_has_role(u, 'medicos')}")
