from django.shortcuts import render, redirect
from django.utils import timezone

from gestionApp.models import Paciente, Medico, Matrona, Tens
from authentication.utils import get_dashboard_url_for_user


def home(request):
    if request.user.is_authenticated:
        destino = get_dashboard_url_for_user(request.user)
        if destino:
            return redirect(destino)

    ahora = timezone.now()

    context = {
        "pacientes_activos": Paciente.objects.filter(Activo=True).count(),
        "medicos_activos": Medico.objects.filter(Activo=True).count(),
        "matronas_activas": Matrona.objects.filter(Activo=True).count(),
        "tens_activos": Tens.objects.filter(Activo=True).count(),
        "fecha_actual": ahora.strftime("%d de %B de %Y"),
        "hora_actual": ahora.strftime("%H:%M"),
    }

    return render(request, "inicio/home.html", context)
