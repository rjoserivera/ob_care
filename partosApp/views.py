"""
partosApp/views.py
Vistas para gestionar Registro de Partos (9 pasos)
CORREGIDO: Sin typos de espacios en nombres
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from ingresoPartoApp.models import FichaParto
from .models import RegistroParto
from .forms.registro_parto import (
    RegistroPartoBaseForm,
    RegistroPartoObstetricoForm,
    RegistroPartoAlubramientoForm,
    RegistroPartoPerinealForm,
    RegistroPartoAnestesiaForm,
    RegistroPartoApegoForm,
    RegistroPartoProfesionalesForm,
    RegistroPartoLeyDomingaForm,
    RegistroPartoObservacionesForm,
)


# ============================================
# PASO 1: INFO BÁSICA
# ============================================

@login_required
def crear_registro_parto_paso1(request, ficha_parto_pk):
    """
    Paso 1: Crear registro de parto con info básica
    URL: /partos/registro/<ficha_parto_pk>/paso1/
    """
    ficha_parto = get_object_or_404(FichaParto, pk=ficha_parto_pk)
    
    if request.method == 'POST':
        form = RegistroPartoBaseForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.ficha_parto = ficha_parto
            registro.save()
            
            # Guardar en sesión para pasos siguientes
            request.session['registro_parto_id'] = registro.pk
            
            messages.success(request, '✅ Información básica guardada')
            return redirect('partos:crear_registro_parto_paso2')
    else:
        form = RegistroPartoBaseForm()
    
    context = {
        'form': form,
        'ficha_parto': ficha_parto,
        'paso_actual': 1,
        'total_pasos': 9,
        'titulo': 'Paso 1: Información Básica del Parto'
    }
    return render(request, 'Parto/form_parto_paso1.html', context)


# ============================================
# PASO 2: DATOS OBSTÉTRICOS
# ============================================

@login_required
def crear_registro_parto_paso2(request):
    """
    Paso 2: Datos obstétricos
    URL: /partos/registro/paso2/
    """
    registro_id = request.session.get('registro_parto_id')
    if not registro_id:
        messages.error(request, '⚠️ Sesión expirada. Comienza desde paso 1')
        return redirect('partos:menu_partos')
    
    registro = get_object_or_404(RegistroParto, pk=registro_id)
    
    if request.method == 'POST':
        form = RegistroPartoObstetricoForm(request.POST, instance=registro)
        if form.is_valid():
            registro = form.save()
            messages.success(request, '✅ Datos obstétricos guardados')
            return redirect('partos:crear_registro_parto_paso3')
    else:
        form = RegistroPartoObstetricoForm(instance=registro)
    
    context = {
        'form': form,
        'registro': registro,
        'paso_actual': 2,
        'total_pasos': 9,
        'titulo': 'Paso 2: Datos Obstétricos'
    }
    return render(request, 'Parto/form_parto_paso2.html', context)


# ============================================
# PASO 3: ALUMBRAMIENTO Y PLACENTA
# ============================================

@login_required
def crear_registro_parto_paso3(request):
    """
    Paso 3: Alumbramiento y placenta
    URL: /partos/registro/paso3/
    """
    registro_id = request.session.get('registro_parto_id')
    if not registro_id:
        messages.error(request, '⚠️ Sesión expirada. Comienza desde paso 1')
        return redirect('partos:menu_partos')
    
    registro = get_object_or_404(RegistroParto, pk=registro_id)
    
    if request.method == 'POST':
        form = RegistroPartoAlubramientoForm(request.POST, instance=registro)
        if form.is_valid():
            registro = form.save()
            messages.success(request, '✅ Datos de alumbramiento guardados')
            return redirect('partos:crear_registro_parto_paso4')
    else:
        form = RegistroPartoAlubramientoForm(instance=registro)
    
    context = {
        'form': form,
        'registro': registro,
        'paso_actual': 3,
        'total_pasos': 9,
        'titulo': 'Paso 3: Alumbramiento y Placenta'
    }
    return render(request, 'Parto/form_parto_paso3.html', context)


# ============================================
# PASO 4: PERINÉ Y COMPLICACIONES
# ============================================

@login_required
def crear_registro_parto_paso4(request):
    """
    Paso 4: Periné, complicaciones y esterilización
    URL: /partos/registro/paso4/
    """
    registro_id = request.session.get('registro_parto_id')
    if not registro_id:
        messages.error(request, '⚠️ Sesión expirada. Comienza desde paso 1')
        return redirect('partos:menu_partos')
    
    registro = get_object_or_404(RegistroParto, pk=registro_id)
    
    if request.method == 'POST':
        form = RegistroPartoPerinealForm(request.POST, instance=registro)
        if form.is_valid():
            registro = form.save()
            messages.success(request, '✅ Datos perineales guardados')
            return redirect('partos:crear_registro_parto_paso5')
    else:
        form = RegistroPartoPerinealForm(instance=registro)
    
    context = {
        'form': form,
        'registro': registro,
        'paso_actual': 4,
        'total_pasos': 9,
        'titulo': 'Paso 4: Periné y Complicaciones'
    }
    return render(request, 'Parto/form_parto_paso4.html', context)


# ============================================
# PASO 5: ANESTESIA/ANALGESIA ⭐
# ============================================

@login_required
def crear_registro_parto_paso5(request):
    """
    Paso 5: Anestesia y Analgesia COMPLETO
    URL: /partos/registro/paso5/
    """
    registro_id = request.session.get('registro_parto_id')
    if not registro_id:
        messages.error(request, '⚠️ Sesión expirada. Comienza desde paso 1')
        return redirect('partos:menu_partos')
    
    registro = get_object_or_404(RegistroParto, pk=registro_id)
    
    if request.method == 'POST':
        form = RegistroPartoAnestesiaForm(request.POST, instance=registro)
        if form.is_valid():
            registro = form.save()
            messages.success(request, '✅ Anestesia/Analgesia registrada')
            return redirect('partos:crear_registro_parto_paso6')
    else:
        form = RegistroPartoAnestesiaForm(instance=registro)
    
    context = {
        'form': form,
        'registro': registro,
        'paso_actual': 5,
        'total_pasos': 9,
        'titulo': 'Paso 5: Anestesia y Analgesia'
    }
    return render(request, 'Parto/form_parto_paso5_anestesia.html', context)


# ============================================
# PASO 6: APEGO/ACOMPAÑAMIENTO ⭐
# ============================================

@login_required
def crear_registro_parto_paso6(request):
    """
    Paso 6: Apego y Acompañamiento COMPLETO
    URL: /partos/registro/paso6/
    """
    registro_id = request.session.get('registro_parto_id')
    if not registro_id:
        messages.error(request, '⚠️ Sesión expirada. Comienza desde paso 1')
        return redirect('partos:menu_partos')
    
    registro = get_object_or_404(RegistroParto, pk=registro_id)
    
    if request.method == 'POST':
        form = RegistroPartoApegoForm(request.POST, instance=registro)
        if form.is_valid():
            registro = form.save()
            messages.success(request, '✅ Apego/Acompañamiento registrado')
            return redirect('partos:crear_registro_parto_paso7')
    else:
        form = RegistroPartoApegoForm(instance=registro)
    
    context = {
        'form': form,
        'registro': registro,
        'paso_actual': 6,
        'total_pasos': 9,
        'titulo': 'Paso 6: Apego y Acompañamiento'
    }
    return render(request, 'Parto/form_parto_paso6_apego.html', context)


# ============================================
# PASO 7: PROFESIONALES Y CAUSAS
# ============================================

@login_required
def crear_registro_parto_paso7(request):
    """
    Paso 7: Profesionales y causas de intervención
    URL: /partos/registro/paso7/
    """
    registro_id = request.session.get('registro_parto_id')
    if not registro_id:
        messages.error(request, '⚠️ Sesión expirada. Comienza desde paso 1')
        return redirect('partos:menu_partos')
    
    registro = get_object_or_404(RegistroParto, pk=registro_id)
    
    if request.method == 'POST':
        form = RegistroPartoProfesionalesForm(request.POST, instance=registro)
        if form.is_valid():
            registro = form.save()
            messages.success(request, '✅ Datos de profesionales guardados')
            return redirect('partos:crear_registro_parto_paso8')
    else:
        form = RegistroPartoProfesionalesForm(instance=registro)
    
    context = {
        'form': form,
        'registro': registro,
        'paso_actual': 7,
        'total_pasos': 9,
        'titulo': 'Paso 7: Profesionales'
    }
    return render(request, 'Parto/form_parto_paso7_profesionales.html', context)


# ============================================
# PASO 8: LEY DOMINGA N° 21.372
# ============================================

@login_required
def crear_registro_parto_paso8(request):
    """
    Paso 8: Ley Dominga N° 21.372
    URL: /partos/registro/paso8/
    """
    registro_id = request.session.get('registro_parto_id')
    if not registro_id:
        messages.error(request, '⚠️ Sesión expirada. Comienza desde paso 1')
        return redirect('partos:menu_partos')
    
    registro = get_object_or_404(RegistroParto, pk=registro_id)
    
    if request.method == 'POST':
        form = RegistroPartoLeyDomingaForm(request.POST, instance=registro)
        if form.is_valid():
            registro = form.save()
            messages.success(request, '✅ Ley Dominga registrada')
            return redirect('partos:crear_registro_parto_paso9')
    else:
        form = RegistroPartoLeyDomingaForm(instance=registro)
    
    context = {
        'form': form,
        'registro': registro,
        'paso_actual': 8,
        'total_pasos': 9,
        'titulo': 'Paso 8: Ley Dominga N° 21.372'
    }
    return render(request, 'Parto/form_parto_paso8_ley_dominga.html', context)


# ============================================
# PASO 9: OBSERVACIONES FINALES
# ============================================

@login_required
def crear_registro_parto_paso9(request):
    """
    Paso 9: Observaciones finales
    URL: /partos/registro/paso9/
    """
    registro_id = request.session.get('registro_parto_id')
    if not registro_id:
        messages.error(request, '⚠️ Sesión expirada. Comienza desde paso 1')
        return redirect('partos:menu_partos')
    
    registro = get_object_or_404(RegistroParto, pk=registro_id)
    
    if request.method == 'POST':
        form = RegistroPartoObservacionesForm(request.POST, instance=registro)
        if form.is_valid():
            registro = form.save()
            
            # Limpiar sesión
            if 'registro_parto_id' in request.session:
                del request.session['registro_parto_id']
            
            messages.success(request, '✅ Registro de parto completado exitosamente')
            return redirect('partos:detalle_registro', registro_pk=registro.pk)
    else:
        form = RegistroPartoObservacionesForm(instance=registro)
    
    context = {
        'form': form,
        'registro': registro,
        'paso_actual': 9,
        'total_pasos': 9,
        'titulo': 'Paso 9: Observaciones Finales'
    }
    return render(request, 'Parto/form_parto_paso9_final.html', context)


# ============================================
# DETALLE REGISTRO
# ============================================

@login_required
def detalle_registro_parto(request, registro_pk):
    """
    Ver detalle de registro de parto
    URL: /partos/registro/<registro_pk>/
    """
    registro = get_object_or_404(RegistroParto, pk=registro_pk)
    ficha_parto = registro.ficha_parto
    ficha_obstetrica = ficha_parto.ficha_obstetrica
    paciente = ficha_obstetrica.paciente
    
    context = {
        'registro': registro,
        'ficha_parto': ficha_parto,
        'ficha_obstetrica': ficha_obstetrica,
        'paciente': paciente,
        'titulo': f'Registro Parto {registro.pk}'
    }
    return render(request, 'Parto/detalle_registro_parto.html', context)


# ============================================
# LISTA REGISTROS
# ============================================

@login_required
def lista_registros_parto(request):
    """
    Listar todos los registros de parto
    URL: /partos/registros/
    """
    registros = RegistroParto.objects.select_related(
        'ficha_parto__ficha_obstetrica__paciente__persona'
    ).order_by('-fecha_creacion')
    
    # Paginación
    paginator = Paginator(registros, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'registros': page_obj.object_list,
        'titulo': 'Registros de Parto',
        'total_registros': paginator.count
    }
    return render(request, 'Parto/lista_registros_parto.html', context)


# ============================================
# MENU PARTOS
# ============================================

@login_required
def menu_partos(request):
    """
    Menu principal de partos
    URL: /partos/
    """
    total_registros = RegistroParto.objects.count()
    registros_recientes = RegistroParto.objects.order_by('-fecha_creacion')[:5]
    
    context = {
        'titulo': 'Registro de Partos',
        'total_registros': total_registros,
        'registros_recientes': registros_recientes
    }
    return render(request, 'Parto/menu_partos.html', context)


