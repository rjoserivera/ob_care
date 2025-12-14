"""
Utilidades para el sistema de PIN de inicio de parto
"""
import random
import string
from django.utils import timezone


def generar_pin(longitud=6):
    """
    Genera un PIN numérico aleatorio
    
    Args:
        longitud: Longitud del PIN (default: 6)
    
    Returns:
        str: PIN numérico
    """
    return ''.join(random.choices(string.digits, k=longitud))


def equipo_completo(ficha_parto):
    """
    Verifica si el equipo requerido está completo y aceptado
    
    Args:
        ficha_parto: Instancia de FichaParto
    
    Returns:
        bool: True si el equipo está completo
    """
    from gestionProcesosApp.models import AsignacionPersonal
    
    # Calcular requerimientos
    cantidad_bebes = ficha_parto.bebes_esperados.count()
    if cantidad_bebes < 1: 
        cantidad_bebes = 1 # Fallback
        
    medicos_requeridos = cantidad_bebes * 1
    matronas_requeridas = cantidad_bebes * 2
    tens_requeridos = cantidad_bebes * 3
    
    # Contar aceptados
    asignaciones_aceptadas = AsignacionPersonal.objects.filter(
        proceso=ficha_parto,
        estado_respuesta='ACEPTADA'
    )
    
    medicos_aceptados = asignaciones_aceptadas.filter(personal__rol='MEDICO').count()
    matronas_aceptadas = asignaciones_aceptadas.filter(personal__rol='MATRONA').count()
    tens_aceptados = asignaciones_aceptadas.filter(personal__rol='TENS').count()
    
    return (medicos_aceptados >= medicos_requeridos and
            matronas_aceptadas >= matronas_requeridas and
            tens_aceptados >= tens_requeridos)


def enviar_pin_a_medicos(ficha_parto, pin):
    """
    Envía el PIN por Telegram solo a médicos que aceptaron
    
    Args:
        ficha_parto: Instancia de FichaParto
        pin: PIN generado
    """
    from gestionProcesosApp.models import AsignacionPersonal
    from gestionProcesosApp.telegram_utils import enviar_telegram
    
    medicos_aceptados = AsignacionPersonal.objects.filter(
        proceso=ficha_parto,
        estado_respuesta='ACEPTADA',
        personal__rol='MEDICO'
    )
    
    for asignacion in medicos_aceptados:
        try:
            if (hasattr(asignacion.personal.usuario, 'perfil') and 
                asignacion.personal.usuario.perfil.telegram_chat_id):
                
                mensaje = f"""
🔐 <b>PIN DE INICIO DE PARTO</b>

<b>Paciente:</b> {ficha_parto.ficha_obstetrica.paciente.persona.nombre_completo}
<b>Ficha:</b> {ficha_parto.numero_ficha_parto}

<b>PIN:</b> <code>{pin}</code>

Ingrese este PIN en el sistema para iniciar el proceso de parto.

⚠️ <i>Este PIN es confidencial y solo debe ser compartido con el equipo médico autorizado.</i>
"""
                enviar_telegram(asignacion.personal.usuario.perfil.telegram_chat_id, mensaje)
                print(f"📱 PIN enviado a Dr. {asignacion.personal.usuario.get_full_name()}")
        except Exception as e:
            print(f"⚠️ Error enviando PIN a {asignacion.personal.usuario.get_full_name()}: {e}")
