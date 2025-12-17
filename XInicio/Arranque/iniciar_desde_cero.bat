@echo off
chcp 65001 > nul
echo ==================================================
echo 🚀 INICIANDO CARGA COMPLETA DEL SISTEMA (DESDE CERO)
echo ==================================================
echo.
echo 1. Limpiando sistema (Base de Datos y Migraciones)...
python XInicio/Arranque/clean_migrations.py

echo.
echo 2. Verificando entorno virtual...
if exist "..\..\venv\Scripts\activate.bat" (
    call ..\..\venv\Scripts\activate.bat
    echo    ✅ Entorno virtual activado.
) else (
    echo    ⚠️ No se encontró venv, usando Python del sistema.
)

echo.
echo 3. Instalando dependencias (requirements.txt)...
pushd "%~dp0..\.."
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Error instalando dependencias.
    pause
    exit /b
)
popd

echo.
echo 4. Creando Migraciones Iniciales...
pushd "%~dp0..\.."
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo ❌ Error en makemigrations.
    pause
    exit /b
)

echo.
echo 4. Aplicando migraciones (Base de Datos Nueva)...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ❌ Error en migraciones.
    pause
    exit /b
)

echo.
echo 3. Poblando Catálogos del Sistema (populate_full_system)...
python XInicio/Arranque/populate_full_system.py
if %errorlevel% neq 0 (
    echo ❌ Error poblando catálogos.
    pause
    exit /b
)

echo.
echo 4. Poblando Usuarios y Staff (populate_users)...
python XInicio/Arranque/populate_users.py
if %errorlevel% neq 0 (
    echo ❌ Error poblando usuarios.
    pause
    exit /b
)



echo.
echo 5. Iniciando Turnos Activos (start_all_shifts)...
python XInicio/Arranque/start_all_shifts.py
if %errorlevel% neq 0 (
    echo ❌ Error iniciando turnos.
    pause
    exit /b
)

echo.
echo 6. Poblando Personas Generales (100) (populate_personas)...
python XInicio/Arranque/populate_personas.py
if %errorlevel% neq 0 (
    echo ❌ Error poblando personas.
    pause
    exit /b
)

echo.
echo ==================================================
echo ✨ PROCESO FINALIZADO CON ÉXITO ✨
echo ==================================================
echo Ahora puedes iniciar el servidor con: 
echo python manage.py runserver
echo.
REM Para iniciar el servidor manualmente usa:
REM python manage.py runserver
pause
