"""
Vista AJAX para limpiar invitaciones
"""
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from ingresoPartoApp.models import FichaParto
from gestionProcesosApp.models import AsignacionPersonal


@login_required
@require_POST
def limpiar_invitaciones_ajax(request, ficha_parto_id):
    """
    Limpia todas las invitaciones de una ficha de parto vía AJAX
    """
    try:
        ficha_parto = get_object_or_404(FichaParto, pk=ficha_parto_id)
        
        # Eliminar SOLO asignaciones pendientes (ENVIADA)
        # Respetamos las ACEPTADA y RECHAZADA
        asignaciones = AsignacionPersonal.objects.filter(
            proceso=ficha_parto,
            estado_respuesta='ENVIADA'
        )
        count = asignaciones.count()
        asignaciones.delete()
        
        return JsonResponse({
            'success': True,
            'eliminados': count,
            'message': f'Se limpiaron {count} invitaciones pendientes. Puede volver a invitar.'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
