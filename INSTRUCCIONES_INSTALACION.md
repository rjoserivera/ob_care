# 🚀 Guía de Instalación Rápida - Obstetric Care

Bienvenido al proyecto **Obstetric Care**. Esta guía te ayudará a configurar el entorno de base de datos y usuarios iniciales en un solo paso.

## 📋 Requisitos Previos

Asegúrate de tener instalado:
- **Python 3.8+**
- **pip** (Gestor de paquetes de Python)

---

## 🛠️ Pasos de Instalación

### 1. Activar Entorno Virtual
Antes de ejecutar cualquier comando, asegúrate de estar en tu entorno virtual.

**Windows:**
```bash
.\venv\Scripts\activate
```
**Mac/Linux:**
```bash
source venv/bin/activate
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Aplicar Migraciones
Crea las tablas en la base de datos (SQLite por defecto).
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. ⚡ Ejecutar Script de Configuración Inicial
Este script creará automáticamente los **Roles**, **Usuarios de Prueba** y **Catálogos** necesarios (Medicamentos, Consultorios, etc.).

```bash
python setup_project.py
```

Deberías ver una salida confirmando la creación de cada elemento.

---

## 🔑 Credenciales de Acceso
El script crea los siguientes usuarios por defecto para pruebas:

| Rol | Usuario | Contraseña |
|-----|---------|------------|
| **Administrador** | `admin` | `admin123` |
| **Matrona** | `matrona` | `matrona123` |
| **Médico** | `medico` | `medico123` |
| **TENS** | `tens` | `tens123` |

---

## 🏃‍♂️ Ejecutar el Proyecto
Una vez configurado, inicia el servidor:

```bash
python manage.py runserver
```

Accede a: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🆘 Solución de Problemas

- **Error "Table doesn't exist"**: Asegúrate de haber ejecutado `python manage.py migrate` antes del script de setup.
- **Error de dependencias**: Verifica que `requirements.txt` esté instalado correctamente.
