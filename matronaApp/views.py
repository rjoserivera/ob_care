"""
matronaApp/views.py
Vistas para matronaApp - Fichas obstÃ©tricas, medicamentos, dilatación y parto
COMPLETO: Con TODAS las vistas existentes + nuevas funcionalidades
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
# Force reload - ARO updated
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.utils import timezone
from legacyApp.models import ControlesPrevios # Importación explícita
from django.db import transaction
from django.db.models import Q, Count, Case, When, Value, IntegerField
from datetime import date
import json
from django.utils.dateparse import parse_datetime
from gestionProcesosApp.models import AsignacionPersonal, PersonalTurno

# Sistema de encriptación de URLs
from gestionApp.decorators import decrypt_url_params
from gestionApp.url_encryption import decrypt_id, encrypt_id

# ============================================
# IMPORTACIONES DE MODELOS
# ============================================

# Modelos de gestionApp (Persona, Paciente, etc.)
from gestionApp.models import Persona, Paciente, CatalogoParentesco

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
from ingresoPartoApp.models import FichaParto
# Nuevos imports para Parto y RN
from partosApp.models import (
    RegistroParto, CatalogoTipoParto, CatalogoPosicionParto, CatalogoEstadoPerine, 
    CatalogoClasificacionRobson, CatalogoCausaCesarea, CatalogoMotivoPartoNoAcompanado, 
    CatalogoPersonaAcompanante, CatalogoMetodoNoFarmacologico, CatalogoTipoEsterilizacion,
    CatalogoRegimenParto, CatalogoTipoRoturaMembrana
)
from recienNacidoApp.models import RegistroRecienNacido, CatalogoSexoRN, CatalogoComplicacionesRN, CatalogoMotivoHospitalizacionRN
from django.contrib.auth.models import User
from legacyApp.models import ControlesPrevios

# Formularios
from .forms import FichaObstetricaForm, MedicamentoFichaForm
from .forms.parto_forms import RegistroPartoForm, RegistroRecienNacidoForm # NEW


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

# ============================================
# MENU MATRONA (DASHBOARD)
# ============================================

from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from authentication.utils import user_has_role

@method_decorator(login_required, name='dispatch')
class DashboardMatronaView(TemplateView):
    template_name = "Matrona/Data/dashboard_matrona.html"
    
    def dispatch(self, request, *args, **kwargs):
        # Permitir matronas y superusuarios
        if not (user_has_role(request.user, "matrona") or request.user.is_superuser):
            messages.error(request, "No tienes permisos para acceder al dashboard de matrona.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['titulo'] = 'Dashboard Matrona'
        context['usuario'] = self.request.user
        
        
        # 1. Fichas Activas
        context['total_fichas'] = FichaObstetrica.objects.filter(activa=True).count()
        
        from django.contrib.auth.models import Group
        
        try:
            medico_group = Group.objects.get(name='Medico')
            context['total_medicos'] = medico_group.user_set.filter(is_active=True).count()
        except Group.DoesNotExist:
            context['total_medicos'] = 0

        try:
            matronas_group = Group.objects.get(name='Matrona')
            context['total_matronas'] = matronas_group.user_set.filter(is_active=True).count()
        except Group.DoesNotExist:
            context['total_matronas'] = 0

        try:
            tens_group = Group.objects.get(name='TENS')
            context['total_tens'] = tens_group.user_set.filter(is_active=True).count()
        except Group.DoesNotExist:
            context['total_tens'] = 0

        # Permisos
        context['puede_ingresar_paciente'] = True
        context['puede_asignar_medicamentos'] = True
        context['puede_buscar_paciente'] = True
        context['puede_editar_ficha'] = True
        context['puede_iniciar_parto'] = False
        
        return context

# Mantener soporte para URL antigua si es necesario, o redirigir
menu_matrona = DashboardMatronaView.as_view()


# ============================================
# SELECCIONAR PERSONA PARA FICHA
# ============================================

@login_required
def seleccionar_persona_ficha(request):
    """
    Buscar y seleccionar persona para crear ficha obstÃ©trica
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
    
    # Verificar permisos para crear personas (Solo Matrona y Admin)
    puede_registrar = user_has_role(request.user, 'matrona') or request.user.is_superuser

    context = {
        'titulo': 'Seleccionar Persona para Ficha Obstétrica',
        'personas': personas,
        'busqueda': busqueda,
        'puede_registrar': puede_registrar,
    }
    return render(request, 'Matrona/seleccionar_persona_ficha.html', context)


# ============================================
# CREAR FICHA OBSTÃ‰TRICA - DESDE PACIENTE
# ============================================

@login_required
def crear_ficha_obstetrica(request, paciente_pk):
    """
    Crear nueva ficha obstÃ©trica a partir de un Paciente existente
    URL: /matrona/ficha/crear/<paciente_pk>/
    """
    paciente = get_object_or_404(Paciente, pk=paciente_pk)
    persona = paciente.persona
    
    # Verificar si ya tiene ficha activa
    ficha_existente = FichaObstetrica.objects.filter(paciente=paciente, activa=True).first()
    if ficha_existente:
        messages.warning(request, 'Esta paciente ya tiene una ficha obstÃ©trica activa.')
        return redirect('matrona:detalle_ficha', ficha_pk=encrypt_id(ficha_existente.pk))
    
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
                
                messages.success(request, f'âœ… Ficha Obstétrica {ficha.numero_ficha} creada exitosamente')
                return redirect('matrona:detalle_ficha', ficha_pk=encrypt_id(ficha.pk))
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = FichaObstetricaForm()
    
    # CatÃ¡logos para el template
    vias_administracion = CatalogoViaAdministracion.objects.filter(activo=True)
    consultorios = CatalogoConsultorioOrigen.objects.filter(activo=True)
    
    



# ============================================
# CREAR FICHA OBSTÃ‰TRICA - DESDE PERSONA
# ============================================

@login_required
def crear_ficha_obstetrica_persona(request, persona_pk):
    """
    Crear nueva ficha obstÃ©trica a partir de una Persona
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
        messages.warning(request, 'Esta paciente ya tiene una ficha obstÃ©trica activa.')
        return redirect('matrona:detalle_ficha', ficha_pk=encrypt_id(ficha_existente.pk))
    
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
                
                messages.success(request, f'âœ… Ficha Obstétrica {ficha.numero_ficha} creada exitosamente')
                return redirect('matrona:detalle_ficha', ficha_pk=encrypt_id(ficha.pk))
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = FichaObstetricaForm()
    
    # CatÃ¡logos para el template
    vias_administracion = CatalogoViaAdministracion.objects.filter(activo=True)
    consultorios = CatalogoConsultorioOrigen.objects.filter(activo=True)
    
    # Obtener controles previos si existen
    controles_previos = ControlesPrevios.objects.filter(
        paciente_rut=persona.Rut
    ).order_by('-fecha_control')[:20]

    from ingresoPartoApp.models import CatalogoDerivacion

    context = {
        'form': form,
        'paciente': paciente,
        'persona': persona,
        'edad': edad,
        'titulo': 'Crear Ficha Obstétrica',
        'accion': 'crear',
        'vias_administracion': vias_administracion,
        'consultorios': consultorios,
        'controles_previos': controles_previos,
        'derivaciones_hepatitis': CatalogoDerivacion.objects.filter(activo=True),
        'parentescos': CatalogoParentesco.objects.filter(activo=True).order_by('orden', 'nombre'),
    }
    return render(request, 'Matrona/crear_ficha_obstetrica.html', context)


# ============================================
# EDITAR FICHA OBSTÃ‰TRICA
# ============================================

@login_required
@decrypt_url_params('ficha_pk')
def editar_ficha_obstetrica(request, ficha_pk):
    """
    Editar ficha obstÃ©trica existente
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
                
                messages.success(request, f'âœ… Ficha {ficha.numero_ficha} actualizada')
                return redirect('matrona:detalle_ficha', ficha_pk=encrypt_id(ficha.pk))
    else:
        form = FichaObstetricaForm(instance=ficha)
    
    # Obtener datos existentes
    medicamentos = ficha.medicamentos.filter(activo=True)
    registros_dilatacion = ficha.registros_dilatacion.all().order_by('fecha_hora')
    
    # CatÃ¡logos para el template
    vias_administracion = CatalogoViaAdministracion.objects.filter(activo=True)
    consultorios = CatalogoConsultorioOrigen.objects.filter(activo=True)

    # Obtener controles previos si existen
    controles_previos = ControlesPrevios.objects.filter(
        paciente_rut=persona.Rut
    ).order_by('-fecha_control')[:20]
    
    from ingresoPartoApp.models import CatalogoDerivacion
    
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
        'controles_previos': controles_previos,
        'derivaciones_hepatitis': CatalogoDerivacion.objects.filter(activo=True),
        'parentescos': CatalogoParentesco.objects.filter(activo=True).order_by('orden', 'nombre'),
    }
    return render(request, 'Matrona/crear_ficha_obstetrica.html', context)


# ============================================
# DETALLE FICHA OBSTÃ‰TRICA
# ============================================

