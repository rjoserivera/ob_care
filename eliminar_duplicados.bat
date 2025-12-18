@echo off
echo ========================================
echo   ELIMINAR GRUPOS DUPLICADOS
echo ========================================
echo.

echo [1/2] Activando entorno virtual...
call venv\Scripts\activate.bat

echo.
echo [2/2] Ejecutando script...
python manage.py eliminar_grupos_duplicados

echo.
echo ========================================
echo   PROCESO COMPLETADO
echo ========================================
echo.
pause
