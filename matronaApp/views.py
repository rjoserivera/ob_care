"""
matronaApp/views.py
Vistas para matronaApp - Fichas obstétricas, medicamentos, dilatación y parto
COMPLETO: Con TODAS las vistas existentes + nuevas funcionalidades
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
from gestionApp.models import Persona, Paciente

# Modelos de matronaApp
from .models import (
    FichaObstetrica,
    MedicamentoFicha,
    AdministracionMedicamento,
    IngresoPaciente,
    CatalogoViaAdministracion,
    CatalogoConsultorioOrigen,
    CatalogoMedicamento,
    RegistroDilatacion,
    PersonalAsignadoParto,
)

# Formularios
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
    fichas_recientes = FichaObstetrica.objects.filter(
        activa=True
    ).select_related('paciente__persona').order_by('-fecha_creacion')[:5]
    
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
    
    # Fichas listas para parto
    fichas_listas = FichaObstetrica.objects.filter(
        activa=True,
        estado_dilatacion='LISTA'
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
        'fichas_listas': fichas_listas,
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
            Q(Apellido_Paterno__icontains=busqueda) |
            Q(Apellido_Materno__icontains=busqueda)
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
    return render(request, 'Matrona/crear_ficha_obstetrica.html', context)


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
    return render(request, 'Matrona/crear_ficha_obstetrica.html', context)


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
    return render(request, 'Matrona/crear_ficha_obstetrica.html', context)


# ============================================
# DETALLE FICHA OBSTÉTRICA
# ============================================

@login_required
def detalle_ficha_obstetrica(request, ficha_pk):
    """
    Ver detalle de ficha obstétrica
    URL: /matrona/ficha/<ficha_pk>/
    """
    ficha = get_object_or_404(
        FichaObstetrica.objects.select_related(
            'paciente__persona',
            'consultorio_origen'
        ).prefetch_related(
            'registros_dilatacion',
            'medicamentos__via_administracion',
            'personal_asignado'
        ),
        pk=ficha_pk
    )
    
    paciente = ficha.paciente
    persona = paciente.persona
    medicamentos = ficha.medicamentos.filter(activo=True)
    registros_dilatacion = ficha.registros_dilatacion.all().order_by('-fecha_hora')
    personal_asignado = ficha.personal_asignado.all()
    
    edad = calcular_edad(persona.Fecha_nacimiento)
    
    # Verificar estado de dilatación
    ficha.verificar_estancamiento()
    puede_parto_vaginal = ficha.puede_parto_vaginal()
    
    # Obtener información de parto
    puede_parto, razon_parto, tipo_sugerido = ficha.puede_iniciar_parto()
    
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
        'puede_parto': puede_parto,
        'razon_parto': razon_parto,
        'tipo_parto_sugerido': tipo_sugerido,
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
        'paciente__persona', 'matrona_responsable', 'consultorio_origen'
    ).order_by('-fecha_creacion')
    
    # Filtros
    estado = request.GET.get('estado', '')
    if estado == 'estancada':
        fichas = fichas.filter(estado_dilatacion='ESTANCADA')
    elif estado == 'en_parto':
        fichas = fichas.filter(proceso_parto_iniciado=True)
    elif estado == 'lista':
        fichas = fichas.filter(estado_dilatacion='LISTA')
    
    # Búsqueda
    busqueda = request.GET.get('q', '')
    if busqueda:
        fichas = fichas.filter(
            Q(paciente__persona__Nombre__icontains=busqueda) |
            Q(paciente__persona__Apellido_Paterno__icontains=busqueda) |
            Q(paciente__persona__Rut__icontains=busqueda) |
            Q(numero_ficha__icontains=busqueda)
        )
    
    context = {
        'fichas': fichas,
        'titulo': 'Fichas Obstétricas',
        'estado_filtro': estado,
        'busqueda': busqueda,
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
            
            # Si no hay fecha de inicio, usar ahora
            if not medicamento.fecha_inicio:
                medicamento.fecha_inicio = timezone.now()
            
            medicamento.save()
            messages.success(request, f'✅ Medicamento "{medicamento.nombre_display}" agregado')
            return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
    else:
        form = MedicamentoFichaForm()
    
    context = {
        'form': form,
        'ficha': ficha,
        'titulo': 'Agregar Medicamento',
        'vias': CatalogoViaAdministracion.objects.filter(activo=True),
        'medicamentos_catalogo': CatalogoMedicamento.objects.filter(activo=True)[:50],
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
# MEDICAMENTOS - AGREGAR AJAX
# ============================================

@login_required
@require_POST
def agregar_medicamento_ajax(request, ficha_pk):
    """
    API para agregar medicamento vía AJAX
    URL: /matrona/api/ficha/<ficha_pk>/medicamento/agregar/
    """
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk, activa=True)
    
    try:
        data = json.loads(request.body)
        
        medicamento = MedicamentoFicha.objects.create(
            ficha=ficha,
            medicamento=data.get('medicamento', ''),
            medicamento_catalogo_id=data.get('medicamento_catalogo_id'),
            dosis=data.get('dosis', ''),
            via_administracion_id=data.get('via_administracion_id'),
            frecuencia=data.get('frecuencia', ''),
            cantidad=int(data.get('cantidad', 1)),
            fecha_inicio=timezone.now(),
            indicaciones=data.get('indicaciones', ''),
        )
        
        return JsonResponse({
            'success': True,
            'medicamento': {
                'id': medicamento.id,
                'nombre': medicamento.nombre_display,
                'dosis': medicamento.dosis,
                'via': str(medicamento.via_administracion) if medicamento.via_administracion else '',
                'frecuencia': medicamento.frecuencia,
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ============================================
# MEDICAMENTOS - ELIMINAR AJAX
# ============================================

@login_required
@require_POST
def eliminar_medicamento_ajax(request, medicamento_pk):
    """
    API para eliminar medicamento vía AJAX
    URL: /matrona/api/medicamento/<medicamento_pk>/eliminar/
    """
    try:
        medicamento = get_object_or_404(MedicamentoFicha, pk=medicamento_pk)
        medicamento.activo = False
        medicamento.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ============================================
# MEDICAMENTOS - BUSCAR EN CATÁLOGO
# ============================================

@login_required
def buscar_medicamentos(request):
    """
    API para buscar medicamentos en el catálogo
    URL: /matrona/api/medicamentos/buscar/
    """
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'resultados': []})
    
    medicamentos = CatalogoMedicamento.objects.filter(
        activo=True
    ).filter(
        Q(nombre__icontains=query) |
        Q(nombre_generico__icontains=query) |
        Q(codigo__icontains=query)
    )[:20]
    
    resultados = [{
        'id': m.id,
        'codigo': m.codigo,
        'nombre': m.nombre,
        'nombre_generico': m.nombre_generico,
        'concentracion': m.concentracion,
        'presentacion': m.presentacion,
        'display': str(m)
    } for m in medicamentos]
    
    return JsonResponse({'resultados': resultados})


# ============================================
# DILATACIÓN - AGREGAR REGISTRO (AJAX)
# ============================================

@login_required
@require_POST
def agregar_registro_dilatacion(request, ficha_pk):
    """
    API para agregar un nuevo registro de dilatación
    URL: /matrona/api/ficha/<ficha_pk>/dilatacion/agregar/
    Acepta tanto JSON (AJAX) como datos de formulario POST
    """
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk, activa=True)
    
    try:
        # Detectar si es JSON o formulario POST
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
                  request.content_type == 'application/json'
        
        if is_ajax:
            # Procesar como JSON
            data = json.loads(request.body)
            valor = int(data.get('valor', data.get('valor_dilatacion')))
            observacion = data.get('observacion', '')
        else:
            # Procesar como formulario POST
            valor = int(request.POST.get('valor_dilatacion'))
            observacion = request.POST.get('observacion', '')
        
        if valor < 0 or valor > 10:
            error_msg = 'La dilatación debe estar entre 0 y 10 cm'
            if is_ajax:
                return JsonResponse({'success': False, 'error': error_msg})
            else:
                messages.error(request, error_msg)
                return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
        
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
        elif estancamiento:
            ficha.estado_dilatacion = 'ESTANCADA'
        else:
            ficha.estado_dilatacion = 'PROGRESANDO'
        ficha.save(update_fields=['estado_dilatacion'])
        
        if is_ajax:
            puede_parto, razon, _ = ficha.puede_iniciar_parto()
            return JsonResponse({
                'success': True,
                'registro': {
                    'id': registro.id,
                    'hora': registro.fecha_hora.strftime('%d/%m/%Y %H:%M'),
                    'valor': registro.valor_dilatacion,
                    'observacion': registro.observacion
                },
                'estado': {
                    'codigo': ficha.estado_dilatacion,
                    'display': ficha.get_estado_dilatacion_display(),
                    'estancamiento': estancamiento,
                    'puede_vaginal': puede_vaginal,
                    'puede_iniciar_parto': puede_parto,
                    'razon_parto': razon
                }
            })
        
        messages.success(request, f'✅ Dilatación registrada: {valor} cm')
        return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
        
    except (ValueError, KeyError) as e:
        error_msg = f'Error en los datos: {str(e)}'
        if is_ajax:
            return JsonResponse({'success': False, 'error': error_msg})
        messages.error(request, error_msg)
        return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
    
    except Exception as e:
        error_msg = f'Error al registrar: {str(e)}'
        if is_ajax:
            return JsonResponse({'success': False, 'error': error_msg})
        messages.error(request, error_msg)
        return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)


# ============================================
# DILATACIÓN - VERIFICAR ESTADO
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
    
    # Formatear fechas
    for r in registros:
        r['fecha_hora'] = r['fecha_hora'].strftime('%d/%m/%Y %H:%M')
    
    puede_parto, razon, tipo = ficha.puede_iniciar_parto()
    
    return JsonResponse({
        'estado': ficha.estado_dilatacion,
        'estado_display': ficha.get_estado_dilatacion_display(),
        'puede_vaginal': ficha.puede_parto_vaginal(),
        'estancamiento': ficha.estado_dilatacion == 'ESTANCADA',
        'valor_actual': ficha.valor_dilatacion_actual,
        'registros': registros,
        'puede_iniciar_parto': puede_parto,
        'razon_parto': razon,
        'tipo_sugerido': tipo
    })


# ============================================
# PARTO - INICIAR PROCESO
# ============================================

@login_required
@require_POST
def iniciar_proceso_parto(request, ficha_pk):
    """
    Iniciar proceso de parto
    URL: /matrona/ficha/<ficha_pk>/iniciar-parto/
    """
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk, activa=True)
    
    # Verificar si puede iniciar parto
    puede_parto, razon, tipo_sugerido = ficha.puede_iniciar_parto()
    
    if not puede_parto:
        messages.error(request, f'No se puede iniciar el parto: {razon}')
        return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
    
    # Obtener tipo de parto del POST o usar el sugerido
    tipo_parto = request.POST.get('tipo_parto', tipo_sugerido)
    if tipo_parto not in ['VAGINAL', 'CESAREA', 'URGENTE']:
        tipo_parto = 'VAGINAL'
    
    with transaction.atomic():
        ficha.tipo_parto = tipo_parto if tipo_parto != 'URGENTE' else 'VAGINAL'
        ficha.proceso_parto_iniciado = True
        ficha.fecha_inicio_parto = timezone.now()
        ficha.save()
        
        # Asignar personal automáticamente
        asignar_personal_parto(ficha)
        
        tipo_texto = 'parto vaginal' if tipo_parto == 'VAGINAL' else 'cesárea'
        messages.success(request, f'✅ Proceso de {tipo_texto} iniciado exitosamente.')
    
    # Redirigir a página dedicada de proceso de parto
    return redirect('matrona:proceso_parto_iniciado', ficha_pk=ficha.pk)


# ============================================
# PARTO - PROCESO INICIADO
# ============================================

@login_required
def proceso_parto_iniciado(request, ficha_pk):
    """
    Página de proceso de parto iniciado
    URL: /matrona/ficha/<ficha_pk>/proceso-parto-iniciado/
    """
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk)
    
    context = {
        'ficha': ficha,
        'paciente': ficha.paciente,
        'persona': ficha.paciente.persona,
        'personal_asignado': ficha.personal_asignado.all(),
        'personal_requerido': ficha.personal_requerido,
        'titulo': 'Proceso de Parto Iniciado'
    }
    return render(request, 'Matrona/proceso_parto_iniciado.html', context)


# ============================================
# PERSONAL - OBTENER REQUERIDO
# ============================================

@login_required
def obtener_personal_requerido(request, ficha_pk):
    """
    API para obtener personal requerido para el parto
    URL: /matrona/api/ficha/<ficha_pk>/personal/
    """
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk)
    
    personal_asignado = list(ficha.personal_asignado.filter(activo=True).values(
        'id', 'rol', 'bebe_numero', 'usuario__first_name', 'usuario__last_name'
    ))
    
    return JsonResponse({
        'personal_requerido': ficha.personal_requerido,
        'personal_asignado': personal_asignado,
        'cantidad_bebes': ficha.cantidad_bebes
    })


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
            fecha_inicio = request.POST.get(f'medicamentos[{index}][fecha_inicio]')
            fecha_termino = request.POST.get(f'medicamentos[{index}][fecha_termino]')
            
            MedicamentoFicha.objects.create(
                ficha=ficha,
                medicamento=med_nombre,
                dosis=request.POST.get(f'medicamentos[{index}][dosis]', ''),
                via_administracion_id=via_id if via_id else None,
                cantidad=int(request.POST.get(f'medicamentos[{index}][cantidad]', 1)),
                frecuencia=request.POST.get(f'medicamentos[{index}][frecuencia]', ''),
                fecha_inicio=fecha_inicio if fecha_inicio else timezone.now(),
                fecha_termino=fecha_termino if fecha_termino else None,
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
                fecha_hora=hora if hora else timezone.now(),
                valor_dilatacion=int(valor),
                observacion=request.POST.get(f'dilatacion[{index}][observacion]', ''),
                registrado_por=request.user
            )
        index += 1
    
    # Verificar estado después de agregar registros
    ficha.verificar_estancamiento()
    if ficha.puede_parto_vaginal():
        ficha.estado_dilatacion = 'LISTA'
        ficha.save(update_fields=['estado_dilatacion'])


def asignar_personal_parto(ficha):
    """
    Asigna automáticamente el personal requerido para el parto.
    Basado en la cantidad de bebés.
    """
    from django.contrib.auth.models import User, Group
    
    personal_requerido = ficha.personal_requerido
    
    # Intentar asignar personal por rol
    for rol, cantidad in [('MEDICO', personal_requerido['medicos']),
                          ('MATRONA', personal_requerido['matronas']),
                          ('TENS', personal_requerido['tens'])]:
        try:
            # Buscar usuarios con el grupo correspondiente
            grupo = Group.objects.filter(name__iexact=rol).first()
            if grupo:
                usuarios_disponibles = User.objects.filter(
                    groups=grupo, 
                    is_active=True
                ).exclude(
                    asignaciones_parto__ficha=ficha,
                    asignaciones_parto__activo=True
                )[:cantidad]
                
                for i, usuario in enumerate(usuarios_disponibles):
                    PersonalAsignadoParto.objects.create(
                        ficha=ficha,
                        usuario=usuario,
                        rol=rol,
                        bebe_numero=(i % ficha.cantidad_bebes) + 1
                    )
        except Exception:
            # Si hay error, crear asignaciones vacías
            for i in range(cantidad):
                PersonalAsignadoParto.objects.create(
                    ficha=ficha,
                    usuario=None,
                    rol=rol,
                    bebe_numero=(i % ficha.cantidad_bebes) + 1
                )