# 📋 INFORME FINAL DEL PROYECTO OB-CARE

## Sistema de Gestión Obstétrica - Hospital Clínico Herminda Martín

**Unidad 3: Implementación de la Solución**

---

## 📑 Índice

1. [Identificación del Equipo](#i-identificación-del-equipo)
2. [Objetivos del Proyecto](#ii-objetivos-del-proyecto)
3. [Descripción del Desafío](#iii-descripción-del-desafío)
4. [Justificación de la Solución](#iv-justificación-de-la-solución)
5. [Enfoque Técnico](#v-enfoque-técnico)
6. [Arquitectura del Sistema](#vi-arquitectura-del-sistema)
7. [Aplicaciones del Sistema](#vii-aplicaciones-del-sistema)
8. [Flujos de Proceso](#viii-flujos-de-proceso)
9. [Gestión del Proyecto](#ix-gestión-del-proyecto)
10. [Entregables](#x-entregables)
11. [Plan de Pruebas](#xi-plan-de-pruebas)
12. [Anexos](#xii-anexos)
13. [Preguntas Frecuentes](#xiii-preguntas-frecuentes)

---

## I. Identificación del Equipo

### Datos del Proyecto

| Campo | Valor |
|-------|-------|
| **Nombre del Proyecto** | OB-CARE: Sistema de Gestión Obstétrica |
| **Institución** | Hospital Clínico Herminda Martín |
| **Ubicación** | Chillán, Región de Ñuble |
| **Fecha de Entrega** | Diciembre 2025 |
| **Versión** | 1.0.0 |

### Integrantes del Equipo

| Nombre | Rol Principal | Responsabilidades |
|--------|---------------|-------------------|
| **José Rivera** | Líder de Proyecto / Backend | Arquitectura del sistema, desarrollo Django, diseño UX/UI, coordinación del equipo |
| **Edvanc** | Desarrollador de Base de Datos | Diseño del modelo de datos, implementación MySQL, optimización de consultas |
| **Fredy** | Desarrollador de Base de Datos | Normalización 3FN, integridad referencial, scripts de migración |
| **Cristian** | Integración Legacy | Conexión con sistema heredado, router de base de datos, migración de datos |
| **Alexi** | Seguridad y QA | Autenticación, control de acceso por roles, plan de pruebas, testing |

---

## II. Objetivos del Proyecto

### Objetivo General

Desarrollar e implementar un sistema integral de gestión obstétrica que optimice los procesos de atención en el área de maternidad del Hospital Clínico Herminda Martín, mejorando la eficiencia operacional, la trazabilidad clínica y la calidad de atención a las pacientes.

### Objetivos Específicos

| # | Objetivo | Indicador de Éxito |
|---|----------|-------------------|
| 1 | Digitalizar el registro de fichas obstétricas | 100% de fichas en formato digital |
| 2 | Implementar sistema de gestión de procesos de parto en tiempo real | Reducción de tiempo promedio en sala a ~1 hora |
| 3 | Automatizar la asignación de personal según número de bebés | Cálculo automático con fórmula validada |
| 4 | Establecer sistema de notificaciones push con timeout de 60 segundos | 95% de confirmaciones dentro del tiempo |
| 5 | Garantizar trazabilidad completa del proceso madre-hijo | Vinculación permanente MT-XXXX ↔ RN-XXXX |
| 6 | Integrar datos históricos del sistema legacy | Acceso de solo lectura a controles previos |

---

## III. Descripción del Desafío

### Contexto Institucional

El Hospital Clínico Herminda Martín es el centro de referencia para la atención obstétrica en la Región de Ñuble:

| Indicador | Valor |
|-----------|-------|
| Población atendida | ~480,000 habitantes |
| Partos anuales | ~3,500 |
| Salas de parto | 4 |
| Personal obstétrico | 45+ profesionales |

### Problemáticas Identificadas

| # | Problema | Impacto |
|---|----------|---------|
| 1 | Registros manuales en papel | Pérdida de información, ilegibilidad, demoras |
| 2 | Sin sistema de notificación al personal | Tiempos de respuesta variables, descoordinación |
| 3 | Subutilización de salas de parto | Tiempos prolongados, colas de espera |
| 4 | Falta de trazabilidad madre-hijo | Riesgos en identificación, auditoría deficiente |
| 5 | Datos históricos inaccesibles | Sistema legacy aislado, sin integración |
| 6 | Sin métricas de rendimiento | Imposibilidad de mejora continua |

### Oportunidad de Mejora

La implementación de un sistema digital integrado permite:
- **Optimizar uso de salas**: Inicio de proceso a 8cm de dilatación
- **Respuesta inmediata**: Notificaciones con timeout de 60 segundos
- **Coordinación eficiente**: Cálculo automático de personal
- **Trazabilidad total**: Registro de cada evento con timestamp

---

## IV. Justificación de la Solución

### Requerimientos Funcionales

| ID | Requerimiento | Prioridad |
|----|---------------|-----------|
| RF-01 | Gestión de pacientes y personal con validación de RUT | Alta |
| RF-02 | Creación y seguimiento de fichas obstétricas | Alta |
| RF-03 | Registro de signos vitales por TENS | Alta |
| RF-04 | Catálogo de patologías CIE-10 | Media |
| RF-05 | Proceso de ingreso a parto con exámenes de laboratorio | Alta |
| RF-06 | Registro de parto en 9 pasos secuenciales | Alta |
| RF-07 | Registro de recién nacido en 9 pasos | Alta |
| RF-08 | **Gestión de procesos de parto en tiempo real** | **Crítica** |
| RF-09 | Sistema de notificaciones push con confirmación | Alta |
| RF-10 | Integración con sistema legacy (solo lectura) | Media |
| RF-11 | Dashboards diferenciados por rol | Media |
| RF-12 | Reportes y estadísticas | Media |

### Requerimientos No Funcionales

| Categoría | Requerimiento |
|-----------|---------------|
| **Rendimiento** | Tiempo de respuesta < 2 segundos para operaciones críticas |
| **Disponibilidad** | 99.5% uptime (24/7) |
| **Seguridad** | Autenticación obligatoria, control por roles, auditoría completa |
| **Usabilidad** | Interfaz responsive, compatible con tablets y móviles |
| **Escalabilidad** | Soporte para crecimiento de 20% anual |
| **Mantenibilidad** | Código documentado, arquitectura modular |

### Impacto Esperado

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| Tiempo promedio en sala | 2+ horas | ~1 hora | 50% |
| Tiempo de respuesta personal | Variable | < 60 seg | Estandarizado |
| Trazabilidad de procesos | 60% | 100% | +40% |
| Digitalización de registros | 20% | 100% | +80% |
| Errores de identificación | Frecuentes | Eliminados | 100% |

---

## V. Enfoque Técnico

### Stack Tecnológico

| Capa | Tecnología | Versión | Justificación |
|------|------------|---------|---------------|
| **Backend** | Django | 5.2.8 | Framework robusto, ORM potente, seguridad integrada |
| **Base de Datos** | MySQL | 8.0 | Estándar hospitalario, rendimiento probado |
| **Frontend** | Bootstrap | 5.3.7 | Responsive, componentes modernos |
| **Tiempo Real** | Django Channels | 4.x | WebSocket para notificaciones |
| **Cache** | Redis | 7.x | Sesiones, channels, cache |
| **Tareas** | Celery | 5.x | Tareas asíncronas, timeouts |
| **Push** | Firebase FCM | - | Notificaciones móviles |

### Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ARQUITECTURA OB-CARE                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│    ┌─────────┐     ┌─────────┐     ┌─────────┐                     │
│    │ Browser │     │ Mobile  │     │ Push    │                     │
│    │  (Web)  │     │  App    │     │ Client  │                     │
│    └────┬────┘     └────┬────┘     └────┬────┘                     │
│         │               │               │                           │
│         └───────────────┴───────────────┘                           │
│                         │                                           │
│                         ▼                                           │
│              ┌─────────────────────┐                               │
│              │      Nginx          │                               │
│              │  (Reverse Proxy)    │                               │
│              └──────────┬──────────┘                               │
│                         │                                           │
│         ┌───────────────┼───────────────┐                          │
│         │               │               │                          │
│         ▼               ▼               ▼                          │
│   ┌───────────┐  ┌───────────┐  ┌───────────┐                     │
│   │  Daphne   │  │  Daphne   │  │  Daphne   │                     │
│   │  (ASGI)   │  │  (ASGI)   │  │  (ASGI)   │                     │
│   └─────┬─────┘  └─────┬─────┘  └─────┬─────┘                     │
│         │               │               │                          │
│         └───────────────┴───────────────┘                          │
│                         │                                           │
│         ┌───────────────┴───────────────┐                          │
│         │                               │                          │
│         ▼                               ▼                          │
│   ┌───────────┐                  ┌───────────┐                     │
│   │   MySQL   │                  │   Redis   │                     │
│   │ (Primary) │                  │  (Cache/  │                     │
│   │           │                  │  Channels)│                     │
│   └───────────┘                  └───────────┘                     │
│                                                                     │
│   ┌───────────┐                  ┌───────────┐                     │
│   │  Celery   │                  │  Firebase │                     │
│   │ (Workers) │                  │   (Push)  │                     │
│   └───────────┘                  └───────────┘                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Diseño de Base de Datos

La base de datos está normalizada en **Tercera Forma Normal (3FN)**:

- **20+ tablas de catálogos** para mantener integridad referencial
- **ForeignKey** en lugar de CHOICES para permitir mantenimiento sin código
- **Soft delete** en entidades críticas para preservar historial
- **Índices optimizados** en campos de búsqueda frecuente
- **Auditoría automática** con django-auditlog

### Seguridad

| Capa | Implementación |
|------|----------------|
| **Autenticación** | Django Auth + Sesiones en BD |
| **Autorización** | Grupos Django (5 roles) + Decoradores personalizados |
| **CSRF** | Tokens en todos los formularios |
| **XSS** | Escape automático en templates |
| **SQL Injection** | ORM de Django (parametrizado) |
| **Passwords** | PBKDF2 + SHA256 |
| **Sesiones** | Timeout 8 horas, cookie segura |
| **Auditoría** | Log de todos los accesos y cambios |

---

## VI. Arquitectura del Sistema

### Estructura del Proyecto

```
obstetric_care/                    # Proyecto Django principal
├── settings/                      # Configuraciones por entorno
│   ├── base.py                   # Configuración compartida
│   ├── development.py            # Desarrollo local
│   └── production.py             # Producción
├── urls.py                        # URLs raíz
├── asgi.py                        # WebSocket
├── celery.py                      # Tareas asíncronas
│
├── core/                          # Utilidades compartidas
├── gestionApp/                    # Personas y personal
├── matronaApp/                    # Fichas obstétricas
├── medicoApp/                     # Patologías CIE-10
├── tensApp/                       # Signos vitales
├── ingresoPartoApp/               # Ingreso a parto
├── partosApp/                     # Registro de parto
├── recienNacidoApp/               # Registro de RN
├── gestionProcesosApp/            # Flujos de proceso (CENTRAL)
├── legacyApp/                     # Sistema heredado
└── inicioApp/                     # Autenticación
```

### Base de Datos Dual

```
┌─────────────────────────┐      ┌─────────────────────────┐
│                         │      │                         │
│    obstetric_care       │      │    hospital_legacy      │
│    (Base Principal)     │      │    (Solo Lectura)       │
│                         │      │                         │
│  - Pacientes            │      │  - Controles previos    │
│  - Personal             │      │  - Historial médico     │
│  - Fichas obstétricas   │◄────►│  - Exámenes antiguos    │
│  - Procesos de parto    │      │                         │
│  - Recién nacidos       │      │  managed=False          │
│  - Catálogos            │      │  (no migrations)        │
│  - Auditoría            │      │                         │
│                         │      │                         │
└─────────────────────────┘      └─────────────────────────┘
         │                                  │
         └──────────┬───────────────────────┘
                    │
                    ▼
           ┌─────────────────┐
           │  LegacyRouter   │
           │  (Auto-routing) │
           └─────────────────┘
```

---

## VII. Aplicaciones del Sistema

### Catálogo de Aplicaciones (12 Apps)

| # | App | Tamaño Doc | Descripción | Modelos Principales |
|---|-----|------------|-------------|---------------------|
| 1 | **obstetric_care** | 46 KB | Proyecto Django principal | Settings, URLs, ASGI, Celery |
| 2 | **core** | 47 KB | Utilidades compartidas | Modelos base, mixins, decoradores, validators |
| 3 | **inicioApp** | 35 KB | Autenticación y dashboards | RegistroAcceso, SesionActiva, ConfiguracionPantalla |
| 4 | **gestionApp** | 10 KB | Personas y personal | Persona, Paciente, Medico, Matrona, Tens |
| 5 | **matronaApp** | 10 KB | Fichas obstétricas | FichaObstetrica, MedicamentoFicha, IngresoPaciente |
| 6 | **medicoApp** | 4.5 KB | Patologías | Patologias (CIE-10) |
| 7 | **tensApp** | 7.5 KB | Signos vitales | RegistroTens, Tratamiento_aplicado |
| 8 | **ingresoPartoApp** | 7.5 KB | Ingreso a parto | FichaParto |
| 9 | **partosApp** | 11 KB | Registro de parto | RegistroParto (9 pasos secuenciales) |
| 10 | **recienNacidoApp** | 10 KB | Recién nacidos | RegistroRecienNacido (9 pasos), DocumentosParto |
| 11 | **gestionProcesosApp** | 96 KB | **Flujos de proceso (CENTRAL)** | ProcesoParto, SalaParto, ConfirmacionPersonal, AsignacionPersonal |
| 12 | **legacyApp** | 8 KB | Sistema heredado | ControlesPrevios (managed=False) |

### Diagrama de Dependencias

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DEPENDENCIAS DE APPS                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│                          ┌─────────────┐                            │
│                          │    core     │                            │
│                          │ (utilidades)│                            │
│                          └──────┬──────┘                            │
│                                 │                                    │
│         ┌───────────────────────┼───────────────────────┐           │
│         │                       │                       │           │
│         ▼                       ▼                       ▼           │
│  ┌─────────────┐        ┌─────────────┐        ┌─────────────┐     │
│  │ gestionApp  │        │  inicioApp  │        │  legacyApp  │     │
│  │ (personas)  │        │   (auth)    │        │  (legacy)   │     │
│  └──────┬──────┘        └─────────────┘        └─────────────┘     │
│         │                                                           │
│         ▼                                                           │
│  ┌─────────────┐                                                    │
│  │ matronaApp  │◄─────────────────────────────────────┐            │
│  │  (fichas)   │                                      │            │
│  └──────┬──────┘                                      │            │
│         │                                             │            │
│    ┌────┴────┬────────────┬───────────┐              │            │
│    │         │            │           │              │            │
│    ▼         ▼            ▼           ▼              │            │
│ ┌───────┐ ┌───────┐ ┌──────────┐ ┌────────┐         │            │
│ │medico │ │ tens  │ │ ingreso  │ │ partos │         │            │
│ │ App   │ │ App   │ │ PartoApp │ │  App   │         │            │
│ └───────┘ └───────┘ └────┬─────┘ └───┬────┘         │            │
│                          │           │              │            │
│                          │     ┌─────┴─────┐        │            │
│                          │     │           │        │            │
│                          │     ▼           ▼        │            │
│                          │ ┌────────┐ ┌────────────┐│            │
│                          │ │recien  │ │ gestion    ││            │
│                          └►│Nacido  │ │ Procesos   │◄────────────┘
│                            │  App   │ │    App     │              │
│                            └────────┘ └────────────┘              │
│                                       (APP CENTRAL)               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Modelos por App

| App | Modelos | Catálogos |
|-----|---------|-----------|
| **gestionApp** | Persona, Paciente, Medico, Matrona, Tens | CatalogoSexo, CatalogoNacionalidad, CatalogoPrevision, etc. (9) |
| **matronaApp** | FichaObstetrica, IngresoPaciente, MedicamentoFicha, AdministracionMedicamento | CatalogoViaAdministracion, CatalogoConsultorioOrigen |
| **medicoApp** | Patologias | - |
| **tensApp** | RegistroTens, Tratamiento_aplicado | - |
| **ingresoPartoApp** | FichaParto | CatalogoEstadoCervical, CatalogoEstadoFetal |
| **partosApp** | RegistroParto | 8 catálogos (TipoParto, Robson, Posición, etc.) |
| **recienNacidoApp** | RegistroRecienNacido, DocumentosParto | CatalogoSexoRN |
| **gestionProcesosApp** | ProcesoParto, SalaParto, ConfirmacionPersonal, AsignacionPersonal, RegistroIngresoSala, NotificacionProceso, EventoProceso | 7 catálogos (EstadoProceso, EstadoSala, TipoPaciente, etc.) |
| **inicioApp** | RegistroAcceso, SesionActiva, ConfiguracionPantalla | - |
| **legacyApp** | ControlesPrevios | - |

---

## VIII. Flujos de Proceso

### Reglas de Negocio Críticas

| Parámetro | Valor | Justificación |
|-----------|-------|---------------|
| **Inicio del proceso** | 8 cm dilatación | Cuando el equipo llega, paciente ya está en 9-10cm |
| **Timeout confirmación** | 60 segundos | Respuesta inmediata obligatoria |
| **Apego piel a piel** | 5 minutos | Balance entre contacto inicial y eficiencia |
| **Tiempo promedio sala** | ~1 hora | Optimiza rotación de salas |

### Fórmula de Cálculo de Personal

```
POR CADA BEBÉ:
  + 1 Médico
  + 1 Matrona
  + 1 TENS (asignado al bebé)

ADICIONAL FIJO:
  + 2 TENS de apoyo

CASOS ESPECIALES:
  + 1 Anestesiólogo (si cesárea)
  + 1 Médico extra (si crítico)
```

| Escenario | Bebés | Médicos | Matronas | TENS | Anest. | Total |
|-----------|-------|---------|----------|------|--------|-------|
| Parto normal | 1 | 1 | 1 | 3 | 0 | **5** |
| Gemelar cesárea | 2 | 2 | 2 | 4 | 1 | **9** |
| Normal crítico | 1 | 2 | 1 | 3 | 1 | **7** |

### Flujos Implementados

| # | Flujo | Descripción | Características |
|---|-------|-------------|-----------------|
| 1 | **Parto Normal** | Un bebé, vaginal | Proceso estándar ~1 hora |
| 2 | **Parto Gemelar** | Dos bebés, cesárea | Personal duplicado, códigos RN-XXXX-A/B |
| 3 | **Patologías Graves** | Con derivación UCI | Cierre parcial, ficha derivada |
| 4 | **Emergencia Externa** | Ingreso urgente | Ficha rápida, proceso anticipado |

### Diagrama de Flujo Principal

```
┌─────────────────┐
│ PACIENTE 8cm    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Matrona inicia  │────►│ Sistema asigna  │────►│ Notificaciones  │
│    proceso      │     │ sala + personal │     │   push (60s)    │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Personal llega  │◄────│  Confirmación   │◄────│    Timeout      │
│   secuencial    │     │    recibida     │     │   verificado    │
└────────┬────────┘     └─────────────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐
│ Médico inicia   │
│   CRONÓMETRO    │ ◄── Momento único, solo médico
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│     PARTO       │────►│  Apego 5 min    │────►│    Registro     │
│   (bebé nace)   │     │  piel a piel    │     │   recién nacido │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │ Médico finaliza │
                                                │ Sala liberada   │
                                                └─────────────────┘
```

### Máquina de Estados del Proceso

```
CREADO → INICIADO → CONFIRMADO → EN_CURSO → CERRADO
                                     │
                                     └──────► CERRADO_DERIVACION
```

### Códigos Generados

| Entidad | Formato | Ejemplo |
|---------|---------|---------|
| Proceso de Parto | MT-XXXX | MT-0145 |
| Recién Nacido (simple) | RN-XXXX | RN-0145 |
| Recién Nacido (gemelar) | RN-XXXX-L | RN-0156-A, RN-0156-B |

---

## IX. Gestión del Proyecto

### Cronograma

| Semana | Actividades | Responsable |
|--------|-------------|-------------|
| **1-2** | Análisis de requerimientos, diseño de BD | Todo el equipo |
| **3-4** | Implementación core, gestionApp, auth | José, Alexi |
| **5** | matronaApp, medicoApp, tensApp | José, Edvanc |
| **6** | ingresoPartoApp, partosApp, recienNacidoApp | José, Fredy |
| **7** | gestionProcesosApp (flujos centrales) | José |
| **8** | legacyApp, integración | Cristian |
| **9** | Testing, correcciones | Alexi, Todo el equipo |
| **10** | Documentación, despliegue | Todo el equipo |

### Matriz de Responsabilidades

| Entregable | José | Edvanc | Fredy | Cristian | Alexi |
|------------|:----:|:------:|:-----:|:--------:|:-----:|
| Arquitectura | ✅ | | | | |
| Modelos de datos | ✅ | ✅ | ✅ | | |
| Backend Django | ✅ | | | | |
| Frontend Bootstrap | ✅ | | | | |
| Base de datos | | ✅ | ✅ | | |
| Normalización 3FN | | | ✅ | | |
| Integración legacy | | | | ✅ | |
| Autenticación | | | | | ✅ |
| Testing | | | | | ✅ |
| Documentación | ✅ | | | | ✅ |

---

## X. Entregables

### Repositorio de Código

| Elemento | Descripción |
|----------|-------------|
| **URL** | https://github.com/[organization]/obstetric-care |
| **Rama principal** | `main` |
| **Rama desarrollo** | `develop` |
| **Convención commits** | Conventional Commits |

### Aplicaciones Django (12 apps)

| # | App | Archivos | Líneas de Código (est.) |
|---|-----|----------|------------------------|
| 1 | obstetric_care | 8+ | ~500 |
| 2 | core | 15+ | ~1,500 |
| 3 | inicioApp | 12+ | ~1,000 |
| 4 | gestionApp | 10+ | ~800 |
| 5 | matronaApp | 12+ | ~900 |
| 6 | medicoApp | 8+ | ~400 |
| 7 | tensApp | 10+ | ~600 |
| 8 | ingresoPartoApp | 10+ | ~700 |
| 9 | partosApp | 15+ | ~1,200 |
| 10 | recienNacidoApp | 15+ | ~1,200 |
| 11 | gestionProcesosApp | 20+ | ~2,500 |
| 12 | legacyApp | 6+ | ~300 |
| | **TOTAL** | **140+** | **~11,600** |

### Base de Datos

| Elemento | Cantidad |
|----------|----------|
| Tablas principales | 25+ |
| Tablas de catálogos | 20+ |
| Índices | 40+ |
| Relaciones FK | 60+ |

### Documentación Técnica (389 KB - 17 archivos)

| # | Documento | Tamaño | Contenido |
|---|-----------|--------|-----------|
| 1 | README.md | 9 KB | Guía de instalación |
| 2 | INFORME_FINAL.md | 45 KB | Este documento |
| 3 | FLUJOS_TECNICOS.md | 35 KB | Análisis de flujos y reglas de negocio |
| 4 | API_ESTADOS.md | 23 KB | Endpoints REST, WebSocket, máquinas de estado |
| 5 | obstetric_care.md | 46 KB | Proyecto principal Django |
| 6 | core.md | 47 KB | Utilidades compartidas |
| 7 | inicioApp.md | 35 KB | Autenticación y dashboards |
| 8 | gestionApp.md | 10 KB | Personas y personal |
| 9 | matronaApp.md | 10 KB | Fichas obstétricas |
| 10 | medicoApp.md | 4.5 KB | Patologías CIE-10 |
| 11 | tensApp.md | 7.5 KB | Signos vitales |
| 12 | ingresoPartoApp.md | 7.5 KB | Ingreso a parto |
| 13 | partosApp.md | 11 KB | Registro de parto |
| 14 | recienNacidoApp.md | 10 KB | Recién nacidos |
| 15 | gestionProcesosApp.md | 96 KB | App central de flujos |
| 16 | legacyApp.md | 8 KB | Sistema heredado |
| 17 | authentication.md | 11 KB | Sistema de autenticación |

---

## XI. Plan de Pruebas

### Suites de Pruebas

| Suite | Alcance | Casos |
|-------|---------|-------|
| **Core** | Modelos base, utilidades, validadores | 25+ |
| **Autenticación** | Login, logout, roles, sesiones | 15+ |
| **Procesos** | Flujos de parto, confirmaciones, cronómetro | 30+ |
| **Integración** | Legacy, notificaciones, WebSocket | 20+ |

### Casos de Prueba Críticos

| ID | Caso | Resultado Esperado |
|----|------|-------------------|
| CP-001 | Iniciar proceso con >= 8cm | Proceso creado, sala asignada |
| CP-002 | Iniciar proceso con < 8cm | Error de validación |
| CP-003 | Cálculo personal 1 bebé | 5 profesionales |
| CP-004 | Cálculo personal 2 bebés | 9 profesionales |
| CP-005 | Confirmación < 60s | dentro_tiempo = True |
| CP-006 | Confirmación > 60s | dentro_tiempo = False |
| CP-007 | Médico inicia cronómetro | Cronómetro iniciado |
| CP-008 | Matrona intenta iniciar cronómetro | Error de permisos |
| CP-009 | Finalizar sin bebés registrados | Error de validación |
| CP-010 | Derivación a UCI | Estado CERRADO_DERIVACION |
| CP-011 | Login exitoso | Redirección a dashboard según rol |
| CP-012 | Login fallido | Registro de intento fallido |
| CP-013 | Validación RUT | Módulo 11 correcto |
| CP-014 | WebSocket conexión | Eventos en tiempo real |
| CP-015 | Ficha emergencia | Datos mínimos aceptados |

### Comandos de Ejecución

```bash
# Ejecutar todas las pruebas
pytest --cov=. --cov-report=html

# Pruebas por app
pytest gestionProcesosApp/tests/ -v
pytest inicioApp/tests/ -v
pytest core/tests/ -v

# Pruebas de integración
pytest tests/integration/ -v

# Coverage mínimo requerido: 80%
pytest --cov=. --cov-fail-under=80
```

---

## XII. Anexos

### A. Dependencias del Proyecto

```txt
# requirements.txt

Django==5.2.8
mysqlclient==2.2.0
djangorestframework==3.14.0
django-crispy-forms==2.1
crispy-bootstrap5==2024.2
django-auditlog==2.3.0
channels==4.0.0
channels-redis==4.1.0
celery==5.3.0
redis==5.0.0
django-cors-headers==4.3.0
django-filter==23.5
djangorestframework-simplejwt==5.3.0
Pillow==10.1.0
python-dotenv==1.0.0
gunicorn==21.2.0
daphne==4.0.0
whitenoise==6.6.0
pytest-django==4.7.0
pytest-cov==4.1.0
firebase-admin==6.2.0
```

### B. Configuración pytest

```ini
# pytest.ini

[pytest]
DJANGO_SETTINGS_MODULE = obstetric_care.settings.testing
python_files = tests.py test_*.py *_tests.py
addopts = -v --tb=short
filterwarnings =
    ignore::DeprecationWarning
```

### C. Variables de Entorno

```bash
# .env.example

DJANGO_SETTINGS_MODULE=obstetric_care.settings.development
SECRET_KEY=tu-clave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=obstetric_care
DB_USER=root
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=3306

LEGACY_DB_NAME=hospital_legacy
LEGACY_DB_USER=readonly_user
LEGACY_DB_PASSWORD=readonly_password
LEGACY_DB_HOST=legacy-server.hospital.cl

REDIS_URL=redis://localhost:6379/1
CELERY_BROKER_URL=redis://localhost:6379/0

FIREBASE_CREDENTIALS_PATH=/path/to/firebase-credentials.json
```

### D. Glosario de Términos

| Término | Definición |
|---------|------------|
| **Dilatación** | Apertura del cuello uterino medida en centímetros (0-10) |
| **APGAR** | Escala de evaluación del recién nacido (0-10) |
| **Multípara** | Mujer que ha tenido más de un parto |
| **Primigesta** | Mujer en su primer embarazo |
| **Gemelar dicoriónico** | Embarazo de gemelos con dos placentas |
| **Preeclampsia** | Hipertensión durante el embarazo |
| **Eclampsia** | Convulsiones por preeclampsia severa |
| **TENS** | Técnico en Enfermería de Nivel Superior |
| **CIE-10** | Clasificación Internacional de Enfermedades |
| **Robson** | Clasificación de cesáreas en 10 grupos |
| **Ley Dominga** | Ley N° 21.372 sobre derechos de padres de recién nacidos fallecidos |

---

## XIII. Preguntas Frecuentes

### Preguntas por Área

#### Arquitectura (José)
1. ¿Por qué Django y no otro framework?
2. ¿Cómo se maneja la escalabilidad?
3. ¿Por qué WebSocket para notificaciones?
4. ¿Cómo funciona la arquitectura ASGI?

#### Base de Datos (Edvanc/Fredy)
5. ¿Por qué MySQL y no PostgreSQL?
6. ¿Cómo se logró la normalización 3FN?
7. ¿Por qué usar catálogos en lugar de CHOICES?
8. ¿Cómo se manejan las migraciones?

#### Integración (Cristian)
9. ¿Cómo funciona la conexión con el sistema legacy?
10. ¿Por qué solo lectura para la base legacy?
11. ¿Cómo se maneja la migración gradual?
12. ¿Qué pasa si el sistema legacy no está disponible?

#### Seguridad (Alexi)
13. ¿Cómo se implementó el control de acceso por roles?
14. ¿Qué medidas de seguridad se implementaron?
15. ¿Cómo se auditan las acciones del sistema?
16. ¿Cómo funciona el registro de accesos?

#### Flujos de Proceso (José)
17. ¿Por qué iniciar el proceso a 8cm de dilatación?
18. ¿Cómo funciona el cálculo automático de personal?
19. ¿Qué pasa si no se confirma en 60 segundos?
20. ¿Cómo se manejan los partos gemelares?

---

## 📊 Métricas del Proyecto

| Métrica | Valor |
|---------|-------|
| **Apps Django** | 12 |
| **Modelos** | 45+ |
| **Catálogos** | 20+ |
| **Vistas** | 80+ |
| **Templates** | 60+ |
| **Tests** | 100+ |
| **Líneas de código** | ~11,600 |
| **Documentación** | 389 KB (17 archivos) |
| **Cobertura de tests** | 80%+ |

---

## ✅ Conclusión

El sistema **OB-CARE** representa una solución integral para la gestión obstétrica del Hospital Clínico Herminda Martín, abordando las problemáticas identificadas mediante:

1. **Digitalización completa** de todos los registros clínicos
2. **Optimización de procesos** con inicio a 8cm de dilatación
3. **Coordinación eficiente** mediante notificaciones en tiempo real
4. **Trazabilidad total** con vinculación permanente madre-hijo
5. **Integración transparente** con el sistema legacy existente
6. **Seguridad robusta** con control de acceso por roles
7. **Dashboards diferenciados** para cada rol del personal

El sistema está diseñado para escalar con el crecimiento del hospital y adaptarse a futuros requerimientos, manteniendo una arquitectura modular y documentada que facilita el mantenimiento y la evolución continua.

---

**Equipo OB-CARE**  
*Hospital Clínico Herminda Martín*  
*Diciembre 2025*

---

*Documento generado como parte del proyecto de Implementación de Soluciones - Unidad 3*