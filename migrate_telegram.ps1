# Activar entorno virtual y crear migración
& "C:\Users\Bocchi\Desktop\ob_care\venv\Scripts\Activate.ps1"
python manage.py makemigrations gestionApp
python manage.py migrate gestionApp
