@echo off
echo ========================================
echo   ELIMINAR ADMINISTRATOR (INGLES)
echo ========================================
echo.

call venv\Scripts\activate.bat
python manage.py eliminar_administrator_ingles

echo.
echo Listo! Presiona cualquier tecla para cerrar...
pause >nul
