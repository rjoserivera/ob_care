"""
ARCHIVO DE REGISTRO DE NUEVOS CATÁLOGOS
=======================================
Este archivo registra los catálogos nuevos creados a partir de la fecha.

FECHA: 2025-12-15
MOTIVO: Actualización Ficha Obstétrica y Parto (Solicitud Usuario)

CATÁLOGOS NUEVOS:
-----------------

1. CatalogoTipoPaciente (matronaApp)
   - Clasificación del tipo de paciente (Ej: Fonasa, Isapre, Particular, Convenio, etc.)
   - Campos: codigo, nombre, activo

2. CatalogoDiscapacidad (matronaApp)
   - Tipos de discapacidades (Ej: Física, Auditiva, Visual, Intelectual, Psíquica, Visceral)
   - Campos: codigo, nombre, activo

3. CatalogoDerivacion (ingresoPartoApp)
   - Centros o especialidades de derivación (Ej: Infectología, Alto Riesgo, Gastro)
   - Campos: codigo, nombre, activo

4. CatalogoARO (matronaApp)
   - Clasificaciones de Alto Riesgo Obstétrico
   - Campos: nombre, activo

CAMPOS NUEVOS EN FICHA OBSTÉTRICA / PARTO:
----------------------------------
- tipo_paciente (FK a CatalogoTipoPaciente)
- tiene_discapacidad (Boolean)
- discapacidad (FK a CatalogoDiscapacidad, opcional)
- clasificacion_aro (FK a CatalogoARO)
- fecha_creacion (Mostrar en template)

CATÁLOGOS EXISTENTES (Pre-existentes en el sistema):
----------------------------------------------------
- CatalogoTipoParto - Tipos de parto (Vaginal, Cesárea)
- CatalogoRegimen - Régimen de parto (Libre Demanda, Ayuno, etc.)
- CatalogoClasificacionRobson - Clasificación de Robson del parto
- CatalogoPosicionParto - Posiciones maternas durante el parto
- CatalogoEstadoPerine - Estados del periné post-parto
- CatalogoCausaCesarea - Causas médicas de cesárea
- CatalogoPersonaAcompanante - Relación con el acompañante
- CatalogoMotivoPartoNoAcompanado - Motivos de parto sin acompañamiento

CAMPOS/CATÁLOGOS ELIMINADOS:
-----------------------------
- hepatitis_b_realizado, hepatitis_b_fecha, hepatitis_b_resultado (Eliminados de FichaObstetrica - 2025-12-15)
- derivacion_hepatitis_b (Eliminado de FichaObstetrica - 2025-12-15)
- ttc_estado (Eliminado de FichaObstetrica - 2025-12-15)
- TTC_CHOICES (Eliminado de FichaObstetrica - 2025-12-15)

"""
