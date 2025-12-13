"""
Comando para probar envío de Telegram
"""
from django.core.management.base import BaseCommand
from gestionProcesosApp.telegram_utils import enviar_telegram

class Command(BaseCommand):
    help = 'Prueba el envío de Telegram'

    def handle(self, *args, **options):
        chat_id = '8420825600'
        mensaje = """
🧪 <b>PRUEBA DE TELEGRAM</b>

Este es un mensaje de prueba del sistema.

Si recibes esto, el Telegram está funcionando correctamente.
"""
        
        self.stdout.write('📤 Enviando mensaje de prueba...')
        
        resultado = enviar_telegram(chat_id, mensaje)
        
        if resultado:
            self.stdout.write(self.style.SUCCESS('✅ Mensaje enviado exitosamente'))
        else:
            self.stdout.write(self.style.ERROR('❌ Error al enviar mensaje'))
