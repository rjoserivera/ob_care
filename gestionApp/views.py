# gestionApp/views.py
"""
Vistas para gestionApp - Gestión de Personas
Las personas se convierten en Pacientes cuando se crea una Ficha Obstétrica
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView, DetailView

from .models import Persona
from .forms import PersonaForm, BuscarPersonaForm


# ============================================
# REGISTRAR PERSONA NUEVA
# ============================================

@login_required
def registrar_persona(request):
    """
    Registrar una Persona nueva en el sistema
    NO es paciente aún (se vuelve paciente al crear ficha)
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
                    f"✅ Persona {persona.Nombre} {persona.Apellido_Paterno} registrada"
                )
                
                return redirect('gestion:detalle_persona', pk=persona.pk)
                
            except Exception as e:
                messages.error(request, f"❌ Error: {str(e)}")
        else:
            messages.error(request, "❌ Por favor corrige los errores en el formulario.")
    
    else:
        form = PersonaForm()
    
    context = {
        'form': form,
        'titulo': 'Registrar Nueva Persona',
    }
    
    return render(request, 'Gestion/registrar_persona.html', context)


# ============================================
# EDITAR PERSONA
# ============================================

@login_required
def editar_persona(request, pk):
    """Editar datos de una Persona"""
    
    persona = get_object_or_404(Persona, pk=pk, Activo=True)
    
    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=persona)
        
        if form.is_valid():
            persona = form.save()
            messages.success(request, f"✅ Persona actualizada")
            return redirect('gestion:detalle_persona', pk=persona.pk)
        else:
            messages.error(request, "❌ Por favor corrige los errores.")
    
    else:
        form = PersonaForm(instance=persona)
    
    context = {
        'form': form,
        'persona': persona,
        'titulo': f'Editar: {persona.Nombre} {persona.Apellido_Paterno}',
        'es_edicion': True,
    }
    
    return render(request, 'Gestion/registrar_persona.html', context)


# ============================================
# DETALLE DE PERSONA
# ============================================

@login_required
def detalle_persona(request, pk):
    """Ver detalles de una Persona"""
    
    persona = get_object_or_404(Persona, pk=pk, Activo=True)
    
    # Verificar si es paciente
    from .models import Paciente
    try:
        paciente = Paciente.objects.get(persona=persona)
        es_paciente = True
    except Paciente.DoesNotExist:
        paciente = None
        es_paciente = False
    
    context = {
        'persona': persona,
        'paciente': paciente,
        'es_paciente': es_paciente,
        'titulo': f'{persona.Nombre} {persona.Apellido_Paterno}',
    }
    
    return render(request, 'Gestion/detalle_persona.html', context)


# ============================================
# LISTAR PERSONAS
# ============================================

@login_required
def persona_list(request):
    """Listar todas las personas activas"""
    
    personas = Persona.objects.filter(
        Activo=True
    ).order_by('Nombre')
    
    # Filtro opcional por estado (paciente o no)
    es_paciente = request.GET.get('es_paciente')
    
    if es_paciente == '1':
        # Solo personas que son pacientes
        from .models import Paciente
        pacientes_ids = Paciente.objects.values_list('persona_id', flat=True)
        personas = personas.filter(id__in=pacientes_ids)
    
    elif es_paciente == '0':
        # Solo personas que NO son pacientes
        from .models import Paciente
        pacientes_ids = Paciente.objects.values_list('persona_id', flat=True)
        personas = personas.exclude(id__in=pacientes_ids)
    
    context = {
        'personas': personas,
        'titulo': 'Personas del Sistema',
        'total': personas.count(),
    }
    
    return render(request, 'Gestion/lista_personas.html', context)


# ============================================
# BUSCAR PERSONA
# ============================================

@login_required
def buscar_persona(request):
    """Buscar una Persona por RUT o nombre"""
    
    query = request.GET.get('q', '').strip()
    personas = []
    
    if query and len(query) >= 2:
        personas = Persona.objects.filter(
            Q(Rut__icontains=query) |
            Q(Nombre__icontains=query) |
            Q(Apellido_Paterno__icontains=query) |
            Q(Apellido_Materno__icontains=query),
            Activo=True
        ).order_by('Nombre')
    
    context = {
        'personas': personas,
        'query': query,
        'titulo': 'Búsqueda de Personas',
    }
    
    return render(request, 'Gestion/buscar_persona.html', context)


# ============================================
# ACTIVAR/DESACTIVAR PERSONA
# ============================================

@login_required
def desactivar_persona(request, pk):
    """Desactivar una Persona"""
    
    persona = get_object_or_404(Persona, pk=pk)
    
    if request.method == 'POST':
        persona.Activo = False
        persona.save()
        messages.success(request, f"✅ Persona desactivada")
        return redirect('gestion:persona_list')
    
    context = {
        'persona': persona,
        'accion': 'Desactivar',
    }
    
    return render(request, 'Gestion/confirmar_accion.html', context)


@login_required
def activar_persona(request, pk):
    """Activar una Persona"""
    
    persona = get_object_or_404(Persona, pk=pk)
    
    if request.method == 'POST':
        persona.Activo = True
        persona.save()
        messages.success(request, f"✅ Persona activada")
        return redirect('gestion:persona_list')
    
    context = {
        'persona': persona,
        'accion': 'Activar',
    }
    
    return render(request, 'Gestion/confirmar_accion.html', context)


# ============================================
# API - BÚSQUEDA AJAX
# ============================================

@login_required
def api_buscar_persona(request):
    """API para búsqueda en tiempo real (AJAX)"""
    
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 2:
        return JsonResponse({'resultados': []})
    
    personas = Persona.objects.filter(
        Q(Rut__icontains=query) |
        Q(Nombre__icontains=query) |
        Q(Apellido_Paterno__icontains=query),
        Activo=True
    ).values('id', 'Rut', 'Nombre', 'Apellido_Paterno')[:15]
    
    resultados = [
        {
            'id': p['id'],
            'rut': p['Rut'],
            'nombre_completo': f"{p['Nombre']} {p['Apellido_Paterno']}",
            'display': f"{p['Rut']} - {p['Nombre']} {p['Apellido_Paterno']}",
        }
        for p in personas
    ]
    
    return JsonResponse({'resultados': resultados})