@login_required
@decrypt_url_params('ficha_pk')
def detalle_ficha_obstetrica(request, ficha_pk):
    """
    Ver detalle de ficha obstÃ©trica
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
    
    # Obtener controles previos desde la base de datos legacy
    controles_previos = ControlesPrevios.objects.filter(
        paciente_rut=persona.Rut
    ).order_by('-fecha_control')[:20]  # Últimos 20 controles
    
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
        'edad_gestacional': f"{ficha.edad_gestacional_semanas or 0}+{ficha.edad_gestacional_dias or 0}",
        'controles_previos': controles_previos,
        'vias_administracion': CatalogoViaAdministracion.objects.filter(activo=True),
        'medicamentos_catalogo': CatalogoMedicamento.objects.filter(activo=True).order_by('nombre'),
    }
    return render(request, 'Matrona/detalle_ficha_obstetrica.html', context)


# ============================================
# LISTA DE FICHAS OBSTÃ‰TRICAS
# ============================================

@login_required
def lista_fichas_obstetrica(request):
    """
    Listar todas las fichas obstÃ©tricas
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
    
    # Acción (editar vs ver)
    accion = request.GET.get('accion', '')
    titulo = 'Seleccionar Ficha para Editar' if accion == 'editar' else 'Fichas Obstétricas'

    context = {
        'fichas': fichas,
        'titulo': titulo,
        'estado_filtro': estado,
        'busqueda': busqueda,
        'accion': accion,
    }
    return render(request, 'Matrona/lista_fichas_obstetrica.html', context)


# ============================================
# MEDICAMENTOS - AGREGAR
# ============================================

