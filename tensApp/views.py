"""
tensApp/views.py
Vistas del módulo TENS - CORREGIDO para usar User + Groups
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Count, Prefetch
from django.utils import timezone
from django.contrib.auth.models import User

from gestionApp.models import Persona, Paciente
from matronaApp.models import (
    FichaObstetrica, 
    MedicamentoFicha, 
    AdministracionMedicamento, 
    IngresoPaciente
)
from tensApp.models import RegistroTens, Tratamiento_aplicado


# ============================================
# BUSCAR PACIENTE
# ============================================

@login_required
def buscar_paciente_tens(request):
    """Buscar paciente por RUT o nombre"""
    from django.core.paginator import Paginator
    
    query = request.GET.get('q', '').strip()
    pacientes = Paciente.objects.filter(activo=True).select_related('persona')
    
    if query:
        pacientes = pacientes.filter(
            Q(persona__Rut__icontains=query) |
            Q(persona__Nombre__icontains=query) |
            Q(persona__Apellido_Paterno__icontains=query) |
            Q(persona__Apellido_Materno__icontains=query)
        )
    
    pacientes = pacientes.order_by('persona__Apellido_Paterno')
    
    paginator = Paginator(pacientes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'titulo': 'Buscar Paciente',
        'pacientes': page_obj,
        'page_obj': page_obj,
        'query': query,
    }
    
    return render(request, 'Tens/buscar_paciente.html', context)


# ============================================
# MENÚ PRINCIPAL TENS
# ============================================

@login_required
def menu_tens(request):
    """Menú principal del módulo TENS"""
    
    # Obtener la fecha de hoy
    hoy = timezone.now().date()
    
    # Contar administraciones de hoy
    administraciones_hoy = AdministracionMedicamento.objects.filter(
        fecha_hora_administracion__date=hoy
    ).count()
    
    # Medicamentos pendientes (activos sin administración hoy)
    medicamentos_pendientes = MedicamentoFicha.objects.filter(
        activo=True,
        ficha__activa=True
    ).exclude(
        administraciones__fecha_hora_administracion__date=hoy
    ).count()
    
    context = {
        'titulo': 'Panel TENS',
        'total_pacientes': Paciente.objects.filter(activo=True).count(),
        'total_fichas_activas': FichaObstetrica.objects.filter(activa=True).count(),
        'administraciones_hoy': administraciones_hoy,
        'medicamentos_pendientes': medicamentos_pendientes,
    }
    
    return render(request, 'Tens/menu_tens.html', context)


# ============================================
# LISTA DE FICHAS PARA TENS
# ============================================

@login_required
def lista_fichas_tens(request):
    """Lista de fichas obstétricas activas para TENS"""
    
    fichas = FichaObstetrica.objects.filter(
        activa=True
    ).select_related(
        'paciente__persona'
    ).prefetch_related(
        'medicamentos'
    ).order_by('-fecha_creacion')
    
    # Filtro por búsqueda
    busqueda = request.GET.get('q', '')
    if busqueda:
        fichas = fichas.filter(
            Q(paciente__persona__Nombre__icontains=busqueda) |
            Q(paciente__persona__Apellido_Paterno__icontains=busqueda) |
            Q(paciente__persona__Rut__icontains=busqueda) |
            Q(numero_ficha__icontains=busqueda)
        )
    
    context = {
        'titulo': 'Fichas Activas',
        'fichas': fichas,
        'busqueda': busqueda,
    }
    
    return render(request, 'Tens/lista_fichas_tens.html', context)


# ============================================
# DETALLE DE FICHA PARA TENS
# ============================================

@login_required
def detalle_ficha_tens(request, ficha_pk):
    """Ver detalle de ficha para administrar medicamentos"""
    
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk)
    paciente = ficha.paciente
    persona = paciente.persona
    
    # Medicamentos activos de la ficha
    medicamentos = ficha.medicamentos.filter(activo=True)
    
    # Administraciones de hoy
    hoy = timezone.now().date()
    administraciones_hoy = AdministracionMedicamento.objects.filter(
        medicamento_ficha__ficha=ficha,
        fecha_hora_administracion__date=hoy
    ).order_by('-fecha_hora_administracion')
    
    # Registros de signos vitales
    registros_tens = RegistroTens.objects.filter(
        ficha=ficha
    ).order_by('-fecha_registro')[:10]
    
    context = {
        'titulo': f'Ficha {ficha.numero_ficha}',
        'ficha': ficha,
        'paciente': paciente,
        'persona': persona,
        'medicamentos': medicamentos,
        'administraciones_hoy': administraciones_hoy,
        'registros_tens': registros_tens,
    }
    
    return render(request, 'Tens/detalle_ficha_tens.html', context)


# ============================================
# ADMINISTRAR MEDICAMENTO
# ============================================

@login_required
def administrar_medicamento(request, medicamento_pk):
    """Registrar administración de un medicamento"""
    
    medicamento = get_object_or_404(MedicamentoFicha, pk=medicamento_pk, activo=True)
    ficha = medicamento.ficha
    
    if request.method == 'POST':
        dosis = request.POST.get('dosis_administrada', medicamento.dosis)
        observaciones = request.POST.get('observaciones', '')
        
        # Crear registro de administración
        AdministracionMedicamento.objects.create(
            medicamento_ficha=medicamento,
            tens=request.user,  # Ahora es User directamente
            dosis_administrada=dosis,
            observaciones=observaciones,
            fecha_hora_administracion=timezone.now()
        )
        
        messages.success(
            request, 
            f'✅ Medicamento {medicamento.medicamento} administrado correctamente'
        )
        return redirect('tens:detalle_ficha', ficha_pk=ficha.pk)
    
    context = {
        'titulo': 'Administrar Medicamento',
        'medicamento': medicamento,
        'ficha': ficha,
    }
    
    return render(request, 'Tens/administrar_medicamento.html', context)


# ============================================
# REGISTRAR SIGNOS VITALES
# ============================================

@login_required
def registrar_signos_vitales(request, ficha_pk):
    """Registrar signos vitales de una paciente"""
    
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk, activa=True)
    
    if request.method == 'POST':
        # Crear registro de signos vitales
        registro = RegistroTens.objects.create(
            ficha=ficha,
            tens=request.user,  # Ahora es User directamente
            temperatura=request.POST.get('temperatura') or None,
            frecuencia_cardiaca=request.POST.get('frecuencia_cardiaca') or None,
            presion_sistolica=request.POST.get('presion_sistolica') or None,
            presion_diastolica=request.POST.get('presion_diastolica') or None,
            frecuencia_respiratoria=request.POST.get('frecuencia_respiratoria') or None,
            saturacion_oxigeno=request.POST.get('saturacion_oxigeno') or None,
            observaciones=request.POST.get('observaciones', ''),
        )
        
        messages.success(request, '✅ Signos vitales registrados correctamente')
        return redirect('tens:detalle_ficha', ficha_pk=ficha.pk)
    
    context = {
        'titulo': 'Registrar Signos Vitales',
        'ficha': ficha,
        'paciente': ficha.paciente,
    }
    
    return render(request, 'Tens/registrar_signos.html', context)


# ============================================
# HISTORIAL DE SIGNOS VITALES
# ============================================

@login_required
def historial_signos(request, ficha_pk):
    """Ver historial de signos vitales de una ficha"""
    
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk)
    
    registros = RegistroTens.objects.filter(
        ficha=ficha
    ).select_related('tens').order_by('-fecha_registro')
    
    context = {
        'titulo': f'Historial - {ficha.numero_ficha}',
        'ficha': ficha,
        'registros': registros,
    }
    
    return render(request, 'Tens/historial_signos.html', context)


# ============================================
# REGISTRAR TRATAMIENTO
# ============================================

@login_required
def registrar_tratamiento(request, ficha_pk):
    """Registrar aplicación de tratamiento"""
    
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk, activa=True)
    
    if request.method == 'POST':
        tratamiento = Tratamiento_aplicado.objects.create(
            ficha=ficha,
            tens=request.user,  # Ahora es User directamente
            tipo_tratamiento=request.POST.get('tipo_tratamiento', ''),
            descripcion=request.POST.get('descripcion', ''),
            observaciones=request.POST.get('observaciones', ''),
        )
        
        messages.success(request, '✅ Tratamiento registrado correctamente')
        return redirect('tens:detalle_ficha', ficha_pk=ficha.pk)
    return render(request, 'Tens/registrar_tratamiento.html', context)


# ============================================
# HISTORIAL DE TRATAMIENTOS
# ============================================

@login_required
def historial_tratamientos(request, ficha_pk):
    """Ver historial de tratamientos aplicados de una ficha"""
    
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk)
    
    tratamientos = Tratamiento_aplicado.objects.filter(
        ficha=ficha
    ).select_related('tens').order_by('-fecha_aplicacion')
    
    context = {
        'titulo': f'Historial Tratamientos - {ficha.numero_ficha}',
        'ficha': ficha,
        'tratamientos': tratamientos,
    }
    
    return render(request, 'Tens/historial_tratamientos.html', context)


# ============================================
# LISTAS ESPECÍFICAS POR ACCIÓN
# ============================================

@login_required
def lista_fichas_signos(request):
    """Lista de fichas activas para registrar signos vitales"""
    
    fichas = FichaObstetrica.objects.filter(
        activa=True
    ).select_related(
        'paciente__persona'
    ).order_by('-fecha_creacion')
    
    # Filtro por búsqueda
    busqueda = request.GET.get('q', '')
    if busqueda:
        fichas = fichas.filter(
            Q(paciente__persona__Nombre__icontains=busqueda) |
            Q(paciente__persona__Apellido_Paterno__icontains=busqueda) |
            Q(paciente__persona__Rut__icontains=busqueda) |
            Q(numero_ficha__icontains=busqueda)
        )
    
    context = {
        'titulo': 'Registrar Signos Vitales',
        'fichas': fichas,
        'busqueda': busqueda,
        'accion': 'signos',
        'accion_url': 'tens:registrar_signos',
        'accion_texto': 'Registrar Signos',
        'accion_icono': 'bi-heart-pulse',
    }
    
    return render(request, 'Tens/lista_fichas_accion.html', context)


@login_required
def lista_fichas_historial(request):
    """Lista de fichas activas para ver historial"""
    
    fichas = FichaObstetrica.objects.filter(
        activa=True
    ).select_related(
        'paciente__persona'
    ).order_by('-fecha_creacion')
    
    # Filtro por búsqueda
    busqueda = request.GET.get('q', '')
    if busqueda:
        fichas = fichas.filter(
            Q(paciente__persona__Nombre__icontains=busqueda) |
            Q(paciente__persona__Apellido_Paterno__icontains=busqueda) |
            Q(paciente__persona__Rut__icontains=busqueda) |
            Q(numero_ficha__icontains=busqueda)
        )
    
    context = {
        'titulo': 'Ver Historial de Pacientes',
        'fichas': fichas,
        'busqueda': busqueda,
        'accion': 'historial',
        'accion_url': 'tens:historial_signos',
        'accion_texto': 'Ver Historial',
        'accion_icono': 'bi-clock-history',
    }
    
    return render(request, 'Tens/lista_fichas_accion.html', context)


@login_required
def lista_fichas_tratamiento(request):
    """Lista de fichas activas para registrar tratamientos"""
    
    fichas = FichaObstetrica.objects.filter(
        activa=True
    ).select_related(
        'paciente__persona'
    ).order_by('-fecha_creacion')
    
    # Filtro por búsqueda
    busqueda = request.GET.get('q', '')
    if busqueda:
        fichas = fichas.filter(
            Q(paciente__persona__Nombre__icontains=busqueda) |
            Q(paciente__persona__Apellido_Paterno__icontains=busqueda) |
            Q(paciente__persona__Rut__icontains=busqueda) |
            Q(numero_ficha__icontains=busqueda)
        )
    
    context = {
        'titulo': 'Registrar Tratamientos',
        'fichas': fichas,
        'busqueda': busqueda,
        'accion': 'tratamiento',
        'accion_url': 'tens:registrar_tratamiento',
        'accion_texto': 'Registrar Tratamiento',
        'accion_icono': 'bi-bandaid',
    }
    
    return render(request, 'Tens/lista_fichas_accion.html', context)