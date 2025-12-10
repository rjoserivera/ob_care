# gestionApp/views.py
"""
Vistas para gestionApp - Gestión de Personas
Las personas se convierten en Pacientes cuando se crea una Ficha Obstétrica
ACTUALIZADO: Cálculo correcto de edad con datetime
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from datetime import date

from .models import Persona
from .forms import PersonaForm, BuscarPersonaForm
from authentication.decorators import roles_required


# ============================================
# FUNCIÓN HELPER: Calcular Edad
# ============================================

def calcular_edad(fecha_nacimiento):
    """
    Calcula la edad correctamente basada en la fecha de nacimiento
    
    Parámetros:
        fecha_nacimiento: date object
    
    Retorna:
        int: edad en años
    """
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year
    
    # Restar 1 si el cumpleaños aún no ha ocurrido este año
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    
    return edad


# ============================================
# REGISTRAR PERSONA NUEVA
# ============================================

@login_required
@roles_required('medico', 'administrador')
def registrar_persona(request):
    """
    Registrar una Persona nueva en el sistema
    NO es paciente aún (se vuelve paciente al crear ficha)
    
    Restricción: Solo Médico y Administrador pueden registrar personas
    """
    
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        
        if form.is_valid():
            try:
                persona = form.save(commit=False)
                persona.Activo = True
                persona.save()
                
                messages.success(
                    request,
                    f"✅ Persona {persona.Nombre} {persona.Apellido_Paterno} registrada exitosamente"
                )
                
                # Redirigir al detalle de la persona
                return redirect('gestion:detalle_persona', pk=persona.pk)
                
            except Exception as e:
                messages.error(request, f"❌ Error al registrar: {str(e)}")
        else:
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"❌ {field}: {error}")
    
    else:
        form = PersonaForm()
    
    context = {
        'form': form,
        'titulo': 'Registrar Nueva Persona',
        'subtitulo': 'Complete los datos básicos de la persona',
        'button_text': 'Registrar Persona',
    }
    
    return render(request, 'Gestion/Formularios/registrar_persona.html', context)


# ============================================
# DETALLE PERSONA
# ============================================

@login_required
def detalle_persona(request, pk):
    """
    Ver detalles de una Persona
    Calcula la edad correctamente
    """
    
    persona = get_object_or_404(Persona, pk=pk)
    
    # ✅ CALCULAR EDAD CORRECTAMENTE
    edad = None
    if persona.Fecha_nacimiento:
        edad = calcular_edad(persona.Fecha_nacimiento)
    
    context = {
        'persona': persona,
        'edad': edad,
        'titulo': f'{persona.Nombre} {persona.Apellido_Paterno}',
    }
    
    return render(request, 'Gestion/detalle_persona.html', context)


# ============================================
# EDITAR PERSONA
# ============================================

@login_required
@roles_required('medico', 'administrador')
def editar_persona(request, pk):
    """
    Editar datos de una Persona
    Restricción: Solo Médico y Administrador
    """
    
    persona = get_object_or_404(Persona, pk=pk, Activo=True)
    
    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=persona)
        
        if form.is_valid():
            persona = form.save()
            messages.success(request, f"✅ Datos de {persona.Nombre} actualizados")
            return redirect('gestion:detalle_persona', pk=persona.pk)
        else:
            messages.error(request, "❌ Por favor corrige los errores.")
    
    else:
        form = PersonaForm(instance=persona)
    
    context = {
        'form': form,
        'persona': persona,
        'titulo': f'Editar: {persona.Nombre} {persona.Apellido_Paterno}',
        'button_text': 'Guardar Cambios',
    }
    
    return render(request, 'Gestion/Formularios/registrar_persona.html', context)


# ============================================
# LISTAR PERSONAS
# ============================================

@login_required
def persona_list(request):
    """Listar todas las personas activas"""
    
    query = request.GET.get('q', '').strip()
    
    personas = Persona.objects.filter(Activo=True)
    
    if query:
        personas = personas.filter(
            Q(Nombre__icontains=query) |
            Q(Apellido_Paterno__icontains=query) |
            Q(Apellido_Materno__icontains=query) |
            Q(Rut__icontains=query)
        )
    
    context = {
        'personas': personas,
        'query': query,
        'total': personas.count(),
        'titulo': 'Listado de Personas',
    }
    
    return render(request, 'Gestion/lista_personas.html', context)


# ============================================
# BUSCAR PERSONA
# ============================================

@login_required
def buscar_persona(request):
    """Búsqueda avanzada de personas"""
    
    query = request.GET.get('q', '').strip()
    personas = []
    
    if query and len(query) >= 2:
        personas = Persona.objects.filter(
            Q(Nombre__icontains=query) |
            Q(Apellido_Paterno__icontains=query) |
            Q(Apellido_Materno__icontains=query) |
            Q(Rut__icontains=query),
            Activo=True
        )
    
    context = {
        'personas': personas,
        'query': query,
        'titulo': 'Buscar Persona',
    }
    
    return render(request, 'Gestion/buscar_persona.html', context)


# ============================================
# DESACTIVAR PERSONA
# ============================================

@login_required
@roles_required('administrador')
def desactivar_persona(request, pk):
    """
    Desactivar una Persona (no eliminar)
    Restricción: Solo Administrador
    """
    
    persona = get_object_or_404(Persona, pk=pk)
    persona.Activo = False
    persona.save()
    
    messages.success(request, f"✅ Persona {persona.Nombre} desactivada")
    return redirect('gestion:persona_list')


# ============================================
# ACTIVAR PERSONA
# ============================================

@login_required
@roles_required('administrador')
def activar_persona(request, pk):
    """
    Activar una Persona desactivada
    Restricción: Solo Administrador
    """
    
    persona = get_object_or_404(Persona, pk=pk)
    persona.Activo = True
    persona.save()
    
    messages.success(request, f"✅ Persona {persona.Nombre} activada")
    return redirect('gestion:persona_list')


# ============================================
# API - BÚSQUEDA AJAX
# ============================================

@login_required
def api_buscar_persona(request):
    """
    API para búsqueda AJAX de personas
    Retorna JSON con edad calculada correctamente
    """
    
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'resultados': []})
    
    personas = Persona.objects.filter(
        Q(Nombre__icontains=query) |
        Q(Apellido_Paterno__icontains=query) |
        Q(Rut__icontains=query),
        Activo=True
    )[:10]
    
    resultados = []
    for p in personas:
        edad = calcular_edad(p.Fecha_nacimiento) if p.Fecha_nacimiento else 'N/A'
        resultados.append({
            'id': p.pk,
            'nombre': f'{p.Nombre} {p.Apellido_Paterno}',
            'rut': p.Rut,
            'edad': edad,
        })
    
    return JsonResponse({'resultados': resultados})