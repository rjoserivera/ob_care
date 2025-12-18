@echo off
call venv\Scripts\activate.bat
python manage.py generar_datos_demo --cantidad 100
pause
