# Script para iniciar el servidor completo
# Ejecutar con: .\start_server.ps1

Write-Host "🚀 Iniciando Sistema Obstétrico..." -ForegroundColor Green

# Activar entorno virtual
& "C:\Users\Bocchi\Desktop\ob_care\venv\Scripts\Activate.ps1"

# Iniciar servidor
Write-Host "🌐 Servidor web iniciado en http://0.0.0.0:8000" -ForegroundColor Cyan
Write-Host "📱 Notificaciones de Telegram: ACTIVAS" -ForegroundColor Green
Write-Host "" 
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow

python manage.py runserver 0.0.0.0:8000
