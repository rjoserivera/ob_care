from django.contrib import admin
from .models import PersonalTurno, Notificacion, AsignacionPersonal, Sala

@admin.register(PersonalTurno)
class PersonalTurnoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'estado', 'fecha_inicio_turno', 'fecha_fin_turno')
    list_filter = ('rol', 'estado')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name')

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'titulo', 'destinatario', 'estado', 'timestamp_envio')
    list_filter = ('tipo', 'estado')

@admin.register(AsignacionPersonal)
class AsignacionPersonalAdmin(admin.ModelAdmin):
    list_display = ('proceso', 'personal', 'rol_en_proceso', 'timestamp_notificacion')

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'estado')
