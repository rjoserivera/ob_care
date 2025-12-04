"""
ingresoPartoApp/views.py
Vistas para gestionar Fichas de Ingreso a Parto
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from matronaApp.models import FichaObstetrica
from .models import FichaParto
from .forms.forms import FichaPartoForm


# ============================================
# FICHA PARTO - CREAR
# ============================================

@login_required
def crear_ficha_parto(request, ficha_obstetrica_pk):
    """
    Crear ficha de parto (ingreso a sala)
    URL: /ingreso-parto/crear/<ficha_obstetrica_pk>/
    """
    ficha_obstetrica = get_object_or_404(
        FichaObstetrica,
        pk=ficha_obstetrica_pk,
        activa=True
    )
    paciente = ficha_obstetrica.paciente
    
    if request.method == 'POST':
        form = FichaPartoForm(request.POST)
        if form.is_valid():
            ficha = form.save(commit=False)
            ficha.ficha_obstetrica = ficha_obstetrica
            ficha.numero_ficha_parto = f"FP-{FichaParto.objects.count() + 1:06d}"
            ficha.save()
            messages.success(
                request,
                f'✅ Ficha de Parto {ficha.numero_ficha_parto} creada'
            )
            # Ir al primer paso del registro de parto
            return redirect('partos:crear_registro_parto_paso1', ficha_parto_pk=ficha.pk)
    else:
        form = FichaPartoForm()
    
    context = {
        'form': form,
        'ficha_obstetrica': ficha_obstetrica,
        'paciente': paciente,
        'titulo': 'Crear Ficha de Ingreso a Parto'
    }
    return render(request, 'IngesoParto/form_ingreso_parto.html', context)


# ============================================
# FICHA PARTO - EDITAR
# ============================================

@login_required
def editar_ficha_parto(request, ficha_parto_pk):
    """
    Editar ficha de parto
    URL: /ingreso-parto/<ficha_parto_pk>/editar/
    """
    ficha = get_object_or_404(FichaParto, pk=ficha_parto_pk)
    ficha_obstetrica = ficha.ficha_obstetrica
    paciente = ficha_obstetrica.paciente
    
    if request.method == 'POST':
        form = FichaPartoForm(request.POST, instance=ficha)
        if form.is_valid():
            ficha = form.save()
            messages.success(request, f'✅ Ficha actualizada')
            return redirect('ingreso_parto:detalle_ficha', ficha_parto_pk=ficha.pk)
    else:
        form = FichaPartoForm(instance=ficha)
    
    context = {
        'form': form,
        'ficha': ficha,
        'ficha_obstetrica': ficha_obstetrica,
        'paciente': paciente,
        'titulo': 'Editar Ficha de Ingreso a Parto'
    }
    return render(request, 'IngesoParto/form_ingreso_parto.html', context)


# ============================================
# FICHA PARTO - DETALLE
# ============================================

@login_required
def detalle_ficha_parto(request, ficha_parto_pk):
    """
    Ver detalle de ficha de parto
    URL: /ingreso-parto/<ficha_parto_pk>/
    """
    ficha = get_object_or_404(FichaParto, pk=ficha_parto_pk)
    ficha_obstetrica = ficha.ficha_obstetrica
    paciente = ficha_obstetrica.paciente
    
    context = {
        'ficha': ficha,
        'ficha_obstetrica': ficha_obstetrica,
        'paciente': paciente,
        'titulo': f'Ficha {ficha.numero_ficha_parto}'
    }
    return render(request, 'IngesoParto/detalle_ficha_parto.html', context)


# ============================================
# FICHA PARTO - LISTA
# ============================================

@login_required
def lista_fichas_parto(request):
    """
    Listar todas las fichas de ingreso a parto
    URL: /ingreso-parto/fichas/
    """
    fichas = FichaParto.objects.select_related(
        'ficha_obstetrica__paciente__persona'
    ).order_by('-fecha_ingreso')
    
    # Búsqueda
    search_query = request.GET.get('q', '')
    if search_query:
        fichas = fichas.filter(
            Q(ficha_obstetrica__paciente__persona__Nombre__icontains=search_query) |
            Q(ficha_obstetrica__paciente__persona__Rut__icontains=search_query) |
            Q(numero_ficha_parto__icontains=search_query)
        )
    
    context = {
        'fichas': fichas,
        'titulo': 'Fichas de Ingreso a Parto',
        'search_query': search_query
    }
    return render(request, 'IngesoParto/lista_fichas_parto.html', context)


# ============================================
# MENU INGRESO PARTO
# ============================================

@login_required
def menu_ingreso_parto(request):
    """
    Menu principal de ingreso a parto
    URL: /ingreso-parto/
    """
    total_fichas = FichaParto.objects.count()
    fichas_recientes = FichaParto.objects.order_by('-fecha_ingreso')[:5]
    
    context = {
        'titulo': 'Ingreso a Parto',
        'total_fichas': total_fichas,
        'fichas_recientes': fichas_recientes
    }
    return render(request, 'IngesoParto/menu_ingreso_parto.html', context)