# matronaApp/views.py
"""
Vistas para matronaApp - Gestión de Fichas Obstétricas
Al crear ficha, se crean automáticamente: Paciente + IngresoPaciente
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone

from gestionApp.models import Persona, Paciente
from .models import FichaObstetrica, IngresoPaciente, MedicamentoFicha
from .forms import FichaObstetricaForm, MedicamentoFichaForm
from datetime import date


# ============================================
# MENÚ PRINCIPAL
# ============================================

@login_required
def menu_matrona(request):
    """Menú principal del módulo Matrona"""
    hoy = timezone.now().date()
    
    context = {
        'total_fichas': FichaObstetrica.objects.filter(activa=True).count(),
        'fichas_hoy': FichaObstetrica.objects.filter(
            fecha_creacion__date=hoy,
            activa=True
        ).count(),
    }
    
    return render(request, 'Matrona/menu_matrona.html', context)


# ============================================
# FICHAS OBSTÉTRICAS
# ============================================

@login_required
def seleccionar_persona_ficha(request):
    """
    Buscar una Persona para crear su Ficha Obstétrica
    """
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
    
    return render(request, 'Matrona/seleccionar_persona_ficha.html', {
        'personas': personas,
        'query': query
    })


@login_required
@transaction.atomic
def crear_ficha_obstetrica(request, persona_pk):
    """
    Crear Ficha Obstétrica para una Persona
    
    AUTOMÁTICAMENTE CREA:
    1. Paciente (si no existe)
    2. IngresoPaciente
    3. FichaObstetrica
    
    Todo en una transacción atómica
    """
    
    persona = get_object_or_404(Persona, pk=persona_pk, Activo=True)
    
    if request.method == 'POST':
        form = FichaObstetricaForm(request.POST)
        
        if form.is_valid():
            try:
                # ────────────────────────────────────────
                # PASO 1: CREAR PACIENTE (si no existe)
                # ────────────────────────────────────────
                paciente, creado = Paciente.objects.get_or_create(
                    persona=persona,
                    defaults={
                        'paridad': '',
                        'control_prenatal': False,
                        'Alergias': '',
                        'Peso': None,
                        'Talla': None,
                        'IMC': None,
                        'activo': True,
                        'fecha_registro': timezone.now(),
                    }
                )
                
                if creado:
                    messages.info(request, f"ℹ️ Paciente creado para {persona.Nombre}")
                
                # ────────────────────────────────────────
                # PASO 2: CREAR INGRESOPACIENTE
                # ────────────────────────────────────────
                ingreso, _ = IngresoPaciente.objects.get_or_create(
                    paciente=paciente,
                    defaults={
                        'motivo_ingreso': 'Creación de ficha obstétrica',
                        'fecha_ingreso': date.today(),
                        'hora_ingreso': timezone.now().time(),
                        'edad_gestacional_semanas': form.cleaned_data.get('edad_gestacional_semanas'),
                        'derivacion': '',
                        'observaciones': '',
                        'numero_ficha': form.cleaned_data.get('numero_ficha', ''),
                        'activo': True,
                    }
                )
                
                # ────────────────────────────────────────
                # PASO 3: CREAR FICHA OBSTÉTRICA
                # ────────────────────────────────────────
                ficha = form.save(commit=False)
                ficha.paciente = paciente
                ficha.matrona_responsable = request.user.matrona if hasattr(request.user, 'matrona') else None
                ficha.save()
                
                messages.success(
                    request,
                    f"✅ Ficha obstétrica {ficha.numero_ficha} creada exitosamente"
                )
                
                return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
                
            except Exception as e:
                # Si falla algo, se revierte todo gracias a @transaction.atomic
                messages.error(request, f"❌ Error: {str(e)}")
        else:
            messages.error(request, "❌ Por favor corrige los errores en el formulario.")
    
    else:
        form = FichaObstetricaForm(initial={
            'edad_gestacional_semanas': None,
        })
    
    context = {
        'form': form,
        'persona': persona,
        'titulo': f'Crear Ficha Obstétrica - {persona.Nombre} {persona.Apellido_Paterno}',
    }
    
    return render(request, 'Matrona/crear_ficha_obstetrica.html', context)


@login_required
def detalle_ficha(request, ficha_pk):
    """Ver detalle de una Ficha Obstétrica"""
    
    ficha = get_object_or_404(
        FichaObstetrica.objects.select_related(
            'paciente__persona',
            'matrona_responsable'
        ).prefetch_related('medicamentos'),
        pk=ficha_pk
    )
    
    medicamentos = ficha.medicamentos.filter(activo=True)
    
    context = {
        'ficha': ficha,
        'paciente': ficha.paciente,
        'persona': ficha.paciente.persona,
        'medicamentos': medicamentos,
    }
    
    return render(request, 'Matrona/detalle_ficha.html', context)


@login_required
def editar_ficha(request, ficha_pk):
    """Editar una Ficha Obstétrica"""
    
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk)
    
    if request.method == 'POST':
        form = FichaObstetricaForm(request.POST, instance=ficha)
        
        if form.is_valid():
            ficha = form.save()
            messages.success(request, f"✅ Ficha {ficha.numero_ficha} actualizada")
            return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
        else:
            messages.error(request, "❌ Por favor corrige los errores.")
    
    else:
        form = FichaObstetricaForm(instance=ficha)
    
    context = {
        'form': form,
        'ficha': ficha,
        'persona': ficha.paciente.persona,
        'titulo': f'Editar Ficha - {ficha.numero_ficha}',
        'es_edicion': True,
    }
    
    return render(request, 'Matrona/crear_ficha_obstetrica.html', context)


@login_required
def lista_fichas_persona(request, persona_pk):
    """Listar todas las fichas de una persona"""
    
    persona = get_object_or_404(Persona, pk=persona_pk, Activo=True)
    
    try:
        paciente = Paciente.objects.get(persona=persona)
        fichas = FichaObstetrica.objects.filter(
            paciente=paciente
        ).order_by('-fecha_creacion')
    except Paciente.DoesNotExist:
        fichas = []
    
    context = {
        'persona': persona,
        'fichas': fichas,
        'titulo': f'Fichas de {persona.Nombre} {persona.Apellido_Paterno}',
    }
    
    return render(request, 'Matrona/lista_fichas.html', context)


@login_required
def lista_todas_fichas(request):
    """Listar todas las fichas del sistema"""
    
    fichas = FichaObstetrica.objects.select_related(
        'paciente__persona',
        'matrona_responsable'
    ).order_by('-fecha_creacion')
    
    # Filtro opcional
    activa = request.GET.get('activa')
    if activa == '1':
        fichas = fichas.filter(activa=True)
    elif activa == '0':
        fichas = fichas.filter(activa=False)
    
    context = {
        'fichas': fichas,
        'titulo': 'Todas las Fichas Obstétricas',
    }
    
    return render(request, 'Matrona/todas_fichas.html', context)


# ============================================
# MEDICAMENTOS EN FICHA
# ============================================

@login_required
def agregar_medicamento_ficha(request, ficha_pk):
    """Agregar medicamento a una ficha"""
    
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk)
    
    if request.method == 'POST':
        form = MedicamentoFichaForm(request.POST)
        
        if form.is_valid():
            medicamento = form.save(commit=False)
            medicamento.ficha = ficha
            medicamento.save()
            
            messages.success(
                request,
                f"✅ Medicamento {medicamento.nombre_medicamento} agregado"
            )
            return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
        else:
            messages.error(request, "❌ Por favor corrige los errores.")
    
    else:
        form = MedicamentoFichaForm()
    
    context = {
        'form': form,
        'ficha': ficha,
        'titulo': 'Agregar Medicamento',
    }
    
    return render(request, 'Matrona/agregar_medicamento.html', context)


@login_required
def editar_medicamento_ficha(request, medicamento_pk):
    """Editar medicamento de una ficha"""
    
    medicamento = get_object_or_404(MedicamentoFicha, pk=medicamento_pk)
    ficha = medicamento.ficha
    
    if request.method == 'POST':
        form = MedicamentoFichaForm(request.POST, instance=medicamento)
        
        if form.is_valid():
            medicamento = form.save()
            messages.success(request, f"✅ Medicamento actualizado")
            return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
        else:
            messages.error(request, "❌ Por favor corrige los errores.")
    
    else:
        form = MedicamentoFichaForm(instance=medicamento)
    
    context = {
        'form': form,
        'medicamento': medicamento,
        'ficha': ficha,
        'titulo': 'Editar Medicamento',
    }
    
    return render(request, 'Matrona/agregar_medicamento.html', context)


@login_required
def eliminar_medicamento_ficha(request, medicamento_pk):
    """Eliminar medicamento (desactivar)"""
    
    medicamento = get_object_or_404(MedicamentoFicha, pk=medicamento_pk)
    ficha = medicamento.ficha
    
    if request.method == 'POST':
        medicamento.activo = False
        medicamento.save()
        
        messages.success(request, f"✅ Medicamento eliminado")
        return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
    
    context = {
        'medicamento': medicamento,
        'ficha': ficha,
    }
    
    return render(request, 'Matrona/confirmar_eliminar_medicamento.html', context)


# ============================================
# API - BÚSQUEDA
# ============================================

@login_required
def buscar_persona_api(request):
    """API para buscar personas por AJAX"""
    
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 2:
        return JsonResponse({'resultados': []})
    
    personas = Persona.objects.filter(
        Q(Rut__icontains=query) |
        Q(Nombre__icontains=query) |
        Q(Apellido_Paterno__icontains=query),
        Activo=True
    ).values('id', 'Rut', 'Nombre', 'Apellido_Paterno', 'Apellido_Materno')[:10]
    
    resultados = [
        {
            'id': p['id'],
            'texto': f"{p['Rut']} - {p['Nombre']} {p['Apellido_Paterno']}",
        }
        for p in personas
    ]
    
    return JsonResponse({'resultados': resultados})