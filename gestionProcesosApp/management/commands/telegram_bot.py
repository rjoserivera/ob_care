"""
Bot de Telegram para obtener el Chat ID de los usuarios
Ejecutar con: python manage.py telegram_bot
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import time

class Command(BaseCommand):
    help = 'Inicia el bot de Telegram para que los usuarios obtengan su Chat ID'

    def handle(self, *args, **options):
        token = settings.TELEGRAM_BOT_TOKEN
        
        if token == 'PEGA_AQUI_EL_TOKEN_DE_BOTFATHER':
            self.stdout.write(self.style.ERROR('❌ Debes configurar TELEGRAM_BOT_TOKEN en settings.py'))
            return
        
        self.stdout.write(self.style.SUCCESS('🤖 Bot de Telegram iniciado'))
        self.stdout.write(self.style.SUCCESS('📱 Los usuarios deben:'))
        self.stdout.write('   1. Buscar el bot en Telegram')
        self.stdout.write('   2. Enviar el comando /start')
        self.stdout.write('   3. Copiar su Chat ID')
        self.stdout.write('   4. Agregarlo en su perfil del sistema')
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('Presiona Ctrl+C para detener'))
        self.stdout.write('')
        
        offset = 0
        
        try:
            while True:
                # Obtener actualizaciones
                url = f"https://api.telegram.org/bot{token}/getUpdates"
                params = {'offset': offset, 'timeout': 30}
                
                try:
                    response = requests.get(url, params=params, timeout=35)
                    data = response.json()
                    
                    if data.get('ok'):
                        for update in data.get('result', []):
                            offset = update['update_id'] + 1
                            
                            if 'message' in update:
                                message = update['message']
                                chat_id = message['chat']['id']
                                text = message.get('text', '')
                                username = message['from'].get('username', 'Sin username')
                                first_name = message['from'].get('first_name', '')
                                
                                if text == '/start':
                                    # Enviar mensaje con el Chat ID
                                    send_url = f"https://api.telegram.org/bot{token}/sendMessage"
                                    send_data = {
                                        'chat_id': chat_id,
                                        'text': f"""
✅ <b>¡Conectado con éxito!</b>

Tu Chat ID es: <code>{chat_id}</code>

<b>Pasos siguientes:</b>
1. Copia el número de arriba
2. Ve al sistema web
3. Entra a tu perfil
4. Pega el Chat ID en el campo "Telegram"
5. Guarda los cambios

Ahora recibirás notificaciones urgentes aquí.
""",
                                        'parse_mode': 'HTML'
                                    }
                                    requests.post(send_url, data=send_data)
                                    
                                    self.stdout.write(self.style.SUCCESS(
                                        f'✅ Usuario conectado: {first_name} (@{username}) - Chat ID: {chat_id}'
                                    ))
                    
                except requests.exceptions.Timeout:
                    continue
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error: {e}'))
                    time.sleep(5)
                    
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\n\n👋 Bot detenido'))
