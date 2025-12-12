"""
gestionApp/admin.py
Administración de personas, pacientes y personal de salud
Los turnos y roles se gestionan desde aquí
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from .models import (
    # Catálogos
    CatalogoSexo,
    CatalogoNacionalidad,
    CatalogoPuebloOriginario,
    CatalogoEstadoCivil,
    CatalogoPrevision,
    CatalogoTurno,
    # Modelos principales
    Persona,
    Paciente,
    PerfilUsuario,
)


# ============================================
# CONFIGURACIÓN GENERAL DEL ADMIN
# ============================================

admin.site.site_header = "🏥 OB_CARE - Administración"
admin.site.site_title = "OB_CARE Admin"
admin.site.index_title = "Panel de Administración"


# ============================================
# CATÁLOGOS - ADMINISTRACIÓN SIMPLE
# ============================================

@admin.register(CatalogoSexo)
class CatalogoSexoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'activo', 'orden']
    list_editable = ['activo', 'orden']
    list_filter = ['activo']
    search_fields = ['nombre', 'codigo']
    ordering = ['orden']


@admin.register(CatalogoNacionalidad)
class CatalogoNacionalidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'activo', 'orden']
    list_editable = ['activo', 'orden']
    list_filter = ['activo']
    search_fields = ['nombre', 'codigo']
    ordering = ['orden']


@admin.register(CatalogoPuebloOriginario)
class CatalogoPuebloOriginarioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'activo', 'orden']
    list_editable = ['activo', 'orden']
    list_filter = ['activo']
    search_fields = ['nombre', 'codigo']
    ordering = ['orden']


@admin.register(CatalogoEstadoCivil)
class CatalogoEstadoCivilAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'activo', 'orden']
    list_editable = ['activo', 'orden']
    list_filter = ['activo']
    search_fields = ['nombre', 'codigo']
    ordering = ['orden']


@admin.register(CatalogoPrevision)
class CatalogoPrevisionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'descripcion', 'activo', 'orden']
    list_editable = ['activo', 'orden']
    list_filter = ['activo']
    search_fields = ['nombre', 'codigo']
    ordering = ['orden']


@admin.register(CatalogoTurno)
class CatalogoTurnoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'hora_inicio', 'hora_fin', 'activo', 'orden']
    list_editable = ['activo', 'orden']
    list_filter = ['activo']
    search_fields = ['nombre', 'codigo']
    ordering = ['orden']


# ============================================
# PERSONA - ADMINISTRACIÓN
# ============================================

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = [
        'rut_formateado', 
        'nombre_completo', 
        'edad_display',
        'Sexo', 
        'Telefono',
        'tiene_usuario',
        'Activo'
    ]
    list_filter = ['Activo', 'Sexo', 'Nacionalidad', 'Inmigrante', 'Discapacidad']
    search_fields = ['Rut', 'Nombre', 'Apellido_Paterno', 'Apellido_Materno', 'Telefono']
    ordering = ['Apellido_Paterno', 'Apellido_Materno', 'Nombre']
    
    fieldsets = (
        ('📋 Identificación', {
            'fields': ('Rut', 'Nombre', 'Apellido_Paterno', 'Apellido_Materno', 'Fecha_nacimiento')
        }),
        ('👤 Datos Demográficos', {
            'fields': ('Sexo', 'Nacionalidad', 'Pueblos_originarios', 'Estado_civil')
        }),
        ('⚠️ Condiciones Especiales', {
            'fields': ('Inmigrante', 'Discapacidad', 'Tipo_de_Discapacidad', 'Privada_de_Libertad', 'Trans_Masculino'),
            'classes': ('collapse',)
        }),
        ('📞 Contacto', {
            'fields': ('Telefono', 'Telefono_emergencia', 'Direccion', 'Comuna', 'Email')
        }),
        ('🔐 Usuario del Sistema', {
            'fields': ('usuario',),
            'classes': ('collapse',),
            'description': 'Solo asignar si esta persona necesita acceso al sistema (personal de salud)'
        }),
        ('Estado', {
            'fields': ('Activo',)
        }),
    )
    
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def edad_display(self, obj):
        edad = obj.edad
        if edad:
            return f"{edad} años"
        return "-"
    edad_display.short_description = "Edad"
    
    def tiene_usuario(self, obj):
        if obj.usuario:
            return format_html('<span style="color: green;">✅ {}</span>', obj.usuario.username)
        return format_html('<span style="color: gray;">—</span>')
    tiene_usuario.short_description = "Usuario Sistema"


# ============================================
# PACIENTE - ADMINISTRACIÓN
# ============================================

class PacienteInline(admin.StackedInline):
    """Inline para crear paciente desde Persona"""
    model = Paciente
    can_delete = False
    verbose_name = "Datos de Paciente"
    verbose_name_plural = "Datos de Paciente"
    
    fieldsets = (
        ('Previsión', {
            'fields': ('prevision', 'numero_ficha_hospital')
        }),
        ('Datos Médicos', {
            'fields': ('grupo_sanguineo', 'tiene_alergias', 'alergias', 'antecedentes_morbidos', 'medicamentos_uso_habitual')
        }),
        ('Observaciones', {
            'fields': ('observaciones', 'activo')
        }),
    )


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = [
        'get_rut',
        'get_nombre',
        'get_edad',
        'prevision',
        'grupo_sanguineo',
        'alergias_badge',
        'activo'
    ]
    list_filter = ['activo', 'prevision', 'grupo_sanguineo', 'tiene_alergias']
    search_fields = [
        'persona__Rut', 
        'persona__Nombre', 
        'persona__Apellido_Paterno',
        'numero_ficha_hospital'
    ]
    ordering = ['persona__Apellido_Paterno', 'persona__Apellido_Materno']
    
    autocomplete_fields = ['persona']
    
    fieldsets = (
        ('👤 Persona', {
            'fields': ('persona',)
        }),
        ('🏥 Previsión', {
            'fields': ('prevision', 'numero_ficha_hospital')
        }),
        ('🩸 Datos Médicos', {
            'fields': ('grupo_sanguineo', 'tiene_alergias', 'alergias')
        }),
        ('📋 Antecedentes', {
            'fields': ('antecedentes_morbidos', 'medicamentos_uso_habitual'),
            'classes': ('collapse',)
        }),
        ('📝 Observaciones', {
            'fields': ('observaciones', 'activo')
        }),
    )
    
    def get_rut(self, obj):
        return obj.persona.rut_formateado
    get_rut.short_description = "RUT"
    get_rut.admin_order_field = 'persona__Rut'
    
    def get_nombre(self, obj):
        return obj.persona.nombre_completo
    get_nombre.short_description = "Nombre"
    get_nombre.admin_order_field = 'persona__Apellido_Paterno'
    
    def get_edad(self, obj):
        edad = obj.persona.edad
        return f"{edad} años" if edad else "-"
    get_edad.short_description = "Edad"
    
    def alergias_badge(self, obj):
        if obj.tiene_alergias:
            return format_html('<span style="color: red; font-weight: bold;">⚠️ SÍ</span>')
        return format_html('<span style="color: green;">No</span>')
    alergias_badge.short_description = "Alergias"


# ============================================
# PERFIL USUARIO (PERSONAL DE SALUD) - ADMINISTRACIÓN
# ============================================

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = [
        'get_username',
        'get_nombre_completo',
        'cargo',
        'rol_badge',
        'turno_actual',
        'disponible_badge',
    ]
    list_filter = ['disponible', 'turno_actual', 'usuario__groups']
    search_fields = [
        'usuario__username',
        'usuario__first_name',
        'usuario__last_name',
        'persona__Nombre',
        'persona__Apellido_Paterno',
        'cargo'
    ]
    list_editable = ['turno_actual']
    
    autocomplete_fields = ['usuario', 'persona']
    
    fieldsets = (
        ('🔐 Usuario del Sistema', {
            'fields': ('usuario',),
            'description': 'Seleccione el usuario de Django (login)'
        }),
        ('👤 Datos Personales', {
            'fields': ('persona',),
            'description': 'Vincule con una Persona para tener RUT, nombre, etc.'
        }),
        ('💼 Datos Laborales', {
            'fields': ('cargo', 'telefono_institucional')
        }),
        ('🕐 Turno y Disponibilidad', {
            'fields': ('turno_actual', 'disponible'),
            'description': '⚡ Cambie el turno actual del personal aquí'
        }),
    )
    
    def get_username(self, obj):
        return obj.usuario.username
    get_username.short_description = "Usuario"
    get_username.admin_order_field = 'usuario__username'
    
    def get_nombre_completo(self, obj):
        if obj.persona:
            return obj.persona.nombre_completo
        return obj.usuario.get_full_name() or "-"
    get_nombre_completo.short_description = "Nombre"
    
    def rol_badge(self, obj):
        rol = obj.rol_principal
        colores = {
            'Médico': '#e74c3c',
            'Matrona': '#e91e8c',
            'TENS': '#3498db',
            'Administrador': '#f39c12',
            'Sin rol asignado': '#95a5a6'
        }
        color = colores.get(rol, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color, rol
        )
    rol_badge.short_description = "Rol"
    
    def disponible_badge(self, obj):
        if obj.disponible:
            return format_html('<span style="color: green; font-weight: bold;">✅ Disponible</span>')
        return format_html('<span style="color: red;">❌ No disponible</span>')
    disponible_badge.short_description = "Estado"


# ============================================
# EXTENDER USER ADMIN PARA MOSTRAR PERFIL
# ============================================

class PerfilUsuarioInline(admin.StackedInline):
    """Inline para ver/editar perfil desde User"""
    model = PerfilUsuario
    can_delete = False
    verbose_name = "Perfil de Personal"
    verbose_name_plural = "Perfil de Personal"
    
    fieldsets = (
        ('Datos Laborales', {
            'fields': ('persona', 'cargo', 'telefono_institucional')
        }),
        ('Turno y Disponibilidad', {
            'fields': ('turno_actual', 'disponible')
        }),
    )


# Desregistrar el UserAdmin por defecto y registrar uno personalizado
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """UserAdmin extendido para incluir perfil y facilitar gestión de roles"""
    
    inlines = [PerfilUsuarioInline]
    
    list_display = [
        'username', 
        'get_full_name',
        'email', 
        'get_grupos',
        'get_turno',
        'is_active',
        'is_staff'
    ]
    list_filter = ['is_active', 'is_staff', 'groups']
    
    def get_grupos(self, obj):
        grupos = obj.groups.all()
        if grupos:
            badges = []
            colores = {
                'Medicos': '#e74c3c',
                'Matronas': '#e91e8c',
                'TENS': '#3498db',
                'Administradores': '#f39c12',
            }
            for g in grupos:
                color = colores.get(g.name, '#95a5a6')
                badges.append(
                    f'<span style="background-color: {color}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px; margin-right: 3px;">{g.name}</span>'
                )
            return format_html(''.join(badges))
        return format_html('<span style="color: gray;">Sin grupo</span>')
    get_grupos.short_description = "Rol(es)"
    
    def get_turno(self, obj):
        try:
            perfil = obj.perfil
            if perfil.turno_actual:
                return perfil.turno_actual.nombre
            return "-"
        except PerfilUsuario.DoesNotExist:
            return "-"
    get_turno.short_description = "Turno"
    
    # Agregar acciones para asignar turnos masivamente
    actions = ['asignar_turno_manana', 'asignar_turno_tarde', 'asignar_turno_noche', 'marcar_disponible', 'marcar_no_disponible']
    
    def asignar_turno_manana(self, request, queryset):
        turno = CatalogoTurno.objects.filter(codigo='MANANA').first()
        if turno:
            count = 0
            for user in queryset:
                perfil, created = PerfilUsuario.objects.get_or_create(usuario=user)
                perfil.turno_actual = turno
                perfil.save()
                count += 1
            self.message_user(request, f"✅ {count} usuarios asignados al turno Mañana")
    asignar_turno_manana.short_description = "🌅 Asignar Turno Mañana"
    
    def asignar_turno_tarde(self, request, queryset):
        turno = CatalogoTurno.objects.filter(codigo='TARDE').first()
        if turno:
            count = 0
            for user in queryset:
                perfil, created = PerfilUsuario.objects.get_or_create(usuario=user)
                perfil.turno_actual = turno
                perfil.save()
                count += 1
            self.message_user(request, f"✅ {count} usuarios asignados al turno Tarde")
    asignar_turno_tarde.short_description = "🌇 Asignar Turno Tarde"
    
    def asignar_turno_noche(self, request, queryset):
        turno = CatalogoTurno.objects.filter(codigo='NOCHE').first()
        if turno:
            count = 0
            for user in queryset:
                perfil, created = PerfilUsuario.objects.get_or_create(usuario=user)
                perfil.turno_actual = turno
                perfil.save()
                count += 1
            self.message_user(request, f"✅ {count} usuarios asignados al turno Noche")
    asignar_turno_noche.short_description = "🌙 Asignar Turno Noche"
    
    def marcar_disponible(self, request, queryset):
        count = 0
        for user in queryset:
            perfil, created = PerfilUsuario.objects.get_or_create(usuario=user)
            perfil.disponible = True
            perfil.save()
            count += 1
        self.message_user(request, f"✅ {count} usuarios marcados como disponibles")
    marcar_disponible.short_description = "✅ Marcar como Disponible"
    
    def marcar_no_disponible(self, request, queryset):
        count = 0
        for user in queryset:
            perfil, created = PerfilUsuario.objects.get_or_create(usuario=user)
            perfil.disponible = False
            perfil.save()
            count += 1
        self.message_user(request, f"✅ {count} usuarios marcados como NO disponibles")
    marcar_no_disponible.short_description = "❌ Marcar como No Disponible"