@login_required
@decrypt_url_params('ficha_pk')
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
            messages.success(request, f'âœ… Medicamento "{medicamento.nombre_display}" agregado')
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
        messages.success(request, 'âœ… Medicamento eliminado')
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
@decrypt_url_params('ficha_pk')
def agregar_medicamento_ajax(request, ficha_pk):
    """
    API para agregar medicamento vía AJAX
    URL: /matrona/api/ficha/<ficha_pk>/medicamento/agregar/
    """
    try:
        ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk, activa=True)
        
        data = json.loads(request.body)
        
        # Parse fecha_inicio
        fecha_inicio = timezone.now()
        if data.get('fecha_inicio'):
            try:
                fecha_inicio = parse_datetime(data.get('fecha_inicio'))
                if not fecha_inicio:  # parse_datetime returns None if invalid
                    fecha_inicio = timezone.now()
            except:
                fecha_inicio = timezone.now()
        
        # Parse fecha_termino
        fecha_termino = None
        if data.get('fecha_termino'):
            try:
                fecha_termino = parse_datetime(data.get('fecha_termino'))
            except:
                fecha_termino = None
        
        medicamento = MedicamentoFicha.objects.create(
            ficha=ficha,
            medicamento=data.get('medicamento', ''),
            medicamento_catalogo_id=data.get('medicamento_catalogo_id'),
            dosis=data.get('dosis', ''),
            via_administracion_id=data.get('via_administracion_id'),
            frecuencia=data.get('frecuencia', ''),
            cantidad=int(data.get('cantidad', 1)),
            fecha_inicio=fecha_inicio,
            fecha_termino=fecha_termino,
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
    except json.JSONDecodeError as e:
        return JsonResponse({'success': False, 'error': f'JSON inválido: {str(e)}'}, status=400)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


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
# MEDICAMENTOS - BUSCAR EN CATÃ�LOGO
# ============================================

@login_required
def buscar_medicamentos(request):
    """
    API para buscar medicamentos en el catÃ¡logo
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
# DILATACIÃ“N - AGREGAR REGISTRO (AJAX)
# ============================================

@login_required
@require_POST
@decrypt_url_params('ficha_pk')
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
                return redirect('matrona:detalle_ficha', ficha_pk=encrypt_id(ficha.pk))
        
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
        
        messages.success(request, f'âœ… Dilatación registrada: {valor} cm')
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
# DILATACIÃ“N - VERIFICAR ESTADO
# ============================================

@login_required
@decrypt_url_params('ficha_pk')
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
@decrypt_url_params('ficha_pk')
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
        generar_placeholders_personal(ficha)
        
        tipo_texto = 'parto vaginal' if tipo_parto == 'VAGINAL' else 'cesárea'
        messages.success(request, f'Proceso de {tipo_texto} iniciado exitosamente.')
    
    # Redirigir a página dedicada de proceso de parto
    return redirect('matrona:proceso_parto_iniciado', ficha_pk=encrypt_id(ficha.pk))


# ============================================
# PARTO - PROCESO INICIADO
# ============================================

@login_required
@decrypt_url_params('ficha_pk')
def proceso_parto_iniciado(request, ficha_pk):
    """
    Centro de Control - Sala de Preparación (REDISEÑADO)
    Muestra estadísticas, equipo confirmado, salas disponibles y PIN
    """
    from ingresoPartoApp.models import FichaParto
    from django.utils import timezone
    from gestionProcesosApp.models import Notificacion, PersonalTurno, AsignacionPersonal, Sala
    from gestionProcesosApp.pin_utils import equipo_completo

    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk)
    
    # 1. Obtener o Crear Ficha de Parto
    ficha_parto, created = FichaParto.objects.get_or_create(
        ficha_obstetrica=ficha,
        defaults={
            'numero_ficha_parto': f"P-{ficha.numero_ficha}",
            'fecha_ingreso': timezone.now().date(),
            'hora_ingreso': timezone.now().time(),
            'creado_por': request.user
        }
    )

    # 1.5 Auto-Confirmar al usuario actual si es personal clínico (NO ADMIN puro)
    # "El usuario llega a esta ventana y pasa a confirmarse automáticamente"
    # Buscar si tiene turno activo
    current_turno = PersonalTurno.objects.filter(
        usuario=request.user, 
        estado='DISPONIBLE',
        fecha_fin_turno__gte=timezone.now()
    ).first()

    if current_turno and current_turno.rol in ['MEDICO', 'MATRONA', 'TENS']:
        # Verificar si ya existe asignación
        if not AsignacionPersonal.objects.filter(proceso=ficha_parto, personal=current_turno).exists():
            AsignacionPersonal.objects.create(
                proceso=ficha_parto,
                personal=current_turno,
                estado_respuesta='ACEPTADA',
                confirmo_asistencia=True,
                timestamp_confirmacion=timezone.now(),
                timestamp_notificacion=timezone.now() # Fake notification time
            )
            # Opcional: Feedback al usuario
            # messages.success(request, f"Te has unido al equipo como {current_turno.rol}")

    # 2. Calcular Requerimientos
    # 2. Calcular Requerimientos
    cantidad_bebes = ficha_parto.ficha_obstetrica.cantidad_bebes
    if cantidad_bebes < 1: cantidad_bebes = 1
    
    medicos_req = cantidad_bebes * 1
    matronas_req = cantidad_bebes * 2
    tens_req = cantidad_bebes * 3

    # 3. Obtener Asignaciones
    asignaciones = AsignacionPersonal.objects.filter(proceso=ficha_parto)
    
    # 4. Calcular Estadísticas
    stats = {
        'enviados': asignaciones.count(),
        'aceptados': asignaciones.filter(estado_respuesta='ACEPTADA').count(),
        'pendientes': asignaciones.filter(estado_respuesta='ENVIADA').count(),
        'rechazados': asignaciones.filter(estado_respuesta='RECHAZADA').count(),
    }
    
    # 5. Equipo Aceptado
    asignados_aceptados = asignaciones.filter(estado_respuesta='ACEPTADA').order_by('-timestamp_confirmacion')
    
    # 6. Calcular Slots Pendientes
    medicos_aceptados = asignados_aceptados.filter(personal__rol='MEDICO').count()
    matronas_aceptadas = asignados_aceptados.filter(personal__rol='MATRONA').count()
    tens_aceptados = asignados_aceptados.filter(personal__rol='TENS').count()
    
    slots_pendientes = []
    if medicos_aceptados < medicos_req:
        slots_pendientes.append({'rol': 'Médico', 'cantidad': medicos_req - medicos_aceptados})
            
    if matronas_aceptadas < matronas_req:
        slots_pendientes.append({'rol': 'Matrona', 'cantidad': matronas_req - matronas_aceptadas})
            
    if tens_aceptados < tens_req:
        slots_pendientes.append({'rol': 'TENS', 'cantidad': tens_req - tens_aceptados})
    
    # 7. Verificar si equipo está completo
    equipo_esta_completo = equipo_completo(ficha_parto)
    
    # 7.5 Auto-generar PIN si equipo completo y no existe PIN
    if equipo_esta_completo and not ficha_parto.pin_inicio_parto:
        from gestionProcesosApp.pin_utils import generar_pin, enviar_pin_a_medicos
        pin = generar_pin()
        ficha_parto.pin_inicio_parto = pin
        ficha_parto.pin_generado_en = timezone.now()
        ficha_parto.save(update_fields=['pin_inicio_parto', 'pin_generado_en'])
        
        # Enviar PIN a médicos
        try:
            enviar_pin_a_medicos(ficha_parto, pin)
        except Exception as e:
            print(f"Error enviando PIN: {e}")
    
    # 8. Monitor de Salas
    if Sala.objects.count() == 0:
        Sala.objects.create(nombre="Sala Parto 1", codigo="SP1", capacidad_maxima=1)
        Sala.objects.create(nombre="Sala Parto 2", codigo="SP2", capacidad_maxima=1)
        Sala.objects.create(nombre="Sala Parto 3", codigo="SP3", capacidad_maxima=1)
        
    salas = Sala.objects.all()
    salas_info = []
    
    for sala in salas:
        # Buscar parto activo en esta sala
        parto_activo = FichaParto.objects.filter(
            sala_asignada__nombre=sala.nombre
        ).exclude(pk=ficha_parto.pk).first()
        
        if parto_activo:
            tiempo_transcurrido = timezone.now() - timezone.datetime.combine(
                parto_activo.fecha_ingreso,
                parto_activo.hora_ingreso
            ).replace(tzinfo=timezone.get_current_timezone())
            
            horas = int(tiempo_transcurrido.total_seconds() // 3600)
            minutos = int((tiempo_transcurrido.total_seconds() % 3600) // 60)
            
            salas_info.append({
                'sala': sala,
                'ocupada': True,
                'tiempo_str': f"{horas}h {minutos}min"
            })
        else:
            salas_info.append({
                'sala': sala,
                'ocupada': False
            })
    
    # 9. Personal Disponible (para modal de invitación)
    import json
    now = timezone.now()
    personal_turno = PersonalTurno.objects.filter(
        estado='DISPONIBLE',
        fecha_fin_turno__gte=now
    ).select_related('usuario', 'usuario__perfil')
    
    personal_disponible = []
    for pt in personal_turno:
        personal_disponible.append({
            'id': pt.id,
            'nombre': pt.usuario.get_full_name() or pt.usuario.username,
            'rol': pt.rol,
            'cargo': pt.usuario.perfil.cargo if hasattr(pt.usuario, 'perfil') else ''
        })
    
    # Contar personal disponible por rol
    personal_counts = {
        'MEDICO': PersonalTurno.objects.filter(rol='MEDICO', estado='DISPONIBLE', fecha_fin_turno__gte=now).count(),
        'MATRONA': PersonalTurno.objects.filter(rol='MATRONA', estado='DISPONIBLE', fecha_fin_turno__gte=now).count(),
        'TENS': PersonalTurno.objects.filter(rol='TENS', estado='DISPONIBLE', fecha_fin_turno__gte=now).count(),
    }

    context = {
        'ficha': ficha,
        'ficha_parto': ficha_parto,
        'cantidad_bebes': cantidad_bebes,
        'stats': stats,
        'asignados_aceptados': asignados_aceptados,
        'slots_pendientes': slots_pendientes,
        'equipo_completo': equipo_esta_completo,
        'salas': salas_info,
        'personal_counts': personal_counts,
        'reqs': {
            'medico': medicos_req,
            'matrona': matronas_req,
            'tens': tens_req
        },
        'aceptados_counts': {
            'medico': medicos_aceptados,
            'matrona': matronas_aceptadas,
            'tens': tens_aceptados
        }
    }
    
    return render(request, 'Matrona/proceso_parto_iniciado_simple.html', context)


# ============================================
# PERSONAL - OBTENER REQUERIDO
# ============================================

@login_required
@require_POST
def asignar_personal_parto(request, ficha_parto_id):
    """
    API AJAX para asignar personal y enviar notificación
    URL: /matrona/api/parto/<ficha_pk>/asignar-personal/
    """
    from ingresoPartoApp.models import FichaParto
    from gestionProcesosApp.models import PersonalTurno, Notificacion, AsignacionPersonal
    
    try:
        data = json.loads(request.body)
        personal_id = data.get('personal_id')
        ficha_parto_id = data.get('ficha_parto_id')
        
        # Validar personal
        personal = get_object_or_404(PersonalTurno, pk=personal_id)
        ficha_parto = get_object_or_404(FichaParto, pk=ficha_parto_id)
        
        # Verificar si ya existe asignación
        asignacion_existente = AsignacionPersonal.objects.filter(
            proceso=ficha_parto,
            personal=personal
        ).first()
        
        if asignacion_existente:
            return JsonResponse({
                'success': False,
                'error': f'{personal.usuario.get_full_name()} ya fue invitado'
            })
        
        with transaction.atomic():
            # 1. Crear Asignación
            asignacion = AsignacionPersonal.objects.create(
                proceso=ficha_parto,
                personal=personal,
                rol_en_proceso=personal.rol,  # Usar el rol del PersonalTurno
                observaciones='Asignación desde Sala de Preparación (Matronas)'
            )
            
            # 2. Crear Notificación (Sistema)
            notificacion = Notificacion.objects.create(
                proceso=ficha_parto,
                destinatario=personal,
                tipo='PARTO',
                titulo='URGENTE: Asistencia a Parto',
                mensaje=f"SOLICITUD: Se requiere su presencia de inmediato en la Sala de Parto (Prep). Ficha {ficha_parto.numero_ficha_parto}. Paciente: {ficha_parto.ficha_obstetrica.paciente.persona.nombre_completo}.",
                estado='ENVIADA',
                timestamp_expiracion=timezone.now() + timezone.timedelta(hours=4)
            )

            
            # 3. ENVIAR TELEGRAM (Prioritario)
            print(f"\n{'='*50}")
            print(f"🔔 INTENTANDO ENVIAR NOTIFICACIÓN")
            print(f"Personal: {personal.usuario.get_full_name()}")
            print(f"Ficha: {ficha_parto.numero_ficha_parto}")
            print(f"{'='*50}\n")
            
            try:
                from gestionProcesosApp.telegram_utils import enviar_notificacion_parto
                telegram_enviado = enviar_notificacion_parto(personal, ficha_parto)
                if telegram_enviado:
                    print(f"✅ Telegram enviado a {personal.usuario.get_full_name()}")
                else:
                    print(f"❌ Telegram NO enviado a {personal.usuario.get_full_name()}")
            except Exception as e:
                print(f"⚠️ Error enviando Telegram: {e}")
                import traceback
                traceback.print_exc()
            
            # 4. ENVIAR CORREO (Fallback Automático)
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                
                # Obtener correo del usuario asociado al personal
                email_destino = personal.usuario.email
                if email_destino:
                    asunto = f"🚨 URGENTE: Solicitud de Asistencia - {ficha_parto.numero_ficha_parto}"
                    mensaje_email = f"""
                    Estimado/a {personal.usuario.get_full_name()}:

                    Se requiere su presencia INMEDIATA en la Sala de Parto (Preparación).
                    
                    PACIENTE: {ficha_parto.ficha_obstetrica.paciente.persona.nombre_completo}
                    FICHA: {ficha_parto.numero_ficha_parto}
                    
                    Por favor, confirme su asistencia en el sistema o acuda directamente.
                    
                    Este es un mensaje automático del Sistema de Gestión Obstétrica.
                    """
                    
                    send_mail(
                        asunto,
                        mensaje_email,
                        settings.DEFAULT_FROM_EMAIL,
                        [email_destino],
                        fail_silently=True # No bloquear el proceso si falla el correo
                    )
                    print(f"📧 Correo enviado a {email_destino}")
            except Exception as e:
                print(f"⚠️ Error enviando correo: {e}")
            
            return JsonResponse({
                'success': True,
                'message': f'Solicitud enviada a {personal.usuario.get_full_name()}',
                'asignacion_id': asignacion.id,
                'nuevo_estado': 'Pendiente'
            })
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_POST
def finalizar_asignacion_parto(request, ficha_parto_id):
    """
    Finaliza la asignación y notifica a TODO el equipo confirmado.
    "oseas todos" -> Enviar resumen a todos los involucrados.
    """
    try:
        ficha = get_object_or_404(FichaParto, pk=ficha_parto_id)
        
        # Obtener todos los asignados
        asignados = AsignacionPersonal.objects.filter(proceso=ficha)
        
        if not asignados.exists():
            return JsonResponse({'success': False, 'error': 'No hay personal asignado para notificar.'})

        # Recopilar correos y nombres
        emails_destino = []
        nombres_equipo = []
        
        for a in asignados:
            if a.personal.usuario.email:
                emails_destino.append(a.personal.usuario.email)
            nombres_equipo.append(f"- {a.personal.usuario.get_full_name()} ({a.personal.get_rol_display()})")
            
        if not emails_destino:
            return JsonResponse({'success': True, 'message': 'Asignación finalizada (Sin correos para notificar).'})

        # Enviar Correo Masivo (Resumen)
        from django.core.mail import send_mail
        from django.conf import settings
        
        asunto = f"✅ EQUIPO CONFIRMADO: Parto Ficha {ficha.numero_ficha_parto}"
        lista_equipo = "\n".join(nombres_equipo)
        
        mensaje = f"""
        Estimado equipo:
        
        Se ha confirmado el equipo completo para la atención de parto.
        
        PACIENTE: {ficha.ficha_obstetrica.paciente.persona.nombre_completo}
        FICHA: {ficha.numero_ficha_parto}
        
        EQUIPO ASIGNADO:
        {lista_equipo}
        
        Por favor, coordinar ingreso a pabellón/sala.
        """
        
        send_mail(
            asunto,
            mensaje,
            settings.DEFAULT_FROM_EMAIL,
            emails_destino, # Lista de todos los destinatarios
            fail_silently=True
        )
        
        return JsonResponse({'success': True, 'message': f'Notificación enviada a {len(emails_destino)} profesionales.'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_POST
def responder_asignacion(request, asignacion_id):
    """
    Endpoint para que el personal acepte o rechace una asignación
    """
    try:
        asignacion = get_object_or_404(AsignacionPersonal, pk=asignacion_id)
        data = json.loads(request.body)
        accion = data.get('accion')  # 'aceptar' o 'rechazar'
        
        if accion == 'aceptar':
            asignacion.estado_respuesta = 'ACEPTADA'
            asignacion.confirmo_asistencia = True
            asignacion.timestamp_confirmacion = timezone.now()
            asignacion.save()
            
            # Verificar si el equipo está completo
            from gestionProcesosApp.pin_utils import equipo_completo, generar_pin, enviar_pin_a_medicos
            
            if equipo_completo(asignacion.proceso):
                # Generar PIN
                pin = generar_pin()
                asignacion.proceso.pin_inicio_parto = pin
                asignacion.proceso.pin_generado_en = timezone.now()
                asignacion.proceso.save()
                
                # Enviar PIN solo a médicos que aceptaron
                enviar_pin_a_medicos(asignacion.proceso, pin)
                
                return JsonResponse({
                    'success': True,
                    'message': 'Asignación aceptada. Equipo completo - PIN generado.',
                    'equipo_completo': True
                })
            
            return JsonResponse({
                'success': True,
                'message': 'Asignación aceptada',
                'equipo_completo': False
            })
        
        elif accion == 'rechazar':
            asignacion.estado_respuesta = 'RECHAZADA'
            asignacion.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Asignación rechazada'
            })
        
        else:
            return JsonResponse({'success': False, 'error': 'Acción inválida'}, status=400)
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_POST
def verificar_pin(request, ficha_parto_id):
    """
    Verifica el PIN ingresado y ASIGNA LA SALA seleccionada.
    """
    try:
        ficha = get_object_or_404(FichaParto, pk=ficha_parto_id)
        data = json.loads(request.body)
        pin_ingresado = data.get('pin', '').strip()
        sala_id = data.get('sala_id')
        
        if not ficha.pin_inicio_parto:
            return JsonResponse({'success': False, 'error': 'No se ha generado un PIN. El equipo debe estar completo.'}, status=400)
        
        if pin_ingresado == ficha.pin_inicio_parto:
            # PIN Correcto. Asignar Sala si se envió
            if sala_id:
                from gestionProcesosApp.models import Sala
                sala = get_object_or_404(Sala, pk=sala_id)
                
                # Verificar ocupación (doble check)
                if sala.proceso_activo and sala.proceso_activo != ficha:
                    return JsonResponse({'success': False, 'error': f'La sala {sala.nombre} ya fue ocupada.'}, status=400)
                
                sala.proceso_activo = ficha
                sala.estado = 'OCUPADA'
                sala.save()

            # ============================================
            # PERSISTENCIA DEL EQUIPO (MIGRACIÓN)
            # ============================================
            from gestionProcesosApp.models import AsignacionPersonal
            from matronaApp.models import PersonalAsignadoParto

            # 1. Limpiar asignaciones previas para esta ficha (evitar duplicados si re-inician)
            PersonalAsignadoParto.objects.filter(ficha=ficha.ficha_obstetrica).delete()

            # 2. Buscar aceptados del panel de preparación
            asignaciones_aceptadas = AsignacionPersonal.objects.filter(
                proceso=ficha,
                estado_respuesta='ACEPTADA'
            ).select_related('personal__usuario')

            # 3. Crear registros permanentes
            for asignacion in asignaciones_aceptadas:
                # Determinar rol normalizado
                rol_final = 'TENS'
                if asignacion.rol_en_proceso == 'MEDICO': rol_final = 'MEDICO'
                elif asignacion.rol_en_proceso == 'MATRONA': rol_final = 'MATRONA'
                
                PersonalAsignadoParto.objects.create(
                    ficha=ficha.ficha_obstetrica,
                    usuario=asignacion.personal.usuario,
                    rol=rol_final,
                    activo=True,
                    bebe_numero=1 # Por defecto 1, lógica compleja pendiente si hay múltiples
                )
            
            from django.urls import reverse
            return JsonResponse({
                'success': True,
                'message': 'PIN Correcto. Iniciando...',
                'redirect_url': reverse('matrona:sala_parto', args=[ficha.id])
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'PIN INCORRECTO'
            }, status=403)
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@decrypt_url_params('ficha_pk')
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
    
    # Verificar estado despuÃ©s de agregar registros
    ficha.verificar_estancamiento()
    if ficha.puede_parto_vaginal():
        ficha.estado_dilatacion = 'LISTA'
        ficha.save(update_fields=['estado_dilatacion'])


def generar_placeholders_personal(ficha):
    """
    Asigna automáticamente placeholders para el personal requerido
    según la cantidad de bebés (1 Médico, 2 Matronas, 2 TENS por bebé)
    (Renamed from asignar_personal_parto to avoid collision with view)
    """
    try:
        # Si ya existe personal asignado, no hacemos nada
        if PersonalAsignadoParto.objects.filter(ficha=ficha).exists():
            return

        # Iterar por cada bebé
        for i in range(ficha.cantidad_bebes):
            bebe_num = i + 1
            
            # 1 Médico
            PersonalAsignadoParto.objects.create(
                ficha=ficha, rol='MEDICO', bebe_numero=bebe_num
            )
            
            # 2 Matronas
            PersonalAsignadoParto.objects.create(
                ficha=ficha, rol='MATRONA', bebe_numero=bebe_num
            )
            PersonalAsignadoParto.objects.create(
                ficha=ficha, rol='MATRONA', bebe_numero=bebe_num
            )
            
            # 2 TENS -> 3 TENS per baby
            PersonalAsignadoParto.objects.create(
                ficha=ficha, rol='TENS', bebe_numero=bebe_num
            )
            PersonalAsignadoParto.objects.create(
                ficha=ficha, rol='TENS', bebe_numero=bebe_num
            )
            PersonalAsignadoParto.objects.create(
                ficha=ficha, rol='TENS', bebe_numero=bebe_num
            )
            
    except Exception as e:
        print(f"Error asignando personal de parto: {e}")


# ============================================
# REGISTRO DILATACIÓN (AJAX)
# ============================================

@require_POST
@login_required
@decrypt_url_params('ficha_id')
def registrar_dilatacion(request, ficha_id):
    """
    Registra una nueva dilatación para la ficha obstétrica
    """
    try:
        ficha = get_object_or_404(FichaObstetrica, id=ficha_id)
        
        # Obtener datos del request
        valor = request.POST.get('valor_dilatacion')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        observacion = request.POST.get('observacion', '')

        print(f"DEBUG REGISTRO DILATACION: valor={valor}, fecha={fecha}, hora={hora} | User: {request.user}")
        
        if not all([valor, fecha, hora]):
            return JsonResponse({
                'status': 'error',
                'message': 'Faltan campos obligatorios'
            }, status=400)
            
        # Crear fecha_hora combinada
        from datetime import datetime
        from decimal import Decimal
        
        # Handle decimal separator
        valor = valor.replace(',', '.')
        
        fecha_hora_str = f"{fecha} {hora}"
        try:
            fecha_hora_naive = datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M')
            fecha_hora = timezone.make_aware(fecha_hora_naive)
        except ValueError:
             return JsonResponse({'status': 'error', 'message': 'Formato de fecha/hora inválido'}, status=400)

        
        with transaction.atomic():
            # Crear registro
            registro = RegistroDilatacion.objects.create(
                ficha=ficha,
                valor_dilatacion=Decimal(valor),
                fecha_hora=fecha_hora,
                observacion=observacion,
                registrado_por=request.user
            )
            
            # Actualizar estado de ficha
            ficha.verificar_estancamiento()
            
            # Verificar si está lista para parto
            val = Decimal(valor)
            if val >= 8:
                ficha.estado_dilatacion = 'LISTA'
                ficha.save(update_fields=['estado_dilatacion'])
            elif val > ficha.valor_dilatacion_actual and ficha.estado_dilatacion != 'LISTA' and ficha.estado_dilatacion != 'ESTANCADA':
                ficha.estado_dilatacion = 'PROGRESANDO'
                ficha.save(update_fields=['estado_dilatacion'])
                
        return JsonResponse({
            'status': 'success',
            'message': 'Dilatación registrada correctamente',
            'valor_actual': ficha.valor_dilatacion_actual,
            'estado': ficha.estado_dilatacion
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)



# ============================================
# VISTA CIERRE DE PARTO (NUEVO)
# ============================================

@login_required
def cierre_parto_view(request, ficha_parto_id):
    """
    Vista final para Checklist Ley Dominga y Cierre de Ficha.
    """
    ficha_parto = get_object_or_404(FichaParto, pk=ficha_parto_id)
    
    if request.method == 'POST':
        # Validar Ley Dominga
        ley_dominga = request.POST.get('ley_dominga_informada') == 'on'
        obs = request.POST.get('observaciones_cierre', '')
        
        # 1. Guardar info de cierre
        # Si no hay campos aun, lo haremos en observaciones del parto o similares
        # ficha_parto.observaciones = f"{ficha_parto.observaciones or ''} [Cierre: {obs}, LeyDominga: {ley_dominga}]"
        
        # 2. Cerrar Ficha y Liberar Sala
        ficha_parto.estado_proceso = 'FINALIZADO'
        if ficha_parto.sala_asignada:
            # Liberar sala
            sala = ficha_parto.sala_asignada
            sala.proceso_activo = None
            sala.estado = 'DISPONIBLE'
            sala.save()
            
            # Desvincular sala
            ficha_parto.sala_asignada = None
        
        ficha_parto.save()
        
        # Redirigir a listado o Dashboard
        messages.success(request, f'Proceso de parto finalizado para ficha {ficha_parto.numero_ficha_parto}. Sala liberada.')
        return redirect('matrona:resumen_final_parto', ficha_parto_id=ficha_parto.id)

    # Detectar si hay mortinato para activar Ley Dominga
    has_mortinato = False
    try:
        if hasattr(ficha_parto, 'registro_parto'):
            # Accessing related name or querying directly
            from recienNacidoApp.models import RegistroRecienNacido
            has_mortinato = RegistroRecienNacido.objects.filter(
                registro_parto=ficha_parto.registro_parto, 
                es_mortinato=True
            ).exists()
    except Exception:
        pass

    return render(request, 'Matrona/cierre_parto.html', {
        'ficha': ficha_parto,
        'has_mortinato': has_mortinato
    })

# ============================================
# DEBUG - AUTO RELLENAR EQUIPO
# ============================================

@login_required
@require_POST
def debug_rellenar_equipo(request, ficha_parto_id):
    """
    Vista DEBUG para rellenar automáticamente el equipo, confirmar asistencia y generar PIN.
    Soporta múltiples asignaciones por rol (ej: 2 Matronas).
    """
    try:
        from ingresoPartoApp.models import FichaParto
        from gestionProcesosApp.models import AsignacionPersonal, PersonalTurno
        from gestionProcesosApp.pin_utils import equipo_completo, generar_pin, enviar_pin_a_medicos
        from django.contrib.auth.models import User
        from datetime import timedelta
        
        ficha_parto = get_object_or_404(FichaParto, pk=ficha_parto_id)
        
        # Calcular requerimientos
        cantidad_bebes = ficha_parto.ficha_obstetrica.cantidad_bebes
        if cantidad_bebes < 1: cantidad_bebes = 1
        
        target_map = {
            'MEDICO': cantidad_bebes * 1,
            'MATRONA': cantidad_bebes * 2,
            'TENS': cantidad_bebes * 3
        }
        
        asignados_nuevos = 0
        
        for rol, target_count in target_map.items():
            actual_count = AsignacionPersonal.objects.filter(
                proceso=ficha_parto,
                rol_en_proceso=rol,
                estado_respuesta='ACEPTADA'
            ).count()
            
            needed = target_count - actual_count
            
            if needed > 0:
                # Buscar candidatos disponibles reales
                candidatos = list(PersonalTurno.objects.filter(
                    rol=rol, 
                    estado='DISPONIBLE'
                ).exclude(
                    asignacionpersonal__proceso=ficha_parto
                )[:needed])
                
                # Si faltan, crear dummies
                import uuid
                while len(candidatos) < needed:
                    idx = len(candidatos) + actual_count + 1
                    username = f'dummy_{rol.lower()}_{uuid.uuid4().hex[:8]}'
                    
                    user_dummy, _ = User.objects.get_or_create(
                        username=username,
                        defaults={'first_name': f'{rol.capitalize()}', 'last_name': 'Debug'}
                    )
                    
                    p_dummy, _ = PersonalTurno.objects.get_or_create(
                        usuario=user_dummy,
                        defaults={
                            'rol': rol,
                            'estado': 'DISPONIBLE',
                            'fecha_inicio_turno': timezone.now(),
                            'fecha_fin_turno': timezone.now() + timedelta(hours=12),
                            'dispositivo_activo': True
                        }
                    )
                    candidatos.append(p_dummy)
                
                # Asignar (update_or_create para evitar duplicados de rol+personal+proceso)
                for cand in candidatos:
                    AsignacionPersonal.objects.update_or_create(
                        proceso=ficha_parto,
                        personal=cand,
                        rol_en_proceso=rol,
                        defaults={
                            'estado_respuesta': 'ACEPTADA',
                            'confirmo_asistencia': True,
                            'timestamp_confirmacion': timezone.now(),
                            'observaciones': 'Asignación Automática DEBUG'
                        }
                    )
                    asignados_nuevos += 1
        
        # Verificar y Generar PIN
        pin = None
        # Recargar para asegurar conteo actualizado en equipo_completo (aunque verify query de DB)
        if equipo_completo(ficha_parto):
            if not ficha_parto.pin_inicio_parto: 
                pin = generar_pin()
                ficha_parto.pin_inicio_parto = pin
                ficha_parto.pin_generado_en = timezone.now()
                ficha_parto.save()
                ficha_parto.save()
                enviar_pin_a_medicos(ficha_parto, pin)
                
                return JsonResponse({
                    'success': True,
                    'asignados': asignados_nuevos,
                    'pin': pin,
                    'message': f'Equipo relleno. PIN generado: {pin}'
                })
                # Re-enviar PIN si ya existe (para pruebas)
                enviar_pin_a_medicos(ficha_parto, pin)
                
                return JsonResponse({
            'success': True,
            'asignados': asignados_nuevos,
            'pin': pin,
            'message': f'Equipo relleno. PIN: {pin} (Enviado a médicos)'
        })
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ============================================
# VISTA SALA DE PARTO (NUEVO)
# ============================================

@login_required
@login_required
def sala_parto_view(request, ficha_parto_id):
    """
    Vista principal de la Sala de Parto (SOLO MATERNA).
    RNs se gestionan en vistas separadas.
    """
    ficha_parto = get_object_or_404(FichaParto, pk=ficha_parto_id)
    
    # 1. Registro de Parto (Evento)
    try:
        registro_parto = ficha_parto.registro_parto
    except Exception: 
        registro_parto = None
        
    # 2. Recién Nacidos (Solo para listarlos y linkearlos)
    recien_nacidos = []
    if registro_parto:
        recien_nacidos = registro_parto.recien_nacidos.all().order_by('fecha_nacimiento', 'hora_nacimiento', 'id')
        
    # Catálogos para Parto (MATERNO)
    tipos_parto = CatalogoTipoParto.objects.filter(activo=True).order_by('orden')
    posiciones = CatalogoPosicionParto.objects.filter(activo=True).order_by('orden')
    robsons = CatalogoClasificacionRobson.objects.filter(activo=True).order_by('numero_grupo')
    perines = CatalogoEstadoPerine.objects.filter(activo=True).order_by('orden')
    causas_cesarea = CatalogoCausaCesarea.objects.filter(activo=True).order_by('orden')
    motivos_no_acompanado = CatalogoMotivoPartoNoAcompanado.objects.filter(activo=True).order_by('orden')
    personas_acompanante = CatalogoPersonaAcompanante.objects.filter(activo=True).order_by('orden')
    metodos_no_farm = CatalogoMetodoNoFarmacologico.objects.filter(activo=True).order_by('orden')
    tipos_esterilizacion = CatalogoTipoEsterilizacion.objects.filter(activo=True).order_by('orden')
    regimenes_parto = CatalogoRegimenParto.objects.filter(activo=True).order_by('orden')
    tipos_rotura = CatalogoTipoRoturaMembrana.objects.filter(activo=True).order_by('orden')
    
    # Staff asignado (Filtrado por rol para TAF 6)
    # PersonalAsignadoParto está linkeado a FichaObstetrica, no FichaParto directamente
    staff_asignado = ficha_parto.ficha_obstetrica.personal_asignado.all()
    matronas_staff = staff_asignado.filter(rol='MATRONA')
    tens_staff = staff_asignado.filter(rol='TENS')
    
    return render(request, 'Matrona/sala_parto.html', {
        'ficha_parto': ficha_parto,
        'registro_parto': registro_parto,
        'recien_nacidos': recien_nacidos,
        # Catalogos Maternos
        'tipos_parto': tipos_parto,
        'posiciones': posiciones,
        'robsons': robsons,
        'perines': perines,
        'causas_cesarea': causas_cesarea,
        'motivos_no_acompanado': motivos_no_acompanado,
        'personas_acompanante': personas_acompanante,
        'metodos_no_farm': metodos_no_farm, 
        'tipos_esterilizacion': tipos_esterilizacion,
        'regimenes_parto': regimenes_parto,
        'tipos_rotura': tipos_rotura,
        # Staff
        'matronas_staff': matronas_staff,
        'tens_staff': tens_staff,
        'staff_completo': staff_asignado,
    })

@login_required
def crear_asociacion_rn(request, ficha_parto_id):
    """
    Crea un nuevo RegistroRecienNacido vacío asociado a la FichaParto y redirige a su ficha.
    """
    ficha_parto = get_object_or_404(FichaParto, pk=ficha_parto_id)
    
    # Asegurar que existe RegistroParto
    from partosApp.models import RegistroParto, CatalogoTipoParto, CatalogoPosicionParto, CatalogoEstadoPerine
    
    # Check if existing via Reverse Relation or explicit query
    # The related name in FichaParto is 'registro_parto' (OneToOne)
    if not hasattr(ficha_parto, 'registro_parto') or ficha_parto.registro_parto is None:
        # Pre-populate required fields
        tipo_parto_def = CatalogoTipoParto.objects.first()
        if not tipo_parto_def:
            # Fallback for empty catalog
            tipo_parto_def, _ = CatalogoTipoParto.objects.get_or_create(codigo='VAGINAL', defaults={'descripcion': 'Parto Vaginal'})
            
        eg_semanas = ficha_parto.ficha_obstetrica.edad_gestacional_semanas or 38 # Default if None
            
        rp = RegistroParto.objects.create(
            ficha_ingreso_parto=ficha_parto,
            ficha_obstetrica=ficha_parto.ficha_obstetrica,
            edad_gestacional_semanas=eg_semanas,
            tipo_parto=tipo_parto_def,
            activo=True
        )
    else:
        rp = ficha_parto.registro_parto
        
    # Crear RN
    from recienNacidoApp.models import RegistroRecienNacido, CatalogoSexoRN
    
    # Default Sexo (Indeterminado o primero disponible)
    sexo_default = CatalogoSexoRN.objects.first()
    if not sexo_default:
         sexo_default, _ = CatalogoSexoRN.objects.get_or_create(codigo='IND', defaults={'descripcion': 'Indeterminado'})
    
    rn = RegistroRecienNacido.objects.create(
        registro_parto=rp,
        sexo=sexo_default,
        fecha_nacimiento=timezone.now().date(),
        hora_nacimiento=timezone.now().time(),
        peso_gramos=3000, # Default placeholder
        talla_centimetros=50.0,
        apgar_1_minuto=9,
        apgar_5_minutos=10,
        activo=True
    )
    
    messages.success(request, f"Recién Nacido creado exitosamente.")
    from django.urls import reverse
    url = reverse('matrona:ficha_rn', args=[rn.id]) + '?new=1'
    return redirect(url)

@login_required
def ficha_rn_view(request, rn_id):
    """
    Vista independiente para gestionar un Recién Nacido específico.
    """
    from recienNacidoApp.models import RegistroRecienNacido, CatalogoSexoRN, CatalogoComplicacionesRN, CatalogoMotivoHospitalizacionRN
    
    rn = get_object_or_404(RegistroRecienNacido, pk=rn_id)
    ficha_parto = rn.registro_parto.ficha_ingreso_parto
    
    # Catalogos RN
    sexos = CatalogoSexoRN.objects.filter(activo=True).order_by('orden')
    complicaciones_rn = CatalogoComplicacionesRN.objects.filter(activo=True).order_by('orden')
    motivos_hospitalizacion = CatalogoMotivoHospitalizacionRN.objects.filter(activo=True).order_by('orden')
    
    # Staff asignado (para asociar responsables RN)
    staff_asignado = ficha_parto.ficha_obstetrica.personal_asignado.all()
    matronas_staff = staff_asignado.filter(rol='MATRONA')
    tens_staff = staff_asignado.filter(rol='TENS')
    
    # Handle POST - Save Data
    if request.method == "POST":
        try:
            # 1. Identificación y Antropometría
            rn.fecha_nacimiento = request.POST.get('fecha_nacimiento')
            rn.hora_nacimiento = request.POST.get('hora_nacimiento')
            rn.sexo_id = request.POST.get('sexo')
            
            # NUEVO: Estado Born Dead (Ley Dominga)
            rn.es_mortinato = 'es_mortinato' in request.POST
            
            if rn.es_mortinato:
                # GUARDAR SOLO LEY DOMINGA (y defaults requeridos)
                rn.ley_dominga_brazalete = 'ld_brazalete' in request.POST
                rn.ley_dominga_huellas = 'ld_huellas' in request.POST
                rn.ley_dominga_pelo = 'ld_pelo' in request.POST
                rn.ley_dominga_cordon = 'ld_cordon' in request.POST
                rn.ley_dominga_no_quiso = 'ld_no_quiso' in request.POST
                
                # Defaults mínimos para validar modelo (ya que usuario no ingresa esto)
                rn.peso_gramos = request.POST.get('peso') or 500
                rn.talla_centimetros = request.POST.get('talla') or 30
                rn.apgar_1_minuto = 0
                rn.apgar_5_minutos = 0
                
            else:
                # RN VIVO - Limpiar Ley Dominga
                rn.ley_dominga_brazalete = False
                rn.ley_dominga_huellas = False
                rn.ley_dominga_pelo = False
                rn.ley_dominga_cordon = False
                rn.ley_dominga_no_quiso = False
            
                rn.peso_gramos = request.POST.get('peso') or 3000
                rn.talla_centimetros = request.POST.get('talla') or 50
                rn.apgar_1_minuto = request.POST.get('apgar1') or 0 

            # Nuevos Campos ID
            rn.nombre_rn_temporal = request.POST.get('nombre_temporal', '')
            rn.pulsera_identificacion = 'pulsera_id' in request.POST
            
            # Correction: Handle empty strings for decimals
            pc = request.POST.get('pc')
            rn.perimetro_cefalico = pc if pc else None
            
            pt = request.POST.get('pt')
            rn.perimetro_torax = pt if pt else None
            
            # 2. Apgar (Simplified)
            # Only if checkApgar was visible/checked ideally, but saving value if present is fine
            rn.apgar_1_minuto = request.POST.get('apgar1') or 0
            
            # 3. Cordón
            rn.ligadura_tardia_cordon = 'ligadura_tardia' in request.POST
            rn.tiempo_ligadura_minutos = request.POST.get('tiempo_ligadura') or 0
            rn.numero_vasos_cordon = request.POST.get('vasos_cordon') or 3
            
            # 4. Apego
            rn.apego_piel_con_piel = 'apego_piel' in request.POST
            rn.apego_canguro = 'apego_canguro' in request.POST
            rn.duracion_apego_canguro_minutos = request.POST.get('duracion_canguro') or 0
            rn.acompanamiento_madre = 'acomp_madre' in request.POST
            rn.acompanamiento_acompanante = 'acomp_ext' in request.POST
            
            # 5. Evaluaciones
            rn.examen_fisico_completo = 'examen_fisico' in request.POST
            rn.screening_metabolico = 'screening' in request.POST
            rn.vacuna_hepatitis_b = 'vac_hep_b' in request.POST
            rn.vitamina_k = 'vit_k' in request.POST
            rn.profilaxis_oftalmologica = 'prof_oftal' in request.POST
            
            # 6. Alimentación
            rn.lactancia_iniciada = 'lactancia_iniciada' in request.POST
            rn.tiempo_inicio_lactancia_minutos = request.POST.get('tiempo_lactancia') or 0
            rn.alimentacion_con_formula = 'formula' in request.POST
            rn.razon_formula = request.POST.get('razon_formula', '')
            
            # 7. Complicaciones
            rn.dificultad_respiratoria = 'dif_resp' in request.POST
            rn.hipoglucemia = 'hipoglucemia' in request.POST
            rn.hipotermia = 'hipotermia' in request.POST
            rn.ictericia = 'ictericia' in request.POST
            rn.traumatismo_obstetrico = 'trauma_obs' in request.POST
            rn.otras_complicaciones = request.POST.get('otras_complicaciones', '')
            
            rn.requiere_hospitalizacion = 'hospitalizacion' in request.POST
            motivo_id = request.POST.get('motivo_hosp')
            if motivo_id:
                rn.motivo_hospitalizacion_id = motivo_id
            else:
                 rn.motivo_hospitalizacion = None
            
            # 8. Staff Responsable
            matrona_id = request.POST.get('matrona_rn')
            tens_id = request.POST.get('tens_rn')
            
            if matrona_id:
                u = User.objects.get(pk=matrona_id)
                rn.matrona_responsable = u.get_full_name()
            
            if tens_id:
                u = User.objects.get(pk=tens_id)
                rn.tens_responsable = u.get_full_name()
            
            rn.save()
            
            if rn.es_mortinato:
                messages.success(request, 'Ley Dominga registrada. Procediendo al Cierre del Parto.')
                return redirect('matrona:cierre_parto', ficha_parto_id=ficha_parto.id)
            else:
                messages.success(request, 'Ficha Recién Nacido guardada correctamente.')
                # Return to list/detail view or stay? Usually back to sala_parto to see updated list
                # Or detalle_registro_parto to see the summary?
                # User complaint was "si no se marco ... no deberia redirijir aqui [cierre]".
                # So I redirect to sala_parto (main workspace)
                return redirect('matrona:sala_parto', ficha_parto_id=ficha_parto.id)

            
        except Exception as e:
            messages.error(request, f'Error al guardar: {str(e)}')
            
    # DETECT NEW (via query param)
    is_new = request.GET.get('new') == '1'

    return render(request, 'Matrona/ficha_rn.html', {
        'rn': rn,
        'ficha_parto': ficha_parto,
        'sexos': sexos,
        'complicaciones_rn': complicaciones_rn,
        'motivos_hospitalizacion': motivos_hospitalizacion,
        'matronas_staff': matronas_staff,
        'tens_staff': tens_staff,
        'is_new': is_new,
    })

@login_required
def detalle_rn_view(request, rn_id):
    """
    Vista de solo lectura para ver el detalle completo de un recién nacido
    """
    rn = get_object_or_404(RegistroRecienNacido, pk=rn_id)
    
    return render(request, 'Matrona/detalle_rn.html', {
        'rn': rn,
    })
    
@login_required
def historial_partos_view(request):
    """
    Vista de historial de partos completados
    Muestra todos los registros de parto finalizados
    """
    from django.db.models import Q, Count
    
    # Obtener todos los registros de parto con información relacionada
    registros = RegistroParto.objects.select_related(
        'ficha_ingreso_parto__ficha_obstetrica__paciente__persona',
        'tipo_parto',
        'clasificacion_robson'
    ).prefetch_related(
        'recien_nacidos'
    ).order_by('-fecha_creacion')
    
    # Filtros opcionales
    busqueda = request.GET.get('q', '')
    if busqueda:
        registros = registros.filter(
            Q(ficha_ingreso_parto__ficha_obstetrica__paciente__persona__Nombre__icontains=busqueda) |
            Q(ficha_ingreso_parto__ficha_obstetrica__paciente__persona__Apellido_Paterno__icontains=busqueda) |
            Q(ficha_ingreso_parto__ficha_obstetrica__paciente__persona__Rut__icontains=busqueda)
        )
    
    return render(request, 'Matrona/historial_partos.html', {
        'registros': registros,
        'busqueda': busqueda,
    })
    
# ============================================
# LEGACY CODE - STAFF FILTERING (DUPLICATED)
# ============================================
    
    # Staff Filtering using PersonalAsignadoParto
    assigned_staff = PersonalAsignadoParto.objects.filter(
        ficha=ficha_parto.ficha_obstetrica, 
        activo=True
    )
    matrona_ids = assigned_staff.filter(rol='MATRONA').values_list('usuario_id', flat=True)
    tens_ids = assigned_staff.filter(rol__in=['TENS', 'Tens']).values_list('usuario_id', flat=True) 

    # If no staff assigned (fallback or empty?) -> User requested "Solamente esos deben salir". 
    # Logic: If ids exist, filter by them. If not, maybe show all (for safety)? 
    # User was strict: "Solamente esos deben salir". I will respect that.
    
    matronas_staff = User.objects.filter(id__in=matrona_ids) if matrona_ids.exists() else User.objects.none()
    tens_staff = User.objects.filter(id__in=tens_ids) if tens_ids.exists() else User.objects.none()

    # Time Logic for Timer
    start_timestamp_ms = None
    if ficha_parto.fecha_ingreso and ficha_parto.hora_ingreso:
        from datetime import datetime as dt_class # Avoid conflict matching
        full_dt = dt_class.combine(ficha_parto.fecha_ingreso, ficha_parto.hora_ingreso)
        start_timestamp_ms = int(full_dt.timestamp() * 1000)

    context = {
        'ficha_parto': ficha_parto,
        'paciente': ficha_parto.ficha_obstetrica.paciente,
        'registro_parto': registro_parto,
        'recien_nacidos': recien_nacidos,
        'start_timestamp_ms': start_timestamp_ms,
        # Contexto Catálogos Parto
        'tipos_parto': tipos_parto,
        'posiciones': posiciones,
        'robsons': robsons,
        'perines': perines,
        'causas_cesarea': causas_cesarea,
        'motivos_no_acompanado': motivos_no_acompanado,
        'personas_acompanante': personas_acompanante,
        'metodos_no_farm': metodos_no_farm,
        'tipos_esterilizacion': tipos_esterilizacion,
        # Nuevos Catalogos Contexto
        'regimenes_parto': regimenes_parto,
        'tipos_rotura': tipos_rotura,
        # Contexto Catálogos RN
        'sexos': sexos,
        'complicaciones_rn': complicaciones_rn,
        'motivos_hospitalizacion': motivos_hospitalizacion, # NEW
        # Staff
        'matronas_staff': matronas_staff,
        'tens_staff': tens_staff,
    }
    return render(request, 'Matrona/sala_parto.html', context)


# ============================================
# API: GUARDAR REGISTROS
# ============================================

@require_POST
@login_required
def guardar_registro_parto(request, ficha_parto_id):
    ficha_parto = get_object_or_404(FichaParto, pk=ficha_parto_id)
    
    # 1. Intentar obtener instancia existente por relación
    instance = None
    try:
        instance = ficha_parto.registro_parto
    except Exception:
        instance = None
        
    # 2. Si no se encuentra por relación, buscar por Numero de Registro (para evitar error de unique)
    if not instance:
        numero_registro = request.POST.get('numero_registro')
        if numero_registro:
            instance = RegistroParto.objects.filter(numero_registro=numero_registro).first()

    form = RegistroPartoForm(request.POST, instance=instance)
    
    if form.is_valid():
        try:
            with transaction.atomic():
                registro = form.save(commit=False)
                
                # CORRECCIÓN: Asignar al campo OneToOne correcto
                registro.ficha_ingreso_parto = ficha_parto
                
                # Manejo de Nombres de Staff basados en ID
                prof_id = form.cleaned_data.get('profesional_responsable_id')
                tens_id = form.cleaned_data.get('tens_responsable_id')
                
                if prof_id:
                    try:
                        u = User.objects.get(pk=prof_id)
                        # CORRECCIÓN: Usar los campos correctos del modelo
                        registro.profesional_responsable_nombre = u.first_name or u.username
                        registro.profesional_responsable_apellido = u.last_name or ""
                    except User.DoesNotExist:
                        pass
                
                if tens_id:
                    try:
                        u = User.objects.get(pk=tens_id)
                        registro.tens_responsable_nombre = u.first_name or u.username
                        registro.tens_responsable_apellido = u.last_name or ""
                    except User.DoesNotExist:
                        pass
                
                registro.save()
                
                # GUARDAR NOMBRE ACOMPAÑANTE EN FICHA OBSTÉTRICA
                nombre_acompanante = request.POST.get('nombre_acompanante', '').strip()
                if nombre_acompanante:
                    ficha_obstetrica = ficha_parto.ficha_obstetrica
                    ficha_obstetrica.nombre_acompanante = nombre_acompanante
                    ficha_obstetrica.save(update_fields=['nombre_acompanante'])
                
                # URL de redirección al detalle
                redirect_url = reverse('matrona:detalle_registro_parto', args=[ficha_parto.id])
                return JsonResponse({
                    'success': True, 
                    'message': 'Registro de Parto guardado correctamente.',
                    'redirect_url': redirect_url
                })
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al guardar: {str(e)}'}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Error de validación', 'errors': form.errors}, status=400)


@login_required
def detalle_registro_parto(request, ficha_parto_id):
    """
    Vista de sólo lectura con el detalle del parto registrado
    """
    ficha_parto = get_object_or_404(FichaParto, pk=ficha_parto_id)
    
    # 1. Registro de Parto
    try:
        registro = ficha_parto.registro_parto
    except Exception:
        # Si no existe, redirigir a sala de parto para crear
        return redirect('matrona:sala_parto', ficha_parto_id=ficha_parto.id)

    # 2. Recién Nacidos
    recien_nacidos = registro.recien_nacidos.all().order_by('id')
    
    context = {
        'titulo': f'Detalle Parto - {registro.numero_registro}',
        'ficha_parto': ficha_parto,
        'registro': registro,
        'recien_nacidos': recien_nacidos,
        'ficha_obstetrica': registro.ficha_obstetrica,
        'paciente': registro.ficha_obstetrica.paciente,
        'staff_asignado': registro.ficha_obstetrica.personal_asignado.all().annotate(
            rol_order=Case(
                When(rol='MEDICO', then=Value(1)),
                When(rol='MATRONA', then=Value(2)),
                When(rol='TENS', then=Value(3)),
                default=Value(4),
                output_field=IntegerField(),
            )
        ).order_by('rol_order', 'usuario__first_name')
    }
    
    return render(request, 'Matrona/detalle_registro_parto.html', context)




@require_POST
@login_required
def guardar_registro_rn(request, ficha_parto_id):
    ficha_parto = get_object_or_404(FichaParto, pk=ficha_parto_id)
    
    # Ensure RegistroParto exists
    try:
        registro_parto = ficha_parto.registro_parto
    except Exception:
        return JsonResponse({'success': False, 'message': 'Debe guardar el parto primero.'}, status=400)

    form = RegistroRecienNacidoForm(request.POST) # Always create new RN for now
    
    if form.is_valid():
        try:
            with transaction.atomic():
                rn = form.save(commit=False)
                rn.parto = registro_parto
                
                # Handle Staff
                matrona_id = form.cleaned_data.get('matrona_responsable_id')
                tens_id = form.cleaned_data.get('tens_responsable_id')
                
                if matrona_id:
                    u = User.objects.get(pk=matrona_id)
                    rn.matrona_responsable = f"{u.first_name} {u.last_name}"
                    
                if tens_id:
                    u = User.objects.get(pk=tens_id)
                    rn.tens_responsable = f"{u.first_name} {u.last_name}"

                rn.save()
                form.save_m2m() # Save complications
                
                return JsonResponse({'success': True, 'message': 'Recién Nacido registrado correctamente.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al guardar RN: {str(e)}'}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Error de validación RN', 'errors': form.errors}, status=400)
# ============================================
# API ADMINISTRACIÓN MEDICAMENTOS
# ============================================

@login_required
def obtener_administraciones(request, medicamento_id):
    """
    API para obtener el historial de administraciones de un medicamento
    URL: /matrona/api/medicamento/<medicamento_id>/administraciones/
    """
    med = get_object_or_404(MedicamentoFicha, id=medicamento_id)
    adms = med.administraciones.all().order_by('-fecha_hora_administracion')
    
    data = []
    for adm in adms:
        data.append({
            'id': adm.id,
            'fecha': adm.fecha_hora_administracion.strftime('%d/%m/%Y %H:%M'),
            'dosis': adm.dosis_administrada,
            'responsable': f"{adm.tens.first_name} {adm.tens.last_name}" if adm.tens else "Desconocido",
            'observaciones': adm.observaciones
        })
        
    return JsonResponse({'administraciones': data})

@login_required
@require_POST
def registrar_administracion(request, medicamento_id):
    """
    API para registrar una administración
    URL: /matrona/api/medicamento/<medicamento_id>/registrar_administracion/
    """
    med = get_object_or_404(MedicamentoFicha, id=medicamento_id)
    
    try:
        data = json.loads(request.body)
        
        fecha_str = data.get('fecha') # "2025-12-14T15:30"
        # Parse datetime
        # Input default is ISO like "2025-12-14T15:30"
        fecha_dt = timezone.datetime.fromisoformat(fecha_str)
        if timezone.is_naive(fecha_dt):
            fecha_dt = timezone.make_aware(fecha_dt)
            
        AdministracionMedicamento.objects.create(
            medicamento_ficha=med,
            tens=request.user, # Asumiendo que quien lo registra es quien lo administra por ahora
            fecha_hora_administracion=fecha_dt,
            dosis_administrada=data.get('dosis'),
            se_realizo_lavado=data.get('lavado', False),
            observaciones=data.get('observaciones', ''),
            administrado_exitosamente=True
        )
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
@login_required
def resumen_final_parto_view(request, ficha_parto_id):
    """
    Vista de resumen final post-cierre.
    Muestra detalles de la madre y RNs en pestañas.
    """
    ficha_parto = get_object_or_404(FichaParto, pk=ficha_parto_id)
    
    # Obtener Registro Parto
    try:
        registro = RegistroParto.objects.get(ficha_ingreso_parto=ficha_parto)
    except RegistroParto.DoesNotExist:
        messages.error(request, 'No se encontró el registro de parto asociado.')
        return redirect('matrona:menu_matrona')
        
    # Obtener Recién Nacidos
    recien_nacidos = RegistroRecienNacido.objects.filter(registro_parto=registro)
    
    return render(request, 'Matrona/resumen_final_parto.html', {
        'ficha_parto': ficha_parto,
        'registro': registro,
        'recien_nacidos': recien_nacidos,
        'paciente': ficha_parto.ficha_obstetrica.paciente,
        'staff_asignado': ficha_parto.ficha_obstetrica.personal_asignado.all().annotate(
            rol_order=Case(
                When(rol='MEDICO', then=Value(1)),
                When(rol='MATRONA', then=Value(2)),
                When(rol='TENS', then=Value(3)),
                default=Value(4),
                output_field=IntegerField(),
            )
        ).order_by('rol_order', 'usuario__first_name')
    })


@login_required
@decrypt_url_params('ficha_pk')
def equipo_confirmado_partial(request, ficha_pk):
    """
    Vista parcial para actualizar la lista de equipo confirmado (polling)
    """
    from ingresoPartoApp.models import FichaParto
    from gestionProcesosApp.models import AsignacionPersonal
    from django.shortcuts import get_object_or_404
    from django.http import HttpResponse
    from django.db.models import IntegerField
    
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk)
    
    # Obtener Ficha de Parto (debería existir)
    ficha_parto = FichaParto.objects.filter(ficha_obstetrica=ficha).first()
    if not ficha_parto:
        return HttpResponse("") # No renderizar nada si no existe
        
    # Calcular Requerimientos (Duplicado de la vista principal por seguridad)
    cantidad_bebes = ficha_parto.ficha_obstetrica.cantidad_bebes
    if cantidad_bebes < 1: cantidad_bebes = 1
    
    medicos_req = cantidad_bebes * 1
    matronas_req = cantidad_bebes * 2
    tens_req = cantidad_bebes * 3
    
    # Obtener Asignaciones Aceptadas
    asignaciones = AsignacionPersonal.objects.filter(proceso=ficha_parto)
    asignados_aceptados = asignaciones.filter(estado_respuesta='ACEPTADA').order_by('-timestamp_confirmacion')
    
    # Calcular Counts
    medicos_aceptados = asignados_aceptados.filter(personal__rol='MEDICO').count()
    matronas_aceptadas = asignados_aceptados.filter(personal__rol='MATRONA').count()
    tens_aceptados = asignados_aceptados.filter(personal__rol='TENS').count()
    
    # Calcular Slots Pendientes
    slots_pendientes = []
    if medicos_aceptados < medicos_req:
        slots_pendientes.append({'rol': 'Médico', 'cantidad': medicos_req - medicos_aceptados})
    if matronas_aceptadas < matronas_req:
        slots_pendientes.append({'rol': 'Matrona', 'cantidad': matronas_req - matronas_aceptadas})
    if tens_aceptados < tens_req:
        slots_pendientes.append({'rol': 'TENS', 'cantidad': tens_req - tens_aceptados})
        
    context = {
        'asignados_aceptados': asignados_aceptados,
        'slots_pendientes': slots_pendientes
    }
    
    return render(request, 'Matrona/partials/equipo_confirmado_list.html', context)


@login_required
@require_POST
def debug_rellenar_equipo(request, ficha_parto_id):
    """
    API DEBUG: Rellena automáticamente el equipo con usuarios disponibles.
    Solo para TEST.
    """
    from ingresoPartoApp.models import FichaParto
    from gestionProcesosApp.models import PersonalTurno, AsignacionPersonal
    from django.shortcuts import get_object_or_404
    from django.utils import timezone
    from django.http import JsonResponse
    
    ficha_parto = get_object_or_404(FichaParto, pk=ficha_parto_id)
    
    # Requisitos
    reqs = {
        'MEDICO': ficha_parto.ficha_obstetrica.cantidad_bebes * 1,
        'MATRONA': ficha_parto.ficha_obstetrica.cantidad_bebes * 2,
        'TENS': ficha_parto.ficha_obstetrica.cantidad_bebes * 3,
    }
    
    asignados_count = 0
    now = timezone.now()
    
    for rol, cantidad_necesaria in reqs.items():
        # Cuantos tenemos ya aceptados/asignados
        actuales = AsignacionPersonal.objects.filter(proceso=ficha_parto, personal__rol=rol, estado_respuesta='ACEPTADA').count()
        faltan = cantidad_necesaria - actuales
        
        if faltan > 0:
            # Buscar disponibles
            candidatos = PersonalTurno.objects.filter(
                rol=rol, 
                estado='DISPONIBLE',
                fecha_fin_turno__gte=now
            ).exclude(
                id__in=AsignacionPersonal.objects.filter(proceso=ficha_parto).values('personal_id')
            )[:faltan]
            
            for personal in candidatos:
                AsignacionPersonal.objects.create(
                    proceso=ficha_parto,
                    personal=personal,
                    rol_en_proceso=rol,
                    estado_respuesta='ACEPTADA',
                    confirmo_asistencia=True,
                    timestamp_notificacion=now,
                    timestamp_confirmacion=now
                )
                asignados_count += 1
                
    return JsonResponse({'success': True, 'asignados': asignados_count})

# ============================================
# VISTA: CERRAR FICHA DEFINITIVAMENTE
# ============================================

@login_required
@require_POST
@decrypt_url_params('ficha_pk')
def cerrar_ficha_definitivamente(request, ficha_pk):
    """
    Cerrar definitivamente una ficha obstétrica
    Solo disponible después de completar el parto
    URL: /services/case/<ficha_pk>/close/
    """
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk)
    
    # Validar que el parto esté completado
    if not ficha.parto_completado:
        messages.error(request, 'No se puede cerrar la ficha sin completar el parto')
        return redirect('matrona:detalle_ficha', ficha_pk=encrypt_id(ficha.pk))
    
    # Validar que no esté ya cerrada
    if ficha.ficha_cerrada:
        messages.warning(request, 'Esta ficha ya está cerrada')
        return redirect('matrona:detalle_ficha', ficha_pk=encrypt_id(ficha.pk))
    
    # Cerrar ficha
    ficha.ficha_cerrada = True
    ficha.activa = False
    ficha.fecha_cierre = timezone.now()
    ficha.usuario_cierre = request.user
    ficha.save()
    
    messages.success(request, 'Ficha obstétrica cerrada exitosamente. La ficha ahora está en modo solo lectura.')
    return redirect('matrona:historial_partos')


@login_required
@require_POST
def reenviar_pin(request, ficha_parto_id):
    """
    Reenvía el PIN al equipo médico (Telegram).
    """
    from ingresoPartoApp.models import FichaParto
    from gestionProcesosApp.pin_utils import enviar_pin_a_medicos
    
    ficha_parto = get_object_or_404(FichaParto, pk=ficha_parto_id)
    
    if not ficha_parto.pin_inicio_parto:
        return JsonResponse({'success': False, 'error': 'No hay PIN generado aún.'})

    try:
        enviar_pin_a_medicos(ficha_parto, ficha_parto.pin_inicio_parto)
        return JsonResponse({'success': True, 'message': 'PIN reenviado a los médicos.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
