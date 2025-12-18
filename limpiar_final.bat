@echo off
echo ========================================
echo   LIMPIEZA FINAL DE GRUPOS
echo ========================================
echo.

call venv\Scripts\activate.bat
python manage.py limpiar_grupos_final

echo.
echo Presiona cualquier tecla para cerrar...
pause >nul
