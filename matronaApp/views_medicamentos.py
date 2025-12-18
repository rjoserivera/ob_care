

# ============================================
# API ADMINISTRACIÓN MEDICAMENTOS
# ============================================

@login_required
def obtener_administraciones(request, medicamento_id):
    """
    API para obtener el historial de administraciones de un medicamento
    URL: /services/api/treatment/<medicamento_id>/doses/
    """
    try:
        medicamento = get_object_or_404(MedicamentoFicha, id=medicamento_id)
        
        administraciones = AdministracionMedicamento.objects.filter(
            medicamento_ficha=medicamento
        ).order_by('-fecha_hora_administracion')[:20]
        
        data = {
            'administraciones': [{
                'id': adm.id,
                'fecha': adm.fecha_hora_administracion.strftime('%d/%m/%Y %H:%M'),
                'dosis': adm.dosis_administrada,
                'responsable': adm.tens.get_full_name() if adm.tens else 'Desconocido',
                'observaciones': adm.observaciones or ''
            } for adm in administraciones]
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def registrar_administracion(request, medicamento_id):
    """
    API para registrar una nueva administración de medicamento
    URL: /services/api/treatment/<medicamento_id>/administer/
    """
    try:
        medicamento = get_object_or_404(MedicamentoFicha, id=medicamento_id)
        
        data = json.loads(request.body)
        
        # Parse datetime
        fecha_str = data.get('fecha')  # "2025-12-17T22:30"
        fecha_dt = timezone.datetime.fromisoformat(fecha_str)
        if timezone.is_naive(fecha_dt):
            fecha_dt = timezone.make_aware(fecha_dt)
        
        # Crear administración
        AdministracionMedicamento.objects.create(
            medicamento_ficha=medicamento,
            tens=request.user,
            fecha_hora_administracion=fecha_dt,
            dosis_administrada=data.get('dosis'),
            se_realizo_lavado=data.get('lavado', False),
            observaciones=data.get('observaciones', ''),
            administrado_exitosamente=True
        )
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
