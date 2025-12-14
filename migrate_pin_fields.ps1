# Crear migraciones para los nuevos campos
& "C:\Users\Bocchi\Desktop\ob_care\venv\Scripts\Activate.ps1"
python manage.py makemigrations gestionProcesosApp
python manage.py makemigrations ingresoPartoApp
python manage.py migrate
