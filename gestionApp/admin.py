# ============================================
# GESTION APP ADMIN
# ============================================

from django.contrib import admin
from gestionApp.models import (
    CatalogoSexo,
    CatalogoNacionalidad,
    CatalogoPuebloOriginario,
    CatalogoEstadoCivil,
    CatalogoPrevision,
    CatalogoTurno,
    CatalogoEspecialidad,
    CatalogoNivelTens,
    CatalogoCertificacion,
    Persona,
    Paciente,
    Medico,
    Matrona,
    Tens,
)

# ============================================
# CATÁLOGOS
# ============================================

@admin.register(CatalogoSexo)
class CatalogoSexoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']


@admin.register(CatalogoNacionalidad)
class CatalogoNacionalidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre', 'codigo']


@admin.register(CatalogoPuebloOriginario)
class CatalogoPuebloOriginarioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']


@admin.register(CatalogoEstadoCivil)
class CatalogoEstadoCivilAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']


@admin.register(CatalogoPrevision)
class CatalogoPrevisionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']


@admin.register(CatalogoEspecialidad)
class CatalogoEspecialidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'activo']  # ✅ REMOVIDO 'tipo' (no existe)
    list_filter = ['activo']  # ✅ REMOVIDO 'tipo' de filter
    search_fields = ['nombre', 'codigo']


@admin.register(CatalogoTurno)
class CatalogoTurnoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'activo']  # ✅ REMOVIDO 'hora_inicio', 'hora_fin' (no existen)
    list_filter = ['activo']
    search_fields = ['nombre', 'codigo']


@admin.register(CatalogoNivelTens)
class CatalogoNivelTensAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']


@admin.register(CatalogoCertificacion)
class CatalogoCertificacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']


# ============================================
# MODELOS PRINCIPALES
# ============================================

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ['Rut', 'Nombre', 'Sexo', 'Nacionalidad', 'Activo']
    list_filter = ['Activo', 'Sexo', 'Nacionalidad']
    search_fields = ['Rut', 'Nombre', 'Apellido_Paterno', 'Apellido_Materno']

    fieldsets = (
        ('Identidad', {
            'fields': ('Rut', 'Nombre', 'Apellido_Paterno', 'Apellido_Materno', 'Fecha_nacimiento')
        }),
        ('Demográfico', {
            'fields': ('Sexo', 'Nacionalidad', 'Pueblos_originarios')
        }),
        ('Condiciones Especiales', {
            'fields': (
                'Inmigrante',
                'Discapacidad',
                'Tipo_de_Discapacidad',
                'Privada_de_Libertad',
                'Trans_Masculino',
            )
        }),
        ('Contacto', {
            'fields': ('Telefono', 'Email', 'Direccion')
        }),
        ('Control', {
            'fields': ('Activo',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['persona', 'paridad', 'control_prenatal', 'activo']  # ✅ CAMBIADO 'Activo' a 'activo'
    list_filter = ['activo', 'control_prenatal']  # ✅ REMOVIDO 'prevision' (no es field)
    search_fields = ['persona__Nombre', 'persona__Rut']


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ['persona', 'Registro_medico', 'Especialidad', 'Años_experiencia', 'Activo']
    list_filter = ['Activo', 'Especialidad']
    search_fields = ['persona__Nombre', 'Registro_medico']


@admin.register(Matrona)
class MatronaAdmin(admin.ModelAdmin):
    list_display = ['persona', 'Registro_medico', 'Especialidad', 'Años_experiencia', 'Activo']
    list_filter = ['Activo', 'Especialidad']
    search_fields = ['persona__Nombre', 'Registro_medico']


@admin.register(Tens)
class TensAdmin(admin.ModelAdmin):
    list_display = ['persona', 'Nivel', 'Certificaciones', 'Años_experiencia', 'Activo']
    list_filter = ['Activo', 'Nivel', 'Certificaciones']
    search_fields = ['persona__Nombre']