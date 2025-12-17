@echo off
title ObCare - Telegram Bot
color 0A

echo ==================================================
echo      INICIANDO BOT DE TELEGRAM - OBSTETRIC CARE
echo ==================================================
echo.

:: 1. Activar Entorno Virtual (si existe carpeta venv)
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Activando entorno virtual...
    call venv\Scripts\activate.bat
) else (
    echo [INFO] No se encontro entorno virtual (venv), usando Python global...
)

:: 2. Ejecutar el Bot
echo [INFO] Ejecutando comando: python manage.py telegram_bot
echo.
python manage.py telegram_bot

:: 3. Pausa final por si ocurre un error
echo.
echo ==================================================
echo      EL BOT SE HA DETENIDO
echo ==================================================
pause
