@echo off
echo ========================================
echo   GENERAR DATOS DE DEMOSTRACION 2025
echo ========================================
echo.
echo Este script generara aproximadamente 100 fichas
echo con datos del año 2025 para la demostracion.
echo.
echo ADVERTENCIA: Esto agregara datos a la base de datos.
echo.
pause

echo.
echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo.
echo Generando datos...
python manage.py generar_datos_demo --cantidad 100

echo.
echo ========================================
echo   GENERACION COMPLETADA
echo ========================================
echo.
pause
