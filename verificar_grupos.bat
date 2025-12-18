@echo off
echo ========================================
echo   VERIFICAR Y LIMPIAR GRUPOS
echo ========================================
echo.

echo [1/2] Activando entorno virtual...
call venv\Scripts\activate.bat

echo.
echo [2/2] Ejecutando verificacion...
python manage.py verificar_grupos

echo.
pause
