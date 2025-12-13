"""
Utilidad para enviar notificaciones por Telegram
"""
import requests
from django.conf import settings

def enviar_telegram(chat_id, mensaje):
    """
    Envía un mensaje de Telegram a un usuario específico
    
    Args:
        chat_id: ID de chat de Telegram del usuario
        mensaje: Texto del mensaje a enviar
    
    Returns:
        bool: True si se envió correctamente, False en caso contrario
    """
    try:
        token = settings.TELEGRAM_BOT_TOKEN
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        
        data = {
            'chat_id': chat_id,
            'text': mensaje,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Telegram enviado a chat_id: {chat_id}")
            return True
        else:
            print(f"❌ Error Telegram: {response.text}")
            return False
            
    except Exception as e:
        print(f"⚠️ Error enviando Telegram: {e}")
        return False


def enviar_notificacion_parto(personal, ficha_parto):
    """
    Envía notificación de parto por Telegram
    
    Args:
        personal: Objeto PersonalTurno
        ficha_parto: Objeto FichaParto
    """
    # Verificar si el usuario tiene perfil y Telegram configurado
    if not hasattr(personal.usuario, 'perfil'):
        print(f"⚠️ {personal.usuario.get_full_name()} no tiene perfil")
        return False
        
    if not personal.usuario.perfil.telegram_chat_id:
        print(f"⚠️ {personal.usuario.get_full_name()} no tiene Telegram configurado")
        return False
    
    mensaje = f"""
🚨 <b>URGENTE: Solicitud de Asistencia</b>

<b>Paciente:</b> {ficha_parto.ficha_obstetrica.paciente.persona.nombre_completo}
<b>Ficha:</b> {ficha_parto.numero_ficha_parto}

Se requiere su presencia INMEDIATA en la Sala de Parto (Preparación).

Por favor, confirme su asistencia en el sistema o acuda directamente.
"""
    
    return enviar_telegram(personal.usuario.perfil.telegram_chat_id, mensaje)
