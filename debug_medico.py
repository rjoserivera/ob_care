
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obstetric_care.settings")
django.setup()

from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string
from django.test import RequestFactory
from authentication.views import DashboardMedicoView
from authentication.utils import user_has_role

def reproduce_medico_render():
    print("--- Role Check ---")
    # Ensure group exists
    # Check ACTUAL user 'medico'
    try:
        user = User.objects.get(username="medico")
        print(f"User 'medico' found. ID: {user.id}")
        print(f"User has roles: {[g.name for g in user.groups.all()]}")
        print(f"Check 'medicos': {user_has_role(user, 'medicos')}")
        
    except User.DoesNotExist:
        print("User 'medico' NOT FOUND.")
    
    return

    print("\n--- Template Render Check ---")
    factory = RequestFactory()
    request = factory.get('/dashboard/medico/')
    request.user = user
    
    view = DashboardMedicoView()
    view.setup(request)
    
    try:
        context = view.get_context_data()
        print("Context data retrieved successfully.")
        
        # We need to manually render because view.get() does a lot of dispatching
        # simpler to just render the template with context
        content = render_to_string("Medico/Data/dashboard_medico.html", context, request=request)
        print("Template rendered successfully.")
        print(f"Content length: {len(content)}")
    except Exception as e:
        print(f"ERROR RENDER: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reproduce_medico_render()
