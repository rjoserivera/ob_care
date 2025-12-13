"""
Vista simplificada para invitar personal por rol
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db import transaction
import json

from ingresoPartoApp.models import FichaParto
from gestionProcesosApp.models import PersonalTurno, Notificacion, AsignacionPersonal
from gestionProcesosApp.telegram_utils import enviar_notificacion_parto


@login_required
@require_POST
def invitar_personal_rol(request, ficha_parto_id):
    """
    Invita a TODO el personal disponible de un rol específico
    """
    try:
        data = json.loads(request.body)
        rol = data.get('rol')
        
        if not rol:
            return JsonResponse({'success': False, 'error': 'Rol no especificado'})
        
        ficha_parto = get_object_or_404(FichaParto, pk=ficha_parto_id)
        
        # Obtener personal disponible del rol
        now = timezone.now()
        personal_disponible = PersonalTurno.objects.filter(
            rol=rol,
            estado='DISPONIBLE',
            fecha_fin_turno__gte=now
        ).select_related('usuario', 'usuario__perfil')
        
        enviados = 0
        ya_invitados = 0
        errores = 0
        
        for personal in personal_disponible:
            try:
                # Verificar si ya fue invitado
                existe = AsignacionPersonal.objects.filter(
                    proceso=ficha_parto,
                    personal=personal
                ).exists()
                
                if existe:
                    ya_invitados += 1
                    continue
                
                with transaction.atomic():
                    # Crear asignación
                    asignacion = AsignacionPersonal.objects.create(
                        proceso=ficha_parto,
                        personal=personal,
                        rol_en_proceso=rol,
                        observaciones='Invitación automática desde Centro de Control'
                    )
                    
                    # Crear notificación
                    Notificacion.objects.create(
                        proceso=ficha_parto,
                        destinatario=personal,
                        tipo='PARTO',
                        titulo='URGENTE: Asistencia a Parto',
                        mensaje=f"Se requiere su presencia inmediata. Ficha {ficha_parto.numero_ficha_parto}. Paciente: {ficha_parto.ficha_obstetrica.paciente.persona.nombre_completo}.",
                        estado='ENVIADA',
                        timestamp_expiracion=timezone.now() + timezone.timedelta(hours=4)
                    )
                    
                    # Enviar Telegram
                    try:
                        telegram_ok = enviar_notificacion_parto(personal, ficha_parto)
                        if telegram_ok:
                            print(f"✅ Telegram enviado a {personal.usuario.get_full_name()}")
                        else:
                            print(f"⚠️ Telegram NO enviado a {personal.usuario.get_full_name()}")
                    except Exception as e:
                        print(f"❌ Error Telegram: {e}")
                    
                    enviados += 1
                    
            except Exception as e:
                print(f"❌ Error procesando {personal.usuario.get_full_name()}: {e}")
                errores += 1
        
        return JsonResponse({
            'success': True,
            'message': 'Invitaciones enviadas correctamente',
            'enviados': enviados,
            'ya_invitados': ya_invitados,
            'errores': errores
        })
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
