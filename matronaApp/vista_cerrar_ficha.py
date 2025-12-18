
# ============================================
# VISTA: CERRAR FICHA DEFINITIVAMENTE
# ============================================

@login_required
@require_POST
@decrypt_url_params('ficha_pk')
def cerrar_ficha_definitivamente(request, ficha_pk):
    """
    Cerrar definitivamente una ficha obstétrica
    Solo disponible después de completar el parto
    URL: /services/case/<ficha_pk>/close/
    """
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk)
    
    # Validar que el parto esté completado
    if not ficha.parto_completado:
        messages.error(request, 'No se puede cerrar la ficha sin completar el parto')
        return redirect('matrona:detalle_ficha', ficha_pk=encrypt_id(ficha.pk))
    
    # Validar que no esté ya cerrada
    if ficha.ficha_cerrada:
        messages.warning(request, 'Esta ficha ya está cerrada')
        return redirect('matrona:detalle_ficha', ficha_pk=encrypt_id(ficha.pk))
    
    # Cerrar ficha
    ficha.ficha_cerrada = True
    ficha.activa = False
    ficha.fecha_cierre = timezone.now()
    ficha.usuario_cierre = request.user
    ficha.save()
    
    messages.success(request, 'Ficha obstétrica cerrada exitosamente. La ficha ahora está en modo solo lectura.')
    return redirect('matrona:historial_partos')
