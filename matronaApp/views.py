"""
matronaApp/views.py
Vistas para gestionar Fichas Obstétricas
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from gestionApp.models import Paciente, Persona
from .models import FichaObstetrica, MedicamentoFicha
from .forms.ficha_obstetrica_form import FichaObstetricaForm, MedicamentoFichaForm


# ============================================
# FICHA OBSTÉTRICA - CREAR
# ============================================

@login_required
def crear_ficha_obstetrica(request, paciente_pk):
    """
    Crear nueva ficha obstétrica
    URL: /matrona/ficha/crear/<paciente_pk>/
    """
    paciente = get_object_or_404(Paciente, pk=paciente_pk, activo=True)
    persona = paciente.persona
    
    if request.method == 'POST':
        form = FichaObstetricaForm(request.POST)
        if form.is_valid():
            ficha = form.save(commit=False)
            ficha.paciente = paciente
            ficha.numero_ficha = f"FO-{FichaObstetrica.objects.count() + 1:06d}"
            ficha.save()
            messages.success(
                request,
                f'✅ Ficha Obstétrica {ficha.numero_ficha} creada exitosamente'
            )
            return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario')
    else:
        form = FichaObstetricaForm()
    
    context = {
        'form': form,
        'paciente': paciente,
        'persona': persona,
        'titulo': 'Crear Ficha Obstétrica',
        'accion': 'crear'
    }
    return render(request, 'Matrona/form_obstetrica_materna.html', context)


# ============================================
# FICHA OBSTÉTRICA - EDITAR
# ============================================

@login_required
def editar_ficha_obstetrica(request, ficha_pk):
    """
    Editar ficha obstétrica existente
    URL: /matrona/ficha/<ficha_pk>/editar/
    """
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk, activa=True)
    paciente = ficha.paciente
    persona = paciente.persona
    
    if request.method == 'POST':
        form = FichaObstetricaForm(request.POST, instance=ficha)
        if form.is_valid():
            ficha = form.save()
            messages.success(request, f'✅ Ficha {ficha.numero_ficha} actualizada')
            return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
    else:
        form = FichaObstetricaForm(instance=ficha)
    
    context = {
        'form': form,
        'ficha': ficha,
        'paciente': paciente,
        'persona': persona,
        'titulo': 'Editar Ficha Obstétrica',
        'accion': 'editar'
    }
    return render(request, 'Matrona/form_obstetrica_materna.html', context)


# ============================================
# FICHA OBSTÉTRICA - DETALLE
# ============================================

@login_required
def detalle_ficha_obstetrica(request, ficha_pk):
    """
    Ver detalle de ficha obstétrica
    URL: /matrona/ficha/<ficha_pk>/
    """
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk)
    paciente = ficha.paciente
    persona = paciente.persona
    medicamentos = ficha.medicamentos.filter(activo=True)
    
    context = {
        'ficha': ficha,
        'paciente': paciente,
        'persona': persona,
        'medicamentos': medicamentos,
        'titulo': f'Ficha {ficha.numero_ficha}',
        'edad_gestacional': f"{ficha.edad_gestacional_semanas}+{ficha.edad_gestacional_dias}"
    }
    return render(request, 'Matrona/detalle_ficha_obstetrica.html', context)


# ============================================
# FICHA OBSTÉTRICA - LISTA
# ============================================

@login_required
def lista_fichas_obstetrica(request):
    """
    Listar todas las fichas obstétricas
    URL: /matrona/fichas/
    """
    fichas = FichaObstetrica.objects.filter(activa=True).select_related(
        'paciente__persona'
    ).order_by('-fecha_creacion')
    
    # Búsqueda
    search_query = request.GET.get('q', '')
    if search_query:
        fichas = fichas.filter(
            Q(paciente__persona__Nombre__icontains=search_query) |
            Q(paciente__persona__Rut__icontains=search_query) |
            Q(numero_ficha__icontains=search_query)
        )
    
    # Paginación
    paginator = Paginator(fichas, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'fichas': page_obj.object_list,
        'titulo': 'Fichas Obstétricas',
        'total_fichas': paginator.count,
        'search_query': search_query
    }
    return render(request, 'Matrona/lista_fichas_obstetrica.html', context)


# ============================================
# MEDICAMENTOS - AGREGAR A FICHA
# ============================================

@login_required
def agregar_medicamento(request, ficha_pk):
    """
    Agregar medicamento a una ficha
    URL: /matrona/ficha/<ficha_pk>/medicamento/agregar/
    """
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk, activa=True)
    
    if request.method == 'POST':
        form = MedicamentoFichaForm(request.POST)
        if form.is_valid():
            medicamento = form.save(commit=False)
            medicamento.ficha = ficha
            medicamento.save()
            messages.success(
                request,
                f'✅ Medicamento {medicamento.medicamento} agregado'
            )
            return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
    else:
        form = MedicamentoFichaForm()
    
    context = {
        'form': form,
        'ficha': ficha,
        'titulo': 'Agregar Medicamento'
    }
    return render(request, 'Matrona/medicamento_form.html', context)


# ============================================
# MEDICAMENTOS - ELIMINAR
# ============================================

@login_required
def eliminar_medicamento(request, medicamento_pk):
    """
    Eliminar medicamento de una ficha
    URL: /matrona/medicamento/<medicamento_pk>/eliminar/
    """
    medicamento = get_object_or_404(MedicamentoFicha, pk=medicamento_pk)
    ficha = medicamento.ficha
    
    if request.method == 'POST':
        medicamento.delete()
        messages.success(request, f'✅ Medicamento eliminado')
        return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
    
    context = {
        'medicamento': medicamento,
        'ficha': ficha,
        'titulo': 'Eliminar Medicamento'
    }
    return render(request, 'Matrona/medicamento_confirmar_delete.html', context)


# ============================================
# MENU MATRONA
# ============================================

@login_required
def menu_matrona(request):
    """
    Menu principal de matrona
    URL: /matrona/
    """
    total_fichas = FichaObstetrica.objects.filter(activa=True).count()
    fichas_recientes = FichaObstetrica.objects.filter(activa=True).order_by('-fecha_creacion')[:5]
    
    context = {
        'titulo': 'Matrona - Control Prenatal',
        'total_fichas': total_fichas,
        'fichas_recientes': fichas_recientes
    }
    return render(request, 'Matrona/menu_matrona.html', context)

@login_required
def seleccionar_persona_ficha(request):
    """Seleccionar paciente para crear ficha obstétrica"""
    try:
        pacientes = Paciente.objects.filter(activo=True).select_related('persona').order_by('persona__Nombre')
    except:
        from gestionApp.models import Paciente
        pacientes = Paciente.objects.filter(activo=True).select_related('persona').order_by('persona__Nombre')
    
    search_query = request.GET.get('q', '')
    if search_query:
        pacientes = pacientes.filter(
            Q(persona__Nombre__icontains=search_query) |
            Q(persona__Rut__icontains=search_query) |
            Q(persona__Apellido_Paterno__icontains=search_query)
        )
    
    paginator = Paginator(pacientes, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'pacientes': page_obj.object_list,
        'titulo': 'Seleccionar Paciente para Ficha Obstétrica',
        'search_query': search_query,
        'total_pacientes': paginator.count
    }
    return render(request, 'Matrona/seleccionar_paciente_ficha.html', context)