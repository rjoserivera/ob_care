from django.shortcuts import render, redirect
from django.utils import timezone

from gestionApp.models import Paciente, Medico, Matrona, Tens
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

    context = {
        "pacientes_activos": Paciente.objects.filter(activo=True).count(),
        "medicos_activos": Medico.objects.filter(Activo=True).count(),
        "matronas_activas": Matrona.objects.filter(Activo=True).count(),
        "tens_activos": Tens.objects.filter(Activo=True).count(),
        "fecha_actual": ahora.strftime("%d de %B de %Y"),
        "hora_actual": ahora.strftime("%H:%M"),
    }

    return render(request, "screensaver.html", context)