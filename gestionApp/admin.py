# ============================================
# GESTION APP ADMIN
# ============================================

from django.contrib import admin
from gestionApp.models import (
    Sexo, Nacionalidad, PuebloOriginario, EstadoCivil,
    GrupoSanguineo, Prevision, Consultorio, DuctusVenosus,
    Especialidad, Turno, NivelTENS, CertificacionTENS,
    Persona, Paciente, Medico, Matrona, TENS
)

@admin.register(Sexo)
class SexoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']

@admin.register(Nacionalidad)
class NacionalidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre', 'codigo']

@admin.register(PuebloOriginario)
class PuebloOriginarioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']

@admin.register(EstadoCivil)
class EstadoCivilAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']

@admin.register(GrupoSanguineo)
class GrupoSanguineoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']

@admin.register(Prevision)
class PrevisionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']

@admin.register(Consultorio)
class ConsultorioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'comuna', 'activo']
    list_filter = ['activo', 'comuna']
    search_fields = ['nombre', 'comuna']

@admin.register(DuctusVenosus)
class DuctusVenosusAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'activo']
    list_filter = ['tipo', 'activo']
    search_fields = ['nombre']

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'hora_inicio', 'hora_fin', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']

@admin.register(NivelTENS)
class NivelTENSAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']

@admin.register(CertificacionTENS)
class CertificacionTENSAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ['rut', 'nombre_completo', 'sexo', 'nacionalidad', 'activo']
    list_filter = ['activo', 'sexo', 'nacionalidad']
    search_fields = ['rut', 'nombre', 'apellido_paterno', 'apellido_materno']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    fieldsets = (
        ('Identidad', {
            'fields': ('rut', 'nombre', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento')
        }),
        ('Demográfico', {
            'fields': ('sexo', 'nacionalidad', 'pueblo_originario')
        }),
        ('Condiciones Especiales', {
            'fields': ('inmigrante', 'discapacidad', 'tipo_de_discapacidad', 
                       'privada_de_libertad', 'trans_masculino')
        }),
        ('Contacto', {
            'fields': ('telefono', 'correo', 'direccion', 'region')
        }),
        ('Control', {
            'fields': ('activo', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['persona', 'paridad', 'control_prenatal', 'grupo_sanguineo', 'activo']
    list_filter = ['activo', 'control_prenatal', 'grupo_sanguineo']
    search_fields = ['persona__nombre', 'persona__rut']

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ['persona', 'registro_medico', 'especialidad', 'anos_experiencia', 'activo']
    list_filter = ['activo', 'especialidad']
    search_fields = ['persona__nombre', 'registro_medico']

@admin.register(Matrona)
class MatronaAdmin(admin.ModelAdmin):
    list_display = ['persona', 'registro_medico', 'especialidad', 'anos_experiencia', 'activo']
    list_filter = ['activo', 'especialidad']
    search_fields = ['persona__nombre', 'registro_medico']

@admin.register(TENS)
class TENSAdmin(admin.ModelAdmin):
    list_display = ['persona', 'nivel', 'certificacion', 'anos_experiencia', 'activo']
    list_filter = ['activo', 'nivel', 'certificacion']
    search_fields = ['persona__nombre']