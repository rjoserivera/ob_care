from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Notificacion, PersonalTurno, AsignacionPersonal
from django.contrib import messages
from django.contrib.auth.models import User

@login_required
def mis_notificaciones(request):
    """Vista para que el personal vea sus notificaciones"""
    try:
        personal_turno = PersonalTurno.objects.filter(
            usuario=request.user
        ).first()
        
        # 1. Obtener asignaciones pendientes (URGENTES)
        asignaciones = []
        if personal_turno:
            asignaciones = AsignacionPersonal.objects.filter(
                personal=personal_turno,
                estado_respuesta='ENVIADA'
            ).select_related(
                'proceso__ficha_obstetrica__paciente__persona',
                'proceso__sala_asignada'
            ).order_by('-timestamp_notificacion')

        # 2. Obtener notificaciones generales (AVISOS)
        # Buscamos notificaciones donde el destinatario sea el turno actual del usuario
        # Ojo: si el turno cambia, el usuario podría perder notificaciones antiguas si solo filtramos por turno activo.
        # Pero Notificacion tiene FK a PersonalTurno.
        # Vamos a buscar todos los turnos del usuario o el turno especifico.
        # Por simplicidad y consistencia con los modelos:
        notificaciones = Notificacion.objects.filter(
            destinatario__usuario=request.user,
            estado__in=['ENVIADA', 'PENDIENTE']
        ).order_by('-timestamp_envio')
        
        return render(request, 'gestionProcesosApp/mis_notificaciones.html', {
            'asignaciones': asignaciones,
            'notificaciones': notificaciones,
            'personal_turno': personal_turno
        })
    except Exception as e:
        return render(request, 'gestionProcesosApp/mis_notificaciones.html', {
            'error': str(e),
            'asignaciones': [],
            'notificaciones': []
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
    API para verificar si hay nuevas notificaciones (Asignaciones) sin responder.
    Retorna JSON con count y timestamp de la última.
    """
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
            
        # 1. Buscar Notificaciones tradicionales (Sistema antiguo/Genérico)
        notificaciones = Notificacion.objects.filter(
            destinatario__usuario=request.user,
            estado__in=['ENVIADA', 'PENDIENTE']
        ).order_by('-timestamp_envio')
        
        count_notif = notificaciones.count()
        last_notif = notificaciones.first()
        
        # 2. Buscar Asignaciones de Parto (Sistema nuevo)
        # Obtener PersonalTurno
        personal = PersonalTurno.objects.filter(usuario=request.user).first()
        
        count_asig = 0
        last_asig = None
        
        if personal:
            asignaciones = AsignacionPersonal.objects.filter(
                personal=personal,
                estado_respuesta='ENVIADA'
            ).order_by('-timestamp_notificacion')
            count_asig = asignaciones.count()
            last_asig = asignaciones.first()
            
        # 3. Combinar resultados
        total_count = count_notif + count_asig
        
        last_notif_data = {
            'latest_id': None,
            'latest_timestamp': 0,
            'latest_title': "",
            'latest_msg': ""
        }
        
        # Determinar cuál es más reciente
        ts_notif = last_notif.timestamp_envio.timestamp() if last_notif else 0
        ts_asig = last_asig.timestamp_notificacion.timestamp() if (last_asig and last_asig.timestamp_notificacion) else 0
        
        if ts_asig > ts_notif:
             # Ganó Asignación
             last_notif_data = {
                'latest_id': f"asig_{last_asig.id}", # Prefijo para evitar colisión IDs
                'latest_timestamp': ts_asig,
                'latest_title': "URGENTE: Asistencia a Parto",
                'latest_msg': f"Paciente: {last_asig.proceso.ficha_obstetrica.paciente.persona.nombre_completo}. Sala: {last_asig.proceso.sala_asignada.nombre if last_asig.proceso.sala_asignada else 'Por asignar'}"
            }
        elif last_notif:
             # Ganó Notificación
             last_notif_data = {
                'latest_id': f"notif_{last_notif.id}",
                'latest_timestamp': ts_notif,
                'latest_title': last_notif.titulo,
                'latest_msg': last_notif.mensaje
            }
        
        data = {
            'count': total_count,
            'has_new': total_count > 0,
            **last_notif_data
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


@login_required
def marcar_notificacion_leida(request, notificacion_id):
    """
    API para marcar una notificación genérica como LEÍDA/VISTA
    """
    try:
        notificacion = get_object_or_404(Notificacion, pk=notificacion_id, destinatario__usuario=request.user)
        
        # Procesar respuesta si existe
        import json
        try:
            data = json.loads(request.body)
            mensaje = data.get('mensaje_respuesta', '')
            if mensaje:
                # Guardamos la respuesta del usuario en respuesta_servidor (o nuevo campo si existiera)
                # Formato: [FECHA] Usuario: Mensaje
                timestamp = timezone.now().strftime("%d/%m/%Y %H:%M")
                respuesta_texto = f"[{timestamp}] Respuesta User: {mensaje}"
                notificacion.respuesta_servidor = respuesta_texto
                
                # --- LÓGICA DE RESPUESTA AL ADMIN ---
                # Crear una notificación inversa para los administradores
                try:
                    destinatario_resp = None
                    
                    # 1. Buscar turno de ADMIN (Cualquier estado)
                    destinatario_resp = PersonalTurno.objects.filter(rol='ADMIN').order_by('-fecha_inicio_turno').first()
                    
                    # 2. Si no hay turno Admin, buscar un SUPERUSER y asociarle/crearle turno
                    if not destinatario_resp:
                        superuser = User.objects.filter(is_superuser=True).first()
                        if superuser:
                            # Buscar si ya tiene turno (aunque no sea rol ADMIN)
                            turno_su = PersonalTurno.objects.filter(usuario=superuser).first()
                            if turno_su:
                                destinatario_resp = turno_su
                            else:
                                # CREAR TURNO ADMIN AUTOMÁTICO
                                destinatario_resp = PersonalTurno.objects.create(
                                    usuario=superuser,
                                    rol='ADMIN',
                                    estado='DISPONIBLE',
                                    fecha_inicio_turno=timezone.now(),
                                    fecha_fin_turno=timezone.now() + timezone.timedelta(days=365)
                                )

                    # 3. Fallback: Matrona
                    if not destinatario_resp:
                         destinatario_resp = PersonalTurno.objects.filter(rol='MATRONA').order_by('-fecha_inicio_turno').first()

                    if destinatario_resp:
                        Notificacion.objects.create(
                            proceso=notificacion.proceso, 
                            destinatario=destinatario_resp,
                            tipo='AVISO', 
                            titulo=f"Respuesta de {request.user.get_full_name()}",
                            mensaje=f"El usuario respondió a su aviso: '{notificacion.titulo}'.\n\nRespuesta: {mensaje}",
                            estado='PENDIENTE',
                            timestamp_expiracion=timezone.now() + timezone.timedelta(days=2)
                        )
                    else:
                        print("DEBUG: CRÍTICO - No se encontró NINGÚN destinatario para la respuesta")
                except Exception as e:
                    print(f"Error enviando notificacion respuesta: {e}")
                # ------------------------------------
                except Exception as e:
                    print(f"Error enviando notificacion respuesta: {e}")
                # ------------------------------------

        except:
            pass # Si falla el json o no hay mensaje, seguimos

        notificacion.estado = 'VISTA' # O 'CONFIRMADA' si prefieres que desaparezca totalmente de "pendientes"
        notificacion.timestamp_vista = timezone.now()
        notificacion.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def panel_notificaciones_admin(request):
    """
    Panel para que el administrador envíe notificaciones manuales
    """
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a este panel.')
        return redirect('home')
        
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        titulo = request.POST.get('titulo')
        mensaje = request.POST.get('mensaje')
        tipo = request.POST.get('tipo', 'INGRESO')
        
        try:
            destinatario_user = User.objects.get(pk=user_id)
            
            # Buscar un turno para este usuario (el más reciente)
            turno = PersonalTurno.objects.filter(usuario=destinatario_user).order_by('-fecha_inicio_turno').first()
            
            if not turno:
                # Si no tiene turno, creamos uno "ficticio" o usamos uno muy antiguo solo para anclar la notificacion
                # O advertimos al admin
                messages.warning(request, f'El usuario {destinatario_user} no tiene turnos registrados. Se intentará crear uno temporal o fallará.')
                # Fallback: Create a dummy inactive shift just to link the notification if the model requires it
                # Assuming PersonalTurno is required for Notificacion
                # Let's create one if it doesn't exist? risky.
                # Actually, check models.py... Notificacion.destinatario is ForeignKey to PersonalTurno.
                # We MUST have a PersonalTurno.
                turno = PersonalTurno.objects.create(
                    usuario=destinatario_user,
                    rol='ADMIN' if destinatario_user.is_staff else 'MATRONA', # Default fallback
                    estado='AUSENTE',
                    fecha_inicio_turno=timezone.now(),
                    fecha_fin_turno=timezone.now()
                )
            
            # Necesitamos un proceso (FichaParto) para la notificación?
            # Model: proceso = models.ForeignKey(FichaParto, ...)
            # Esto es una limitante del modelo actual. Requiere un proceso.
            # Vamos a buscar un proceso dummy o el último proceso del sistema
            from ingresoPartoApp.models import FichaParto
            proceso = FichaParto.objects.order_by('-id').first()
            
            if not proceso:
                 messages.error(request, 'No se pueden enviar notificaciones porque no historial de partos (FichaParto) en el sistema para vincular.')
                 return redirect('gestion_procesos:panel_notificaciones_admin')

            Notificacion.objects.create(
                proceso=proceso, # Vinculamos al último solo por cumplir la FK
                destinatario=turno,
                tipo=tipo,
                titulo=titulo,
                mensaje=mensaje,
                estado='PENDIENTE',
                timestamp_expiracion=timezone.now() + timezone.timedelta(days=7)
            )
            messages.success(request, f'Notificación enviada a {destinatario_user.get_full_name()}')
            return redirect('gestion_procesos:panel_notificaciones_admin')
            
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
        except Exception as e:
            messages.error(request, f'Error al enviar: {e}')
    
    # Contexto GET
    usuarios = User.objects.filter(is_active=True).order_by('username')
    
    # Últimas enviadas (solo para feedback visual)
    ultimas = Notificacion.objects.order_by('-timestamp_envio')[:10]
    
    return render(request, 'gestionProcesosApp/panel_notificaciones_admin.html', {
        'usuarios': usuarios,
        'ultimas_notificaciones': ultimas
    })
