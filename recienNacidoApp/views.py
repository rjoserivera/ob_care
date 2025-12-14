"""
recienNacidoApp/views.py
Vistas para gestionar Registro de Recién Nacido (9 pasos)
CORREGIDO: Sin typos
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from partosApp.models import RegistroParto
from .models import RegistroRecienNacido, DocumentosParto
from .forms.registro_rn import (
    RegistroRecienNacidoDatosForm,
    RegistroRecienNacidoApgarForm,
    RegistroRecienNacidoCordónForm,
    RegistroRecienNacidoApegoForm,
    RegistroRecienNacidoAcompañamientoForm,
    RegistroRecienNacidoAlimentacionForm,
    RegistroRecienNacidoEvaluacionesForm,
    RegistroRecienNacidoComplicacionesForm,
    DocumentosPartoForm,
)


# ============================================
# PASO 1: DATOS BÁSICOS
# ============================================

@login_required
def crear_registro_rn_paso1(request, registro_parto_pk):
    """
    Paso 1: Datos básicos del recién nacido
    URL: /recien-nacido/crear/<registro_parto_pk>/paso1/
    """
    registro_parto = get_object_or_404(RegistroParto, pk=registro_parto_pk)
    
    if request.method == 'POST':
        form = RegistroRecienNacidoDatosForm(request.POST)
        if form.is_valid():
            registro_rn = form.save(commit=False)
            registro_rn.registro_parto = registro_parto
            registro_rn.save()
            
            # Guardar en sesión
            request.session['registro_rn_id'] = registro_rn.pk
            
            messages.success(request, '✅ Datos básicos guardados')
            return redirect('recien_nacido:crear_rn_paso2')
    else:
        form = RegistroRecienNacidoDatosForm()
    
    context = {
        'form': form,
        'registro_parto': registro_parto,
        'paso_actual': 1,
        'total_pasos': 9,
        'titulo': 'Paso 1: Datos Básicos del Recién Nacido'
    }
    return render(request, 'RecienNacido/form_rn_paso1_datos.html', context)


# ============================================
# PASO 2: APGAR
# ============================================

@login_required
def crear_registro_rn_paso2(request):
    """
    Paso 2: Puntuación Apgar
    URL: /recien-nacido/paso2/
    """
    registro_rn_id = request.session.get('registro_rn_id')
    if not registro_rn_id:
        messages.error(request, '⚠️ Sesión expirada. Comienza desde paso 1')
        return redirect('recien_nacido:menu_recien_nacido')
    
    registro_rn = get_object_or_404(RegistroRecienNacido, pk=registro_rn_id)
    
    if request.method == 'POST':
        form = RegistroRecienNacidoApgarForm(request.POST, instance=registro_rn)
        if form.is_valid():
            registro_rn = form.save()
            messages.success(request, '✅ Apgar registrado')
            return redirect('recien_nacido:crear_rn_paso3')
    else:
        form = RegistroRecienNacidoApgarForm(instance=registro_rn)
    
    context = {
        'form': form,
        'registro_rn': registro_rn,
        'paso_actual': 2,
        'total_pasos': 9,
        'titulo': 'Paso 2: Puntuación Apgar'
    }
    return render(request, 'RecienNacido/form_rn_paso2_apgar.html', context)


# ============================================
# PASO 3: CORDÓN UMBILICAL
# ============================================

@login_required
def crear_registro_rn_paso3(request):
    """
    Paso 3: Cordón umbilical y ligadura tardía
    URL: /recien-nacido/paso3/
    """
    registro_rn_id = request.session.get('registro_rn_id')
    if not registro_rn_id:
        messages.error(request, '⚠️ Sesión expirada. Comienza desde paso 1')
        return redirect('recien_nacido:menu_recien_nacido')
    
    registro_rn = get_object_or_404(RegistroRecienNacido, pk=registro_rn_id)
    
    if request.method == 'POST':
        form = RegistroRecienNacidoCordónForm(request.POST, instance=registro_rn)
        if form.is_valid():
            registro_rn = form.save()
            messages.success(request, '✅ Cordón umbilical registrado')
            return redirect('recien_nacido:crear_rn_paso4')
    else:
        form = RegistroRecienNacidoCordónForm(instance=registro_rn)
    
    context = {
        'form': form,
        'registro_rn': registro_rn,
        'paso_actual': 3,
        'total_pasos': 9,
        'titulo': 'Paso 3: Cordón Umbilical'
    }
    return render(request, 'RecienNacido/form_rn_paso3_cordon.html', context)


# ============================================
# PASO 4: APEGO ⭐
# ============================================

@login_required
def crear_registro_rn_paso4(request):
    """
    Paso 4: Apego - Piel con piel y contacto temprano
    URL: /recien-nacido/paso4/
    """
    registro_rn_id = request.session.get('registro_rn_id')
    if not registro_rn_id:
        messages.error(request, '⚠️ Sesión expirada. Comienza desde paso 1')
        return redirect('recien_nacido:menu_recien_nacido')
    
    registro_rn = get_object_or_404(RegistroRecienNacido, pk=registro_rn_id)
    
    if request.method == 'POST':
        form = RegistroRecienNacidoApegoForm(request.POST, instance=registro_rn)
        if form.is_valid():
            registro_rn = form.save()
            messages.success(request, '✅ Apego registrado')
            return redirect('recien_nacido:crear_rn_paso5')
    else:
        form = RegistroRecienNacidoApegoForm(instance=registro_rn)
    
    context = {
        'form': form,
        'registro_rn': registro_rn,
        'paso_actual': 4,
        'total_pasos': 9,
        'titulo': 'Paso 4: Apego'
    }
    return render(request, 'RecienNacido/form_rn_paso4_apego.html', context)


# ============================================
# PASO 5: ACOMPAÑAMIENTO ⭐
# ============================================

@login_required
def crear_registro_rn_paso5(request):
    """
    Paso 5: Acompañamiento - Familia presente
    URL: /recien-nacido/paso5/
    """
    registro_rn_id = request.session.get('registro_rn_id')
    if not registro_rn_id:
        messages.error(request, '⚠️ Sesión expirada. Comienza desde paso 1')
        return redirect('recien_nacido:menu_recien_nacido')
    
    registro_rn = get_object_or_404(RegistroRecienNacido, pk=registro_rn_id)
    
    if request.method == 'POST':
        form = RegistroRecienNacidoAcompañamientoForm(request.POST, instance=registro_rn)
        if form.is_valid():
            registro_rn = form.save()
            messages.success(request, '✅ Acompañamiento registrado')
            return redirect('recien_nacido:crear_rn_paso6')
    else:
        form = RegistroRecienNacidoAcompañamientoForm(instance=registro_rn)
    
    context = {
        'form': form,
        'registro_rn': registro_rn,
        'paso_actual': 5,
        'total_pasos': 9,
        'titulo': 'Paso 5: Acompañamiento'
    }
    return render(request, 'RecienNacido/form_rn_paso5_acompanamiento.html', context)


# ============================================
# PASO 6: ALIMENTACIÓN
# ============================================

@login_required
def crear_registro_rn_paso6(request):
    """
    Paso 6: Alimentación - Lactancia o fórmula
    URL: /recien-nacido/paso6/
    """
    registro_rn_id = request.session.get('registro_rn_id')
    if not registro_rn_id:
        messages.error(request, '⚠️ Sesión expirada. Comienza desde paso 1')
        return redirect('recien_nacido:menu_recien_nacido')
    
    registro_rn = get_object_or_404(RegistroRecienNacido, pk=registro_rn_id)
    
    if request.method == 'POST':
        form = RegistroRecienNacidoAlimentacionForm(request.POST, instance=registro_rn)
        if form.is_valid():
            registro_rn = form.save()
            messages.success(request, '✅ Alimentación registrada')
            return redirect('recien_nacido:crear_rn_paso7')
    else:
        form = RegistroRecienNacidoAlimentacionForm(instance=registro_rn)
    
    context = {
        'form': form,
        'registro_rn': registro_rn,
        'paso_actual': 6,
        'total_pasos': 9,
        'titulo': 'Paso 6: Alimentación'
    }
    return render(request, 'RecienNacido/form_rn_paso6_alimentacion.html', context)


# ============================================
# PASO 7: EVALUACIONES
# ============================================

@login_required
def crear_registro_rn_paso7(request):
    """
    Paso 7: Evaluaciones - Screening, examen físico, vacunas
    URL: /recien-nacido/paso7/
    """
    registro_rn_id = request.session.get('registro_rn_id')
    if not registro_rn_id:
        messages.error(request, '⚠️ Sesión expirada. Comienza desde paso 1')
        return redirect('recien_nacido:menu_recien_nacido')
    
    registro_rn = get_object_or_404(RegistroRecienNacido, pk=registro_rn_id)
    
    if request.method == 'POST':
        form = RegistroRecienNacidoEvaluacionesForm(request.POST, instance=registro_rn)
        if form.is_valid():
            registro_rn = form.save()
            messages.success(request, '✅ Evaluaciones registradas')
            return redirect('recien_nacido:crear_rn_paso8')
    else:
        form = RegistroRecienNacidoEvaluacionesForm(instance=registro_rn)
    
    context = {
        'form': form,
        'registro_rn': registro_rn,
        'paso_actual': 7,
        'total_pasos': 9,
        'titulo': 'Paso 7: Evaluaciones'
    }
    return render(request, 'RecienNacido/form_rn_paso7_evaluaciones.html', context)


# ============================================
# PASO 8: COMPLICACIONES
# ============================================

@login_required
def crear_registro_rn_paso8(request):
    """
    Paso 8: Complicaciones neonatales
    URL: /recien-nacido/paso8/
    """
    registro_rn_id = request.session.get('registro_rn_id')
    if not registro_rn_id:
        messages.error(request, '⚠️ Sesión expirada. Comienza desde paso 1')
        return redirect('recien_nacido:menu_recien_nacido')
    
    registro_rn = get_object_or_404(RegistroRecienNacido, pk=registro_rn_id)
    
    if request.method == 'POST':
        form = RegistroRecienNacidoComplicacionesForm(request.POST, instance=registro_rn)
        if form.is_valid():
            registro_rn = form.save()
            messages.success(request, '✅ Complicaciones registradas')
            return redirect('recien_nacido:crear_rn_paso9')
    else:
        form = RegistroRecienNacidoComplicacionesForm(instance=registro_rn)
    
    context = {
        'form': form,
        'registro_rn': registro_rn,
        'paso_actual': 8,
        'total_pasos': 9,
        'titulo': 'Paso 8: Complicaciones'
    }
    return render(request, 'RecienNacido/form_rn_paso8_complicaciones.html', context)


# ============================================
# PASO 9: DOCUMENTOS DEL PARTO
# ============================================

@login_required
def crear_registro_rn_paso9(request):
    """
    Paso 9: Documentos del parto
    URL: /recien-nacido/paso9/
    """
    registro_rn_id = request.session.get('registro_rn_id')
    if not registro_rn_id:
        messages.error(request, '⚠️ Sesión expirada. Comienza desde paso 1')
        return redirect('recien_nacido:menu_recien_nacido')
    
    registro_rn = get_object_or_404(RegistroRecienNacido, pk=registro_rn_id)
    
    # Crear o actualizar DocumentosParto
    documentos, created = DocumentosParto.objects.get_or_create(
        registro_recien_nacido=registro_rn
    )
    
    if request.method == 'POST':
        form = DocumentosPartoForm(request.POST, instance=documentos)
        if form.is_valid():
            form.save()
            
            # Limpiar sesión
            if 'registro_rn_id' in request.session:
                del request.session['registro_rn_id']
            
            messages.success(request, '✅ Registro de recién nacido completado exitosamente')
            return redirect('recien_nacido:detalle_registro_rn', registro_rn_pk=registro_rn.pk)
    else:
        form = DocumentosPartoForm(instance=documentos)
    
    context = {
        'form': form,
        'registro_rn': registro_rn,
        'documentos': documentos,
        'paso_actual': 9,
        'total_pasos': 9,
        'titulo': 'Paso 9: Documentos del Parto'
    }
    return render(request, 'RecienNacido/form_rn_paso9_documentos.html', context)


# ============================================
# DETALLE REGISTRO
# ============================================

@login_required
def detalle_registro_rn(request, registro_rn_pk):
    """
    Ver detalle de registro de recién nacido
    URL: /recien-nacido/registro/<registro_rn_pk>/
    """
    registro_rn = get_object_or_404(RegistroRecienNacido, pk=registro_rn_pk)
    registro_parto = registro_rn.registro_parto
    
    context = {
        'registro_rn': registro_rn,
        'registro_parto': registro_parto,
        'titulo': f'Registro RN {registro_rn.pk}'
    }
    return render(request, 'RecienNacido/detalle_registro_rn.html', context)


# ============================================
# LISTA REGISTROS
# ============================================

@login_required
def lista_registros_rn(request):
    """
    Listar todos los registros de recién nacido
    URL: /recien-nacido/registros/
    """
    registros = RegistroRecienNacido.objects.select_related(
        'registro_parto__ficha_parto__ficha_obstetrica__paciente__persona'
    ).order_by('-fecha_creacion')
    
    # Paginación
    paginator = Paginator(registros, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'registros': page_obj.object_list,
        'titulo': 'Registros de Recién Nacido',
        'total_registros': paginator.count
    }
    return render(request, 'RecienNacido/lista_registros_rn.html', context)


# ============================================
# MENU RECIÉN NACIDO
# ============================================

@login_required
def menu_recien_nacido(request):
    """
    Menu principal de recién nacido
    URL: /recien-nacido/
    """
    total_registros = RegistroRecienNacido.objects.count()
    registros_recientes = RegistroRecienNacido.objects.order_by('-fecha_creacion')[:5]
    
    context = {
        'titulo': 'Registro de Recién Nacido',
        'total_registros': total_registros,
        'registros_recientes': registros_recientes
    }
    return render(request, 'RecienNacido/menu_recien_nacido.html', context)


