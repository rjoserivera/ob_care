"""
ingresoPartoApp/views.py
Vistas para Ingreso a Parto - Con Sala de Espera
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

from .models import FichaParto
from .forms.forms import FichaPartoForm
from matronaApp.models import FichaObstetrica


# ============================================
# SALA DE ESPERA
# ============================================

@login_required
def sala_espera_parto(request, ficha_obstetrica_pk):
    """
    Vista de sala de espera mientras se confirma el equipo médico
    URL: /ingreso-parto/sala-espera/<ficha_obstetrica_pk>/
    """
    ficha_obstetrica = get_object_or_404(
        FichaObstetrica.objects.select_related('paciente__persona'),
        pk=ficha_obstetrica_pk
    )
    
    # Verificar si ya tiene ficha de parto
    if hasattr(ficha_obstetrica, 'ficha_parto'):
        messages.info(request, 'Esta paciente ya tiene una ficha de parto activa.')
        return redirect('ingreso_parto:detalle_ficha', ficha_parto_pk=ficha_obstetrica.ficha_parto.pk)
    
    # Determinar si es urgente (ejemplo: por patologías)
    urgente = ficha_obstetrica.eclampsia or ficha_obstetrica.preeclampsia_severa if hasattr(ficha_obstetrica, 'eclampsia') else False
    
    context = {
        'ficha_obstetrica': ficha_obstetrica,
        'titulo': 'Sala de Espera - Proceso de Parto',
        'urgente': urgente,
    }
    
    return render(request, 'IngresoParto/sala_espera_parto.html', context)


# ============================================
# FICHA PARTO - CREAR
# ============================================

@login_required
def crear_ficha_parto(request, ficha_obstetrica_pk):
    """
    Crear ficha de ingreso a parto
    URL: /ingreso-parto/ficha/crear/<ficha_obstetrica_pk>/
    """
    ficha_obstetrica = get_object_or_404(
        FichaObstetrica.objects.select_related('paciente__persona'),
        pk=ficha_obstetrica_pk
    )
    
    # Verificar si ya tiene ficha de parto
    if hasattr(ficha_obstetrica, 'ficha_parto'):
        messages.warning(request, 'Esta paciente ya tiene una ficha de parto.')
        return redirect('ingreso_parto:detalle_ficha', ficha_parto_pk=ficha_obstetrica.ficha_parto.pk)
    
    # Obtener sala si viene desde sala de espera
    sala = request.GET.get('sala', None)
    
    if request.method == 'POST':
        form = FichaPartoForm(request.POST)
        if form.is_valid():
            ficha_parto = form.save(commit=False)
            ficha_parto.ficha_obstetrica = ficha_obstetrica
            
            # Generar número de ficha automático
            ultimo = FichaParto.objects.order_by('-id').first()
            siguiente_num = (ultimo.id + 1) if ultimo else 1
            ficha_parto.numero_ficha_parto = f"FP-{siguiente_num:06d}"
            
            ficha_parto.save()
            
            messages.success(request, f'Ficha de parto {ficha_parto.numero_ficha_parto} creada exitosamente.')
            return redirect('ingreso_parto:detalle_ficha', ficha_parto_pk=ficha_parto.pk)
    else:
        # Pre-llenar fecha y hora actuales
        form = FichaPartoForm(initial={
            'fecha_ingreso': timezone.now().date(),
            'hora_ingreso': timezone.now().time(),
        })
    
    context = {
        'form': form,
        'ficha_obstetrica': ficha_obstetrica,
        'titulo': 'Nueva Ficha de Ingreso a Parto',
        'sala': sala,
    }
    
    return render(request, 'IngresoParto/form_ingreso_parto.html', context)


# ============================================
# FICHA PARTO - EDITAR
# ============================================

@login_required
def editar_ficha_parto(request, ficha_parto_pk):
    """
    Editar ficha de parto existente
    URL: /ingreso-parto/ficha/<ficha_parto_pk>/editar/
    """
    ficha = get_object_or_404(
        FichaParto.objects.select_related('ficha_obstetrica__paciente__persona'),
        pk=ficha_parto_pk
    )
    
    if request.method == 'POST':
        form = FichaPartoForm(request.POST, instance=ficha)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ficha de parto actualizada correctamente.')
            return redirect('ingreso_parto:detalle_ficha', ficha_parto_pk=ficha.pk)
    else:
        form = FichaPartoForm(instance=ficha)
    
    context = {
        'form': form,
        'ficha_obstetrica': ficha.ficha_obstetrica,
        'ficha_parto': ficha,
        'titulo': f'Editar Ficha {ficha.numero_ficha_parto}',
        'es_edicion': True,
    }
    
    return render(request, 'IngresoParto/form_ingreso_parto.html', context)


# ============================================
# FICHA PARTO - DETALLE
# ============================================

@login_required
def detalle_ficha_parto(request, ficha_parto_pk):
    """
    Ver detalle de ficha de parto
    URL: /ingreso-parto/ficha/<ficha_parto_pk>/
    """
    ficha = get_object_or_404(
        FichaParto.objects.select_related('ficha_obstetrica__paciente__persona'),
        pk=ficha_parto_pk
    )
    
    context = {
        'ficha': ficha,
        'ficha_obstetrica': ficha.ficha_obstetrica,
        'titulo': f'Ficha {ficha.numero_ficha_parto}'
    }
    
    return render(request, 'IngresoParto/detalle_ficha_parto.html', context)


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
    
    return render(request, 'IngresoParto/lista_fichas_parto.html', context)


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
    fichas_hoy = FichaParto.objects.filter(fecha_ingreso=timezone.now().date()).count()
    fichas_recientes = FichaParto.objects.select_related(
        'ficha_obstetrica__paciente__persona'
    ).order_by('-fecha_ingreso')[:5]
    
    context = {
        'titulo': 'Ingreso a Parto',
        'total_fichas': total_fichas,
        'fichas_hoy': fichas_hoy,
        'fichas_recientes': fichas_recientes
    }
    
    return render(request, 'IngresoParto/menu_ingreso_parto.html', context)