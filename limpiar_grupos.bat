@echo off
echo ========================================
echo   LIMPIAR GRUPOS NO OFICIALES
echo ========================================
echo.

call venv\Scripts\activate.bat
python manage.py limpiar_grupos_no_oficiales

echo.
echo Listo! Presiona cualquier tecla para cerrar...
pause >nul
