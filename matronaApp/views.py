"""
matronaApp/views.py
Vistas para matronaApp - Fichas obstétricas, medicamentos, dilatación y parto
ACTUALIZADO: Con todas las nuevas funcionalidades
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db import transaction
from django.db.models import Q, Count
from datetime import date
import json

# ============================================
# IMPORTACIONES DE MODELOS
# ============================================

# Modelos de gestionApp (Persona, Paciente, etc.)
from gestionApp.models import Persona, Paciente, Matrona

# Modelos de matronaApp
from .models import (
    FichaObstetrica,
    MedicamentoFicha,
    AdministracionMedicamento,
    IngresoPaciente,
    CatalogoViaAdministracion,
    CatalogoConsultorioOrigen,
    RegistroDilatacion,
    PersonalAsignadoParto,
)

# Formularios - importar desde forms/__init__.py
from .forms import FichaObstetricaForm, MedicamentoFichaForm


# ============================================
# UTILIDADES
# ============================================

def calcular_edad(fecha_nacimiento):
    """Calcula la edad a partir de la fecha de nacimiento"""
    if not fecha_nacimiento:
        return 0
    hoy = date.today()
    return hoy.year - fecha_nacimiento.year - (
        (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
    )


# ============================================
# MENU MATRONA (DASHBOARD)
# ============================================

@login_required
def menu_matrona(request):
    """
    Menú principal de matrona (Dashboard)
    URL: /matrona/
    """
    # Estadísticas
    total_fichas = FichaObstetrica.objects.filter(activa=True).count()
    fichas_recientes = FichaObstetrica.objects.filter(activa=True).order_by('-fecha_creacion')[:5]
    
    # Fichas con proceso de parto activo
    fichas_en_parto = FichaObstetrica.objects.filter(
        activa=True, 
        proceso_parto_iniciado=True
    ).count()
    
    # Fichas con estancamiento
    fichas_estancadas = FichaObstetrica.objects.filter(
        activa=True,
        estado_dilatacion='ESTANCADA'
    ).count()
    
    # Datos para el dashboard
    total_ingresos = IngresoPaciente.objects.filter(activo=True).count()
    total_medicamentos_asignados = MedicamentoFicha.objects.filter(activo=True).count()
    
    # Permisos específicos de matrona
    puede_ingresar_paciente = True
    puede_asignar_medicamentos = True
    puede_buscar_paciente = True
    puede_editar_ficha = True
    puede_iniciar_parto = False  # Solo médico
    
    context = {
        'titulo': 'Dashboard Matrona',
        'total_fichas': total_fichas,
        'fichas_recientes': fichas_recientes,
        'fichas_en_parto': fichas_en_parto,
        'fichas_estancadas': fichas_estancadas,
        'total_ingresos': total_ingresos,
        'total_medicamentos_asignados': total_medicamentos_asignados,
        'puede_ingresar_paciente': puede_ingresar_paciente,
        'puede_asignar_medicamentos': puede_asignar_medicamentos,
        'puede_buscar_paciente': puede_buscar_paciente,
        'puede_editar_ficha': puede_editar_ficha,
        'puede_iniciar_parto': puede_iniciar_parto,
    }
    return render(request, 'Matrona/Data/dashboard_matrona.html', context)


# ============================================
# SELECCIONAR PERSONA PARA FICHA
# ============================================

@login_required
def seleccionar_persona_ficha(request):
    """
    Buscar y seleccionar persona para crear ficha obstétrica
    URL: /matrona/seleccionar-persona/
    """
    personas = []
    busqueda = request.GET.get('q', '')
    
    if busqueda:
        personas = Persona.objects.filter(
            Q(Rut__icontains=busqueda) |
            Q(Nombre__icontains=busqueda) |
            Q(Apellido_Paterno__icontains=busqueda)
        )[:20]
    
    context = {
        'titulo': 'Seleccionar Persona para Ficha Obstétrica',
        'personas': personas,
        'busqueda': busqueda,
    }
    return render(request, 'Matrona/seleccionar_persona_ficha.html', context)


# ============================================
# CREAR FICHA OBSTÉTRICA - DESDE PACIENTE
# ============================================

@login_required
def crear_ficha_obstetrica(request, paciente_pk):
    """
    Crear nueva ficha obstétrica a partir de un Paciente existente
    URL: /matrona/ficha/crear/<paciente_pk>/
    """
    paciente = get_object_or_404(Paciente, pk=paciente_pk)
    persona = paciente.persona
    
    # Verificar si ya tiene ficha activa
    ficha_existente = FichaObstetrica.objects.filter(paciente=paciente, activa=True).first()
    if ficha_existente:
        messages.warning(request, 'Esta paciente ya tiene una ficha obstétrica activa.')
        return redirect('matrona:detalle_ficha', ficha_pk=ficha_existente.pk)
    
    edad = calcular_edad(persona.Fecha_nacimiento)
    
    if request.method == 'POST':
        form = FichaObstetricaForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                ficha = form.save(commit=False)
                ficha.paciente = paciente
                ficha.numero_ficha = f"FO-{FichaObstetrica.objects.count() + 1:06d}"
                ficha.save()
                form.save_m2m()  # Guardar relaciones ManyToMany
                
                # Procesar medicamentos del POST
                procesar_medicamentos_post(request, ficha)
                
                # Procesar registros de dilatación del POST
                procesar_dilatacion_post(request, ficha)
                
                messages.success(request, f'✅ Ficha Obstétrica {ficha.numero_ficha} creada exitosamente')
                return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = FichaObstetricaForm()
    
    # Catálogos para el template
    vias_administracion = CatalogoViaAdministracion.objects.filter(activo=True)
    consultorios = CatalogoConsultorioOrigen.objects.filter(activo=True)
    
    context = {
        'form': form,
        'paciente': paciente,
        'persona': persona,
        'edad': edad,
        'titulo': 'Crear Ficha Obstétrica',
        'accion': 'crear',
        'vias_administracion': vias_administracion,
        'consultorios': consultorios,
    }
    return render(request, 'Matrona/form_obstetrica_materna.html', context)


# ============================================
# CREAR FICHA OBSTÉTRICA - DESDE PERSONA
# ============================================

@login_required
def crear_ficha_obstetrica_persona(request, persona_pk):
    """
    Crear nueva ficha obstétrica a partir de una Persona
    URL: /matrona/ficha/crear-persona/<persona_pk>/
    
    Si la persona no tiene un paciente creado, lo crea automáticamente
    """
    persona = get_object_or_404(Persona, pk=persona_pk)
    
    # Obtener o crear el paciente
    paciente, created = Paciente.objects.get_or_create(
        persona=persona,
        defaults={'activo': True}
    )
    
    # Si el paciente existe pero no estaba activo, lo activamos
    if not paciente.activo:
        paciente.activo = True
        paciente.save()
    
    # Verificar si ya tiene ficha activa
    ficha_existente = FichaObstetrica.objects.filter(paciente=paciente, activa=True).first()
    if ficha_existente:
        messages.warning(request, 'Esta paciente ya tiene una ficha obstétrica activa.')
        return redirect('matrona:detalle_ficha', ficha_pk=ficha_existente.pk)
    
    edad = calcular_edad(persona.Fecha_nacimiento)
    
    if request.method == 'POST':
        form = FichaObstetricaForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                ficha = form.save(commit=False)
                ficha.paciente = paciente
                ficha.numero_ficha = f"FO-{FichaObstetrica.objects.count() + 1:06d}"
                ficha.save()
                form.save_m2m()
                
                # Procesar medicamentos del POST
                procesar_medicamentos_post(request, ficha)
                
                # Procesar registros de dilatación del POST
                procesar_dilatacion_post(request, ficha)
                
                messages.success(request, f'✅ Ficha Obstétrica {ficha.numero_ficha} creada exitosamente')
                return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = FichaObstetricaForm()
    
    # Catálogos para el template
    vias_administracion = CatalogoViaAdministracion.objects.filter(activo=True)
    consultorios = CatalogoConsultorioOrigen.objects.filter(activo=True)
    
    context = {
        'form': form,
        'paciente': paciente,
        'persona': persona,
        'edad': edad,
        'titulo': 'Crear Ficha Obstétrica',
        'accion': 'crear',
        'vias_administracion': vias_administracion,
        'consultorios': consultorios,
    }
    return render(request, 'Matrona/form_obstetrica_materna.html', context)


# ============================================
# EDITAR FICHA OBSTÉTRICA
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
    
    edad = calcular_edad(persona.Fecha_nacimiento)
    
    if request.method == 'POST':
        form = FichaObstetricaForm(request.POST, instance=ficha)
        if form.is_valid():
            with transaction.atomic():
                ficha = form.save()
                
                # Procesar medicamentos del POST
                procesar_medicamentos_post(request, ficha)
                
                # Procesar registros de dilatación del POST
                procesar_dilatacion_post(request, ficha)
                
                messages.success(request, f'✅ Ficha {ficha.numero_ficha} actualizada')
                return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
    else:
        form = FichaObstetricaForm(instance=ficha)
    
    # Obtener datos existentes
    medicamentos = ficha.medicamentos.filter(activo=True)
    registros_dilatacion = ficha.registros_dilatacion.all().order_by('fecha_hora')
    
    # Catálogos para el template
    vias_administracion = CatalogoViaAdministracion.objects.filter(activo=True)
    consultorios = CatalogoConsultorioOrigen.objects.filter(activo=True)
    
    context = {
        'form': form,
        'ficha': ficha,
        'paciente': paciente,
        'persona': persona,
        'edad': edad,
        'titulo': 'Editar Ficha Obstétrica',
        'accion': 'editar',
        'medicamentos': medicamentos,
        'registros_dilatacion': registros_dilatacion,
        'vias_administracion': vias_administracion,
        'consultorios': consultorios,
    }
    return render(request, 'Matrona/form_obstetrica_materna.html', context)


# ============================================
# DETALLE FICHA OBSTÉTRICA
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
    registros_dilatacion = ficha.registros_dilatacion.all().order_by('fecha_hora')
    personal_asignado = ficha.personal_asignado.all()
    
    edad = calcular_edad(persona.Fecha_nacimiento)
    
    # Verificar estado de dilatación
    ficha.verificar_estancamiento()
    puede_parto_vaginal = ficha.puede_parto_vaginal()
    
    context = {
        'ficha': ficha,
        'paciente': paciente,
        'persona': persona,
        'edad': edad,
        'medicamentos': medicamentos,
        'registros_dilatacion': registros_dilatacion,
        'personal_asignado': personal_asignado,
        'personal_requerido': ficha.personal_requerido,
        'puede_parto_vaginal': puede_parto_vaginal,
        'titulo': f'Ficha {ficha.numero_ficha}',
        'edad_gestacional': f"{ficha.edad_gestacional_semanas or 0}+{ficha.edad_gestacional_dias or 0}"
    }
    return render(request, 'Matrona/detalle_ficha_obstetrica.html', context)


# ============================================
# LISTA DE FICHAS OBSTÉTRICAS
# ============================================

@login_required
def lista_fichas_obstetrica(request):
    """
    Listar todas las fichas obstétricas
    URL: /matrona/fichas/
    """
    fichas = FichaObstetrica.objects.filter(activa=True).select_related(
        'paciente__persona', 'matrona_responsable'
    ).order_by('-fecha_creacion')
    
    # Filtros
    estado = request.GET.get('estado', '')
    if estado == 'estancada':
        fichas = fichas.filter(estado_dilatacion='ESTANCADA')
    elif estado == 'en_parto':
        fichas = fichas.filter(proceso_parto_iniciado=True)
    elif estado == 'lista':
        fichas = fichas.filter(estado_dilatacion='LISTA')
    
    context = {
        'fichas': fichas,
        'titulo': 'Fichas Obstétricas',
        'estado_filtro': estado,
    }
    return render(request, 'Matrona/lista_fichas_obstetrica.html', context)


# ============================================
# MEDICAMENTOS - AGREGAR
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
            messages.success(request, f'✅ Medicamento {medicamento.medicamento} agregado')
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
        medicamento.activo = False
        medicamento.save()
        messages.success(request, '✅ Medicamento eliminado')
        return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
    
    context = {
        'medicamento': medicamento,
        'ficha': ficha,
        'titulo': 'Eliminar Medicamento'
    }
    return render(request, 'Matrona/medicamento_confirmar_delete.html', context)


# ============================================
# DILATACIÓN - AGREGAR REGISTRO (AJAX)
# ============================================

@login_required
@require_POST
def agregar_registro_dilatacion(request, ficha_pk):
    """
    API para agregar un nuevo registro de dilatación
    URL: /matrona/api/ficha/<ficha_pk>/dilatacion/agregar/
    """
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk, activa=True)
    
    try:
        data = json.loads(request.body)
        valor = int(data.get('valor'))
        observacion = data.get('observacion', '')
        
        if valor < 1 or valor > 10:
            return JsonResponse({
                'success': False,
                'error': 'La dilatación debe estar entre 1 y 10 cm'
            })
        
        # Crear registro
        registro = RegistroDilatacion.objects.create(
            ficha=ficha,
            valor_dilatacion=valor,
            observacion=observacion,
            registrado_por=request.user
        )
        
        # Verificar estancamiento
        estancamiento = ficha.verificar_estancamiento()
        puede_vaginal = ficha.puede_parto_vaginal()
        
        # Actualizar estado
        if puede_vaginal:
            ficha.estado_dilatacion = 'LISTA'
        elif not estancamiento:
            ficha.estado_dilatacion = 'PROGRESANDO'
        ficha.save()
        
        return JsonResponse({
            'success': True,
            'registro': {
                'id': registro.id,
                'hora': registro.fecha_hora.strftime('%H:%M'),
                'valor': registro.valor_dilatacion,
                'observacion': registro.observacion
            },
            'estado': {
                'codigo': ficha.estado_dilatacion,
                'estancamiento': estancamiento,
                'puede_vaginal': puede_vaginal
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ============================================
# DILATACIÓN - VERIFICAR ESTADO (AJAX)
# ============================================

@login_required
def verificar_estado_dilatacion(request, ficha_pk):
    """
    API para verificar el estado actual de dilatación
    URL: /matrona/api/ficha/<ficha_pk>/dilatacion/estado/
    """
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk)
    
    registros = list(ficha.registros_dilatacion.order_by('-fecha_hora').values(
        'id', 'fecha_hora', 'valor_dilatacion', 'observacion'
    )[:10])
    
    return JsonResponse({
        'estado': ficha.estado_dilatacion,
        'puede_vaginal': ficha.puede_parto_vaginal(),
        'estancamiento': ficha.estado_dilatacion == 'ESTANCADA',
        'registros': registros,
        'ultimo_valor': registros[0]['valor_dilatacion'] if registros else None
    })


# ============================================
# PARTO - INICIAR PROCESO
# ============================================

@login_required
@require_POST
def iniciar_proceso_parto(request, ficha_pk):
    """
    Iniciar el proceso de parto
    URL: /matrona/ficha/<ficha_pk>/iniciar-parto/
    """
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk, activa=True)
    
    if ficha.proceso_parto_iniciado:
        messages.warning(request, 'El proceso de parto ya fue iniciado.')
        return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
    
    tipo_parto = request.POST.get('tipo_parto')
    
    if not tipo_parto:
        messages.error(request, 'Debe seleccionar el tipo de parto.')
        return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
    
    # Validar para parto vaginal
    if tipo_parto == 'VAGINAL' and not ficha.puede_parto_vaginal():
        messages.error(request, 'No se puede iniciar parto vaginal. La dilatación debe ser de al menos 8 cm.')
        return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
    
    with transaction.atomic():
        ficha.tipo_parto = tipo_parto
        ficha.proceso_parto_iniciado = True
        ficha.fecha_inicio_parto = timezone.now()
        ficha.save()
        
        # Asignar personal automáticamente
        asignar_personal_parto(ficha)
        
        tipo_texto = 'parto vaginal' if tipo_parto == 'VAGINAL' else 'cesárea'
        messages.success(request, f'✅ Proceso de {tipo_texto} iniciado exitosamente.')
    
    return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)


# ============================================
# FUNCIONES AUXILIARES
# ============================================

def procesar_medicamentos_post(request, ficha):
    """Procesa los medicamentos enviados en el POST"""
    index = 0
    while f'medicamentos[{index}][medicamento]' in request.POST:
        med_nombre = request.POST.get(f'medicamentos[{index}][medicamento]')
        
        if med_nombre:
            via_id = request.POST.get(f'medicamentos[{index}][via_administracion]')
            
            MedicamentoFicha.objects.create(
                ficha=ficha,
                medicamento=med_nombre,
                dosis=request.POST.get(f'medicamentos[{index}][dosis]', ''),
                via_administracion_id=via_id if via_id else None,
                cantidad=int(request.POST.get(f'medicamentos[{index}][cantidad]', 1)),
                frecuencia=request.POST.get(f'medicamentos[{index}][frecuencia]', ''),
                fecha_inicio=request.POST.get(f'medicamentos[{index}][fecha_inicio]') or timezone.now(),
                fecha_termino=request.POST.get(f'medicamentos[{index}][fecha_termino]') or None,
                indicaciones=request.POST.get(f'medicamentos[{index}][indicaciones]', ''),
            )
        index += 1


def procesar_dilatacion_post(request, ficha):
    """Procesa los registros de dilatación enviados en el POST"""
    index = 0
    while f'dilatacion[{index}][valor]' in request.POST:
        valor = request.POST.get(f'dilatacion[{index}][valor]')
        
        if valor:
            hora = request.POST.get(f'dilatacion[{index}][hora]')
            
            RegistroDilatacion.objects.create(
                ficha=ficha,
                fecha_hora=hora or timezone.now(),
                valor_dilatacion=int(valor),
                observacion=request.POST.get(f'dilatacion[{index}][observacion]', ''),
                registrado_por=request.user
            )
        index += 1
    
    # Verificar estado después de agregar registros
    ficha.verificar_estancamiento()
    if ficha.puede_parto_vaginal():
        ficha.estado_dilatacion = 'LISTA'
        ficha.save()


def asignar_personal_parto(ficha):
    """
    Asigna automáticamente el personal requerido para el parto.
    Por cada bebé: 1 médico, 2 matronas, 2 TENS
    """
    for bebe_num in range(1, ficha.cantidad_bebes + 1):
        # Crear slot para médico
        PersonalAsignadoParto.objects.create(
            ficha=ficha,
            rol='MEDICO',
            bebe_numero=bebe_num,
        )
        
        # Crear slots para matronas (2 por bebé)
        for _ in range(2):
            PersonalAsignadoParto.objects.create(
                ficha=ficha,
                rol='MATRONA',
                bebe_numero=bebe_num,
            )
        
        # Crear slots para TENS (2 por bebé)
        for _ in range(2):
            PersonalAsignadoParto.objects.create(
                ficha=ficha,
                rol='TENS',
                bebe_numero=bebe_num,
            )


# ============================================
# APIs ADICIONALES
# ============================================

@login_required
def obtener_personal_requerido(request, ficha_pk):
    """
    API para obtener el personal requerido según cantidad de bebés
    URL: /matrona/api/ficha/<ficha_pk>/personal/
    """
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk)
    
    asignados = list(ficha.personal_asignado.values(
        'id', 'rol', 'bebe_numero', 'usuario__first_name', 'usuario__last_name', 'activo'
    ))
    
    return JsonResponse({
        'cantidad_bebes': ficha.cantidad_bebes,
        'personal_requerido': ficha.personal_requerido,
        'asignados': asignados
    })


@login_required
@require_POST
def agregar_medicamento_ajax(request, ficha_pk):
    """
    API AJAX para agregar medicamento
    URL: /matrona/api/ficha/<ficha_pk>/medicamento/agregar/
    """
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk, activa=True)
    
    try:
        data = json.loads(request.body)
        
        via_id = data.get('via_administracion')
        
        medicamento = MedicamentoFicha.objects.create(
            ficha=ficha,
            medicamento=data.get('medicamento', ''),
            dosis=data.get('dosis', ''),
            via_administracion_id=via_id if via_id else None,
            cantidad=int(data.get('cantidad', 1)),
            frecuencia=data.get('frecuencia', ''),
            fecha_inicio=data.get('fecha_inicio') or timezone.now(),
            fecha_termino=data.get('fecha_termino') or None,
            indicaciones=data.get('indicaciones', ''),
        )
        
        return JsonResponse({
            'success': True,
            'medicamento': {
                'id': medicamento.id,
                'nombre': medicamento.medicamento,
                'dosis': medicamento.dosis,
                'fecha_inicio': medicamento.fecha_inicio.strftime('%d/%m/%Y') if medicamento.fecha_inicio else ''
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_POST
def eliminar_medicamento_ajax(request, medicamento_pk):
    """
    API AJAX para eliminar medicamento
    URL: /matrona/api/medicamento/<medicamento_pk>/eliminar/
    """
    medicamento = get_object_or_404(MedicamentoFicha, pk=medicamento_pk)
    medicamento.activo = False
    medicamento.save()
    
    return JsonResponse({'success': True})