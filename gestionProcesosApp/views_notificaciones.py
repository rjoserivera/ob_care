"""
Vista para obtener notificaciones del personal
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from gestionProcesosApp.models import PersonalTurno, AsignacionPersonal


@login_required
def obtener_notificaciones_ajax(request):
    """
    Obtiene las notificaciones pendientes del usuario actual (AJAX)
    """
    try:
        # Obtener PersonalTurno del usuario
        personal = PersonalTurno.objects.filter(usuario=request.user).first()
        
        if not personal:
            return JsonResponse({'notificaciones': [], 'count': 0})
        
        # Obtener asignaciones pendientes
        asignaciones = AsignacionPersonal.objects.filter(
            personal=personal,
            estado_respuesta='ENVIADA'
        ).select_related(
            'proceso__ficha_obstetrica__paciente__persona',
            'proceso__sala_asignada'
        ).order_by('-timestamp_notificacion')
        
        notificaciones = []
        for asig in asignaciones:
            notificaciones.append({
                'id': asig.id,
                'ficha': asig.proceso.numero_ficha_parto,
                'paciente': asig.proceso.ficha_obstetrica.paciente.persona.nombre_completo,
                'sala': asig.proceso.sala_asignada.nombre if asig.proceso.sala_asignada else 'Sin asignar',
                'rol': asig.rol_en_proceso,
                'timestamp': asig.timestamp_notificacion.strftime('%H:%M'),
                'fecha': asig.timestamp_notificacion.strftime('%d/%m/%Y')
            })
        
        return JsonResponse({
            'notificaciones': notificaciones,
            'count': len(notificaciones)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def pagina_notificaciones(request):
    """
    Página dedicada para ver todas las notificaciones
    """
    # Obtener PersonalTurno del usuario
    personal = PersonalTurno.objects.filter(usuario=request.user).first()
    
    notificaciones = []
    if personal:
        asignaciones = AsignacionPersonal.objects.filter(
            personal=personal,
            estado_respuesta='ENVIADA'
        ).select_related(
            'proceso__ficha_obstetrica__paciente__persona',
            'proceso__sala_asignada'
        ).order_by('-timestamp_notificacion')
        
        for asig in asignaciones:
            notificaciones.append({
                'id': asig.id,
                'ficha': asig.proceso.numero_ficha_parto,
                'paciente': asig.proceso.ficha_obstetrica.paciente.persona.nombre_completo,
                'sala': asig.proceso.sala_asignada.nombre if asig.proceso.sala_asignada else 'Sin asignar',
                'rol': asig.rol_en_proceso,
                'timestamp': asig.timestamp_notificacion,
                'observaciones': asig.observaciones
            })
    
    return render(request, 'notificaciones.html', {
        'notificaciones': notificaciones,
        'total': len(notificaciones)
    })
