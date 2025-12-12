"""
inicioApp/views.py
Vista principal de inicio - CORREGIDO para usar User + Groups
"""

from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.models import User, Group

from gestionApp.models import Paciente
from authentication.utils import get_dashboard_url_for_user


def home(request):
    """
    Vista principal de inicio
    - Si está autenticado → Redirige a su dashboard
    - Si NO está autenticado → Muestra pantalla de descanso/screensaver
    """
    # Si el usuario está autenticado, redirigir a su dashboard
    if request.user.is_authenticated:
        destino = get_dashboard_url_for_user(request.user)
        if destino:
            return redirect(destino)
    
    # Si NO está autenticado, mostrar pantalla de descanso
    ahora = timezone.now()

    # Contar usuarios activos por grupo
    medicos_activos = User.objects.filter(
        groups__name='Medicos',
        is_active=True
    ).count()
    
    matronas_activas = User.objects.filter(
        groups__name='Matronas',
        is_active=True
    ).count()
    
    tens_activos = User.objects.filter(
        groups__name='TENS',
        is_active=True
    ).count()

    context = {
        "pacientes_activos": Paciente.objects.filter(activo=True).count(),
        "medicos_activos": medicos_activos,
        "matronas_activas": matronas_activas,
        "tens_activos": tens_activos,
        "fecha_actual": ahora.strftime("%d de %B de %Y"),
        "hora_actual": ahora.strftime("%H:%M"),
    }

    return render(request, "screensaver.html", context)