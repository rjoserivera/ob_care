# 🎭 Gestión de Usuarios y Roles - Guía Rápida

## 🚀 Inicio Rápido

### Opción 1: Script PowerShell (Windows) - MÁS FÁCIL ⭐

```powershell
.\gestionar_usuarios.ps1
```

Este script interactivo te guiará por todas las opciones disponibles.

---

### Opción 2: Comando Django Interactivo

```bash
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Ejecutar script interactivo
python manage.py gestionar_usuarios_roles
```

---

### Opción 3: Comandos Directos

```bash
# Crear grupos del sistema (HACER PRIMERO)
python manage.py crear_grupos_sistema

# Crear usuarios iniciales con datos completos
python manage.py crear_usuarios_iniciales

# Listar usuarios
python manage.py gestionar_usuarios_roles --listar todos
python manage.py gestionar_usuarios_roles --listar medico
python manage.py gestionar_usuarios_roles --listar matrona
```

---

## 📋 Roles Disponibles

- **Administrador** - Acceso completo al sistema
- **Médico** - Gestión de pacientes y fichas médicas
- **Matrona** - Gestión de fichas obstétricas
- **TENS** - Registro de signos vitales
- **Paciente** - Usuario de consulta

---

## 🔑 Usuarios por Defecto

Después de ejecutar `crear_usuarios_iniciales`:

| Username | Password | Rol |
|----------|----------|-----|
| admin | pass123 | Administrador |
| medico | pass123 | Médico |
| matrona | pass123 | Matrona |
| tens | pass123 | TENS |

---

## 📖 Documentación Completa

Ver documentación detallada en: **[docs/GUIA_USUARIOS_ROLES.md](docs/GUIA_USUARIOS_ROLES.md)**

---

## 🎯 Casos de Uso Comunes

### Crear un nuevo médico

```bash
python manage.py gestionar_usuarios_roles
# Selecciona opción 1 (Crear usuario)
# Sigue las instrucciones en pantalla
```

### Listar todos los médicos

```bash
python manage.py gestionar_usuarios_roles --listar medico
```

### Cambiar contraseña

```bash
python manage.py gestionar_usuarios_roles
# Selecciona opción 4 (Cambiar contraseña)
```

### Crear usuarios de prueba

```bash
python manage.py gestionar_usuarios_roles
# Selecciona opción 7 (Crear usuarios masivos)
```

---

## 🛠️ Scripts Disponibles

1. **`gestionar_usuarios.ps1`** - Script PowerShell con menú interactivo (Windows)
2. **`python manage.py gestionar_usuarios_roles`** - Comando Django interactivo
3. **`python manage.py crear_usuarios_iniciales`** - Crear usuarios base del sistema
4. **`python manage.py crear_grupos_sistema`** - Crear grupos de roles
5. **`scripts/crear_usuarios_rapido.py`** - Funciones para Django shell

---

## ⚠️ Importante

1. **Siempre ejecuta `crear_grupos_sistema` PRIMERO**
2. Las contraseñas por defecto son para desarrollo - **cámbialas en producción**
3. Los usuarios demo son solo para pruebas

---

## 🆘 Ayuda

Si tienes problemas, consulta la [documentación completa](docs/GUIA_USUARIOS_ROLES.md) o contacta al equipo de desarrollo.
