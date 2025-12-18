@echo off
echo ========================================
echo   Actualizar Fichas Antiguas
echo ========================================
echo.
echo Este script marcara como "parto completado"
echo las fichas que tienen el proceso iniciado
echo pero no estan marcadas correctamente.
echo.

call venv\Scripts\activate.bat

python manage.py actualizar_fichas_antiguas

echo.
pause
