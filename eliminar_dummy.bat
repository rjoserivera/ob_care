@echo off
echo ========================================
echo   ELIMINAR USUARIO DUMMY MATRONA
echo ========================================
echo.

call venv\Scripts\activate.bat
python manage.py eliminar_dummy_matrona

echo.
echo Listo! Presiona cualquier tecla para cerrar...
pause >nul
