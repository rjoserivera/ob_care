@echo off
call venv\Scripts\activate.bat
python test_generar.py > debug_output.txt 2>&1
type debug_output.txt
pause
