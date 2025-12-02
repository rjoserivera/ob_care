"""
gestionApp/views.py - VISTAS COMPLETAS PARA PERSONAS
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from gestionApp.models import Persona
from gestionApp.forms.Gestion_form import PersonaForm


# ============================================
# VISTA: LISTADO DE PERSONAS
# ============================================

@login_required
def persona_list(request):
    """
    Listado de todas las personas del sistema
    Permite búsqueda por RUT, nombre y email
    Permite filtrar por estado (activo/inactivo)
    """
    personas = Persona.objects.all().order_by('-id')
    
    # Búsqueda
    query = request.GET.get('q', '').strip()
    if query:
        personas = personas.filter(
            Q(Rut__icontains=query) |
            Q(Nombre__icontains=query) |
            Q(Apellido_Paterno__icontains=query) |
            Q(Apellido_Materno__icontains=query) |
            Q(Email__icontains=query) |
            Q(Telefono__icontains=query)
        )
    
    # Filtrar por estado
    activo = request.GET.get('activo', '').strip()
    if activo == '1':
        personas = personas.filter(Activo=True)
    elif activo == '0':
        personas = personas.filter(Activo=False)
    
    context = {
        'personas': personas,
        'query': query,
    }
    
    return render(request, 'Gestion/Data/persona_list.html', context)


# ============================================
# VISTA: REGISTRAR NUEVA PERSONA
# ============================================

@login_required
def registrar_persona(request):
    """
    Vista para registrar una nueva persona en el sistema
    """
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            persona = form.save()
            messages.success(
                request, 
                f'✅ Persona {persona.Nombre} {persona.Apellido_Paterno} registrada correctamente.'
            )
            # Redirigir al detalle de la persona creada
            return redirect('gestion:detalle_persona', pk=persona.pk)
        else:
            # Los errores del formulario se mostrarán automáticamente
            messages.error(request, '❌ Por favor corrige los errores en el formulario.')
    else:
        form = PersonaForm()
    
    context = {
        'form': form,
        'titulo': 'Registrar Nueva Persona',
    }
    
    return render(request, 'Gestion/Formularios/registrar_persona.html', context)


# ============================================
# VISTA: DETALLE DE PERSONA
# ============================================

@login_required
def detalle_persona(request, pk):
    """
    Ver detalle completo de una persona
    """
    persona = get_object_or_404(Persona, pk=pk)
    
    context = {
        'persona': persona,
        'titulo': f'Detalle de {persona.Nombre}',
    }
    
    return render(request, 'Gestion/Data/detalle_persona.html', context)


# ============================================
# VISTA: EDITAR PERSONA
# ============================================

@login_required
def editar_persona(request, pk):
    """
    Editar datos de una persona existente
    """
    persona = get_object_or_404(Persona, pk=pk)
    
    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=persona)
        if form.is_valid():
            persona = form.save()
            messages.success(
                request, 
                f'✅ Persona {persona.Nombre} {persona.Apellido_Paterno} actualizada correctamente.'
            )
            return redirect('gestion:detalle_persona', pk=persona.pk)
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario.')
    else:
        form = PersonaForm(instance=persona)
    
    context = {
        'form': form,
        'persona': persona,
        'titulo': f'Editar {persona.Nombre}',
        'editando': True,
    }
    
    return render(request, 'Gestion/Formularios/editar_persona.html', context)


# ============================================
# VISTA: DESACTIVAR PERSONA
# ============================================

@login_required
def desactivar_persona(request, pk):
    """
    Desactivar una persona (cambiar estado a inactivo)
    """
    persona = get_object_or_404(Persona, pk=pk)
    
    if request.method == 'POST':
        persona.Activo = False
        persona.save()
        messages.success(
            request, 
            f'✅ Persona {persona.Nombre} desactivada correctamente.'
        )
        return redirect('gestion:persona_list')
    
    context = {
        'persona': persona,
        'titulo': f'Desactivar {persona.Nombre}',
    }
    
    return render(request, 'Gestion/Formularios/desactivar_persona.html', context)


# ============================================
# VISTA: ACTIVAR PERSONA
# ============================================

@login_required
def activar_persona(request, pk):
    """
    Activar una persona (cambiar estado a activo)
    """
    persona = get_object_or_404(Persona, pk=pk)
    
    if request.method == 'POST':
        persona.Activo = True
        persona.save()
        messages.success(
            request, 
            f'✅ Persona {persona.Nombre} activada correctamente.'
        )
        return redirect('gestion:persona_list')
    
    context = {
        'persona': persona,
        'titulo': f'Activar {persona.Nombre}',
    }
    
    return render(request, 'Gestion/Formularios/activar_persona.html', context)