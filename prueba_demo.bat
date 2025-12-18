@echo off
echo ========================================
echo   PRUEBA: 5 FICHAS DE DEMOSTRACION
echo ========================================
echo.

call venv\Scripts\activate.bat

echo.
echo Generando 5 fichas de prueba...
python manage.py generar_datos_demo --cantidad 5

echo.
pause
