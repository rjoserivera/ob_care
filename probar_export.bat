@echo off
echo ========================================
echo   PROBAR VISTA DE EXPORTACION
echo ========================================
echo.

call venv\Scripts\activate.bat
python manage.py probar_exportacion

echo.
echo Presiona cualquier tecla para cerrar...
pause >nul
