from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Notificacion, PersonalTurno, AsignacionPersonal
from django.contrib import messages

@login_required
def mis_notificaciones(request):
    """Vista para que el personal vea sus notificaciones"""
    try:
        personal_turno = PersonalTurno.objects.filter(
            usuario=request.user
        ).first()
        
        # Obtener asignaciones pendientes
        asignaciones = []
        if personal_turno:
            asignaciones = AsignacionPersonal.objects.filter(
                personal=personal_turno,
                estado_respuesta='ENVIADA'
            ).select_related(
                'proceso__ficha_obstetrica__paciente__persona',
                'proceso__sala_asignada'
            ).order_by('-timestamp_notificacion')
        
        return render(request, 'gestionProcesosApp/mis_notificaciones.html', {
            'asignaciones': asignaciones,
            'personal_turno': personal_turno
        })
    except Exception as e:
        return render(request, 'gestionProcesosApp/mis_notificaciones.html', {
            'error': str(e),
            'asignaciones': []
        })

@login_required
def crear_notificacion_prueba(request):
    """Crea una notificación dummy para el usuario actual para probar el sistema"""
    try:
        # Buscar CUALQUIER turno del usuario (incluso, crear uno dummy si falta, pero asumamos que tiene por seed)
        turno = PersonalTurno.objects.filter(usuario=request.user).first()
        if not turno:
            messages.error(request, 'No tienes ningún turno registrado (ni histórico).')
            return redirect('gestion_procesos:mis_notificaciones')
            
        # Crear notificación sin proceso real (hack: buscar un proceso dummy o dejarlo null si modelo permite... modelo no permite null en proceso)
        # Buscar cualquier FichaParto
        from ingresoPartoApp.models import FichaParto
        proceso = FichaParto.objects.last()
        
        if not proceso:
             messages.error(request, 'No hay procesos de parto en el sistema para vincular la prueba.')
             return redirect('gestion_procesos:mis_notificaciones')

        Notificacion.objects.create(
            proceso=proceso,
            destinatario=turno,
            tipo='URGENCIA',
            titulo='PRUEBA DE SISTEMA',
            mensaje=f'Esta es una notificación de prueba generada a las {timezone.now().strftime("%H:%M:%S")}. Si lees esto, tu celular está conectado correctamente.',
            estado='ENVIADA',
            timestamp_expiracion=timezone.now() + timezone.timedelta(hours=1)
        )
        messages.success(request, 'Notificación de prueba enviada.')
    except Exception as e:
        messages.error(request, f'Error creando prueba: {e}')
        
    return redirect('gestion_procesos:mis_notificaciones')

from django.http import JsonResponse

@login_required
def check_nuevas_notificaciones(request):
    """
    API para verificar si hay nuevas notificaciones sin leer.
    Retorna JSON con count y timestamp de la última.
    """
    try:
        # Filtramos notificaciones del usuario actual que NO han sido vistas (o confirmadas)
        # Check if user is authenticated (decorator handles it but good practice)
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
            
        notificaciones = Notificacion.objects.filter(
            destinatario__usuario=request.user,
            estado__in=['ENVIADA', 'PENDIENTE']
        ).order_by('-timestamp_envio')
        
        count = notificaciones.count()
        last_notif = notificaciones.first()
        
        data = {
            'count': count,
            'has_new': count > 0,
            'latest_id': last_notif.id if last_notif else None,
            'latest_timestamp': last_notif.timestamp_envio.timestamp() if last_notif else 0,
            'latest_title': last_notif.titulo if last_notif else "",
            'latest_msg': last_notif.mensaje if last_notif else ""
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def confirmar_asistencia(request, notificacion_id):
    """
    API para confirmar asistencia desde la notificación
    """
    try:
        notificacion = get_object_or_404(Notificacion, pk=notificacion_id, destinatario__usuario=request.user)
        
        # 1. Update Notification
        notificacion.estado = 'CONFIRMADA'
        notificacion.timestamp_confirmacion = timezone.now()
        notificacion.save()
        
        # 2. Update Assignment
        # Assuming One-to-One relationship via process + user, or explicit link.
        # The model AsignacionPersonal links Process + Personal. Notificacion links Process + Personal.
        # So check AsignacionPersonal for same process and personal
        asignacion = AsignacionPersonal.objects.filter(
            proceso=notificacion.proceso,
            personal=notificacion.destinatario
        ).first()

        if asignacion:
            asignacion.confirmo_asistencia = True
            asignacion.timestamp_confirmacion = timezone.now()
            asignacion.save()
            return JsonResponse({'success': True, 'msg': 'Asistencia confirmada'})
        else:
            return JsonResponse({'success': False, 'msg': 'Asignación no encontrada'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
