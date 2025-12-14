# 📋 Guía de Gestión de Usuarios y Roles - OB Care

Esta guía describe cómo usar los scripts de gestión de usuarios y roles en el sistema OB Care.

## 📚 Índice

1. [Roles del Sistema](#roles-del-sistema)
2. [Comandos Disponibles](#comandos-disponibles)
3. [Guía de Uso](#guía-de-uso)
4. [Ejemplos Prácticos](#ejemplos-prácticos)
5. [Scripts Disponibles](#scripts-disponibles)

---

## 🎭 Roles del Sistema

El sistema maneja 5 roles principales:

| Rol | Descripción | Dashboard |
|-----|-------------|-----------|
| **Administrador** | Acceso completo al sistema | `/auth/dashboard/admin/` |
| **Médico** | Gestión de pacientes y fichas médicas | `/auth/dashboard/medico/` |
| **Matrona** | Gestión de fichas obstétricas | `/matrona/menu/` |
| **TENS** | Registro de signos vitales | `/auth/dashboard/tens/` |
| **Paciente** | Usuario de consulta (limitado) | - |

---

## 🛠️ Comandos Disponibles

### 1. Crear Grupos del Sistema

Crea los 5 grupos básicos del sistema:

```bash
python manage.py crear_grupos_sistema
```

**Salida esperada:**
```
✓ Grupo "Médico" creado
✓ Grupo "Matrona" creado
✓ Grupo "TENS" creado
✓ Grupo "Paciente" creado
✓ Grupo "Administrador" creado
```

---

### 2. Crear Usuarios Iniciales

Crea usuarios de prueba con todos los datos completos (Persona + perfil específico):

```bash
python manage.py crear_usuarios_iniciales
```

**Usuarios creados:**
| Username | Contraseña | Rol |
|----------|-----------|-----|
| Bocchi | Bocchi | Administrador (superuser) |
| medico | Bocchi | Médico |
| matrona | Bocchi | Matrona |
| tens | Bocchi | TENS |

**Además:** 3 pacientes de prueba

---

### 3. Gestionar Usuarios y Roles (INTERACTIVO) ⭐

**Este es el script principal** - Modo interactivo completo:

```bash
python manage.py gestionar_usuarios_roles
```

#### Menú Principal:

```
╔═══════════════════════════════════════════════════════════╗
║                    MENÚ PRINCIPAL                         ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  1️⃣  Crear nuevo usuario                                 ║
║  2️⃣  Asignar/Remover rol a usuario existente             ║
║  3️⃣  Listar usuarios                                      ║
║  4️⃣  Cambiar contraseña                                   ║
║  5️⃣  Activar/Desactivar usuario                           ║
║  6️⃣  Eliminar usuario                                     ║
║  7️⃣  Crear usuarios masivos (demo)                        ║
║  8️⃣  Crear grupos del sistema                             ║
║  0️⃣  Salir                                                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

#### Uso con argumentos:

```bash
# Listar todos los usuarios
python manage.py gestionar_usuarios_roles --listar todos

# Listar solo médicos
python manage.py gestionar_usuarios_roles --listar medico

# Listar matronas
python manage.py gestionar_usuarios_roles --listar matrona

# Asignar rol directamente
python manage.py gestionar_usuarios_roles --username juan --rol Medico
```

---

### 4. Crear Usuarios Realistas

Crea usuarios con datos más realistas:

```bash
python manage.py crear_usuarios_realistas
```

---

## 📖 Guía de Uso

### Paso 1: Configuración Inicial

```bash
# 1. Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# 2. Crear grupos del sistema
python manage.py crear_grupos_sistema

# 3. Crear usuarios iniciales (opcional)
python manage.py crear_usuarios_iniciales
```

### Paso 2: Gestión de Usuarios

#### Opción A: Modo Interactivo (Recomendado)

```bash
python manage.py gestionar_usuarios_roles
```

Luego sigue las instrucciones en pantalla.

#### Opción B: Modo Comando

```bash
# Listar usuarios
python manage.py gestionar_usuarios_roles --listar todos

# Listar por rol
python manage.py gestionar_usuarios_roles --listar medico
python manage.py gestionar_usuarios_roles --listar matrona
python manage.py gestionar_usuarios_roles --listar tens
```

---

## 🎯 Ejemplos Prácticos

### Ejemplo 1: Crear un Nuevo Médico

```bash
python manage.py gestionar_usuarios_roles
```

Selecciona opción **1** (Crear nuevo usuario):

```
👤 Nombre de usuario: doctor_ramirez
📧 Email: ramirez@hospital.cl
👤 Nombre: Carlos
👤 Apellido: Ramírez
🔒 Contraseña: ******
🔒 Confirmar contraseña: ******

📋 Roles disponibles:
  1. Administrador
  2. Médico
  3. Matrona
  4. TENS
  5. Paciente

👉 Selecciona el rol (1-5): 2

✅ Usuario "doctor_ramirez" creado exitosamente con rol "Medico"!

¿Deseas crear el perfil completo para este usuario? (s/n): s
```

Si seleccionas "s", te pedirá datos adicionales como RUT, fecha de nacimiento, especialidad, etc.

---

### Ejemplo 2: Asignar Rol Adicional

Si un usuario necesita múltiples roles:

```bash
python manage.py gestionar_usuarios_roles
```

Selecciona opción **2** (Asignar/Remover rol):

```
👤 Nombre de usuario: doctor_ramirez

📋 Roles actuales: Medico

¿Qué deseas hacer?
  1. Asignar nuevo rol
  2. Remover rol existente

👉 Selecciona (1-2): 1

📋 Roles disponibles:
  1. Administrador
  2. Médico
  3. Matrona
  4. TENS
  5. Paciente

👉 Selecciona el rol a asignar (1-5): 1

✅ Rol "Administrador" asignado a "doctor_ramirez"!
```

---

### Ejemplo 3: Listar Usuarios por Rol

```bash
python manage.py gestionar_usuarios_roles --listar medico
```

**Salida:**
```
═══════════════════════════════════════════════════════════
        MÉDICOS (2)
═══════════════════════════════════════════════════════════

┌─────────────────────┬───────────────────────────┬──────────────────────────┬────────────┐
│ Username            │ Nombre Completo           │ Roles                    │ Estado     │
├─────────────────────┼───────────────────────────┼──────────────────────────┼────────────┤
│ medico              │ Carlos González           │ Medico                   │ ✅ Activo  │
│ doctor_ramirez      │ Carlos Ramírez            │ Medico, Administrador    │ ✅ Activo  │
└─────────────────────┴───────────────────────────┴──────────────────────────┴────────────┘
```

---

### Ejemplo 4: Cambiar Contraseña

```bash
python manage.py gestionar_usuarios_roles
```

Selecciona opción **4** (Cambiar contraseña):

```
👤 Nombre de usuario: doctor_ramirez
🔒 Nueva contraseña: ********
🔒 Confirmar contraseña: ********

✅ Contraseña actualizada para "doctor_ramirez"!
```

---

### Ejemplo 5: Desactivar Usuario Temporalmente

```bash
python manage.py gestionar_usuarios_roles
```

Selecciona opción **5** (Activar/Desactivar):

```
👤 Nombre de usuario: doctor_ramirez

📊 Estado actual: Activo

¿Deseas DESACTIVAR este usuario? (s/n): s

⚠️ Usuario "doctor_ramirez" desactivado.
```

El usuario no podrá iniciar sesión hasta que sea reactivado.

---

### Ejemplo 6: Crear Usuarios de Demo Masivos

Para pruebas rápidas:

```bash
python manage.py gestionar_usuarios_roles
```

Selecciona opción **7** (Crear usuarios masivos):

```
¿Deseas crear 10 usuarios de demostración? (s/n): s

   ✅ medico1 (Medico)
   ✅ medico2 (Medico)
   ✅ matrona1 (Matrona)
   ✅ matrona2 (Matrona)
   ✅ tens1 (TENS)
   ✅ tens2 (TENS)
   ✅ admin1 (Administrador)
   ✅ paciente1 (Paciente)
   ✅ paciente2 (Paciente)
   ✅ paciente3 (Paciente)

✅ 10 usuarios de demostración creados.
🔒 Contraseña para todos: demo123
```

---

## 📝 Scripts Disponibles

### Script 1: `gestionar_usuarios_roles.py`

**Ubicación:** `gestionApp/management/commands/gestionar_usuarios_roles.py`

**Características:**
- ✅ Modo interactivo completo
- ✅ Creación de usuarios con perfiles completos
- ✅ Asignación/remoción de roles
- ✅ Listado de usuarios
- ✅ Cambio de contraseñas
- ✅ Activación/desactivación
- ✅ Eliminación segura
- ✅ Creación masiva de demos

---

### Script 2: `crear_usuarios_rapido.py`

**Ubicación:** `scripts/crear_usuarios_rapido.py`

**Uso:** Para usar desde Django shell

```bash
python manage.py shell
```

```python
>>> from scripts.crear_usuarios_rapido import *

# Ver ejemplos
>>> ejemplos_uso()

# Crear grupos
>>> crear_grupos_sistema()

# Crear un usuario
>>> crear_usuario(
...     username='nuevo_medico',
...     password='pass123',
...     email='nuevo@hospital.cl',
...     first_name='Juan',
...     last_name='Pérez',
...     rol='Medico'
... )

# Listar usuarios
>>> listar_usuarios()

# Listar solo médicos
>>> listar_usuarios('Medico')

# Asignar rol
>>> asignar_rol('nuevo_medico', 'Administrador')

# Remover rol
>>> remover_rol('nuevo_medico', 'Administrador')

# Cambiar contraseña
>>> cambiar_password('nuevo_medico', 'nueva_pass')

# Crear usuarios demo
>>> crear_usuarios_demo()
```

---

## 🔐 Credenciales por Defecto

### Usuarios Iniciales (comando: crear_usuarios_iniciales)

| Username | Password | Rol | Email |
|----------|----------|-----|-------|
| admin | pass123 | Admin | admin@hospital.cl |
| medico | pass123 | Médico | medico@hospital.cl |
| matrona | pass123 | Matrona | matrona@hospital.cl |
| tens | pass123 | TENS | tens@hospital.cl |

### Usuarios Demo (opción 7 del menú interactivo)

| Username | Password | Rol |
|----------|----------|-----|
| medico1 | pass123 | Médico |
| medico2 | pass123 | Médico |
| matrona1 | pass123 | Matrona |
| matrona2 | pass123 | Matrona |
| tens1 | pass123 | TENS |
| tens2 | pass123 | TENS |
| admin1 | pass123 | Administrador |
| paciente1-3 | pass123 | Paciente |

---

## ⚠️ Notas Importantes

1. **Siempre crea los grupos primero** antes de asignar usuarios
2. **Las contraseñas** deben cambiarse en producción
3. **Los usuarios demo** son solo para pruebas
4. **La eliminación de usuarios es irreversible** - ten cuidado
5. **Desactivar temporalmente** es mejor que eliminar
6. **Un usuario puede tener múltiples roles** si es necesario

---

## 🆘 Solución de Problemas

### Problema: "Grupo X no existe"

**Solución:**
```bash
python manage.py crear_grupos_sistema
```

### Problema: "Usuario ya existe"

El usuario ya fue creado. Usa las opciones de listar o asignar rol en su lugar.

### Problema: Error al crear perfil completo

Asegúrate de que los catálogos estén creados:
```bash
python manage.py populate_catalogs
```

---

## 📞 Contacto

Para más información o soporte, contacta al equipo de desarrollo.

---

**Última actualización:** Diciembre 2025  
**Versión del documento:** 1.0
