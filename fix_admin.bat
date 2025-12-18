@echo off
echo ========================================
echo   ELIMINAR ADMINISTRADOR DUPLICADO
echo ========================================
echo.

call venv\Scripts\activate.bat
python manage.py fix_admin_duplicado

echo.
echo Listo! Presiona cualquier tecla para cerrar...
pause >nul
