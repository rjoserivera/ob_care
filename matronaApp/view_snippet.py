
@login_required
@require_POST
def reenviar_pin(request, ficha_parto_id):
    """
    Reenvía el PIN al equipo médico (Telegram).
    """
    from ingresoPartoApp.models import FichaParto
    from gestionProcesosApp.pin_utils import enviar_pin_a_medicos
    
    ficha_parto = get_object_or_404(FichaParto, pk=ficha_parto_id)
    
    if not ficha_parto.pin_inicio_parto:
        return JsonResponse({'success': False, 'error': 'No hay PIN generado aún.'})

    try:
        enviar_pin_a_medicos(ficha_parto, ficha_parto.pin_inicio_parto)
        return JsonResponse({'success': True, 'message': 'PIN reenviado a los médicos.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
