@echo off
echo ========================================
echo   MIGRACION: Campos de Cierre de Ficha
echo ========================================
echo.

echo [1/3] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno virtual
    pause
    exit /b 1
)

echo.
echo [2/3] Creando migracion...
python manage.py makemigrations matronaApp --name add_closure_fields
if errorlevel 1 (
    echo ERROR: No se pudo crear la migracion
    pause
    exit /b 1
)

echo.
echo [3/3] Aplicando migracion...
python manage.py migrate matronaApp
if errorlevel 1 (
    echo ERROR: No se pudo aplicar la migracion
    pause
    exit /b 1
)

echo.
echo ========================================
echo   MIGRACION COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo Los siguientes campos fueron agregados:
echo   - parto_completado
echo   - ficha_cerrada
echo   - fecha_cierre
echo   - usuario_cierre
echo.
echo Presiona cualquier tecla para cerrar...
pause >nul
