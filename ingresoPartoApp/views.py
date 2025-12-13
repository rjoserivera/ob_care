"""
ingresoPartoApp/views.py
Vistas MEJORADAS para ingresoPartoApp
Con soporte para catálogos y bebés esperados
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db import transaction
from django.db.models import Q

from matronaApp.models import FichaObstetrica
from .models import (
    FichaParto,
    BebeEsperado,
    CatalogoPosicionFetal,
    CatalogoSalaAsignada,
)
from .forms.forms import FichaPartoForm, BebeEsperadoForm



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
        'ficha_obstetrica__paciente__persona',
        'sala_asignada'
    ).order_by('-fecha_creacion')[:5]
    
    # Salas disponibles
    salas_disponibles = CatalogoSalaAsignada.objects.filter(activo=True).count()
    
    context = {
        'titulo': 'Ingreso a Parto',
        'total_fichas': total_fichas,
        'fichas_hoy': fichas_hoy,
        'fichas_recientes': fichas_recientes,
        'salas_disponibles': salas_disponibles,
    }
    
    return render(request, 'IngresoParto/menu_ingreso_parto.html', context)


# ============================================
# SALA DE ESPERA (ANTES DE CREAR FICHA)
# ============================================

@login_required
def sala_espera_parto(request, ficha_obstetrica_pk):
    """
    Sala de espera antes de crear ficha de parto
    URL: /ingreso-parto/sala-espera/<ficha_obstetrica_pk>/
    """
    ficha_obstetrica = get_object_or_404(
        FichaObstetrica.objects.select_related('paciente__persona'),
        pk=ficha_obstetrica_pk
    )
    
    # Verificar si ya tiene ficha de parto
    if hasattr(ficha_obstetrica, 'ficha_parto'):
        messages.info(request, 'Esta paciente ya tiene una ficha de parto.')
        return redirect('ingreso_parto:detalle_ficha', ficha_parto_pk=ficha_obstetrica.ficha_parto.pk)
    
    # Verificar condiciones (urgencia, patologías)
    urgente = ficha_obstetrica.tipo_ingreso in ['URGENCIA', 'DERIVACION']
    
    # Obtener salas disponibles
    salas = CatalogoSalaAsignada.objects.filter(activo=True)
    
    context = {
        'ficha_obstetrica': ficha_obstetrica,
        'titulo': 'Sala de Espera - Proceso de Parto',
        'urgente': urgente,
        'salas': salas,
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
    
    # Obtener sala del GET si viene
    sala_id = request.GET.get('sala')
    
    if request.method == 'POST':
        form = FichaPartoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                ficha_parto = form.save(commit=False)
                ficha_parto.ficha_obstetrica = ficha_obstetrica
                ficha_parto.creado_por = request.user
                
                # Generar número de ficha automático
                ultimo = FichaParto.objects.order_by('-id').first()
                siguiente_num = (ultimo.id + 1) if ultimo else 1
                ficha_parto.numero_ficha_parto = f"FP-{siguiente_num:06d}"
                
                ficha_parto.save()
                
                # Procesar bebés esperados
                procesar_bebes_esperados(request, ficha_parto, ficha_obstetrica.cantidad_bebes)
                
                messages.success(request, f'✅ Ficha de parto {ficha_parto.numero_ficha_parto} creada exitosamente.')
                return redirect('ingreso_parto:detalle_ficha', ficha_parto_pk=ficha_parto.pk)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        # Valores iniciales
        initial = {
            'fecha_ingreso': timezone.now().date(),
            'hora_ingreso': timezone.now().time(),
            'edad_gestacional_semanas': ficha_obstetrica.edad_gestacional_semanas,
            'edad_gestacional_dias': ficha_obstetrica.edad_gestacional_dias,
        }
        if sala_id:
            initial['sala_asignada'] = sala_id
            
        form = FichaPartoForm(initial=initial)
    
    # Datos para el template
    posiciones_fetales = CatalogoPosicionFetal.objects.filter(activo=True).order_by('orden')
    
    # Rango de bebés
    cantidad_bebes = ficha_obstetrica.cantidad_bebes or 1
    bebes_range = range(1, cantidad_bebes + 1)
    
    context = {
        'form': form,
        'ficha_obstetrica': ficha_obstetrica,
        'titulo': 'Crear Ficha de Ingreso a Parto',
        'es_edicion': False,
        'posiciones_fetales': posiciones_fetales,
        'bebes_range': bebes_range,
    }
    
    return render(request, 'IngresoParto/form_ingreso_parto.html', context)


# ============================================
# FICHA PARTO - EDITAR
# ============================================

@login_required
def editar_ficha_parto(request, ficha_parto_pk):
    """
    Editar ficha de ingreso a parto
    URL: /ingreso-parto/ficha/<ficha_parto_pk>/editar/
    """
    ficha = get_object_or_404(
        FichaParto.objects.select_related('ficha_obstetrica__paciente__persona'),
        pk=ficha_parto_pk
    )
    ficha_obstetrica = ficha.ficha_obstetrica
    
    if request.method == 'POST':
        form = FichaPartoForm(request.POST, instance=ficha)
        if form.is_valid():
            with transaction.atomic():
                ficha_parto = form.save()
                
                # Actualizar bebés esperados
                procesar_bebes_esperados(request, ficha_parto, ficha_obstetrica.cantidad_bebes)
                
                messages.success(request, f'✅ Ficha {ficha_parto.numero_ficha_parto} actualizada.')
                return redirect('ingreso_parto:detalle_ficha', ficha_parto_pk=ficha_parto.pk)
    else:
        form = FichaPartoForm(instance=ficha)
    
    # Datos para el template
    posiciones_fetales = CatalogoPosicionFetal.objects.filter(activo=True).order_by('orden')
    bebes_existentes = ficha.bebes_esperados.all().order_by('numero_bebe')
    
    cantidad_bebes = ficha_obstetrica.cantidad_bebes or 1
    bebes_range = range(1, cantidad_bebes + 1)
    
    context = {
        'form': form,
        'ficha_obstetrica': ficha_obstetrica,
        'ficha_parto': ficha,
        'titulo': f'Editar Ficha {ficha.numero_ficha_parto}',
        'es_edicion': True,
        'posiciones_fetales': posiciones_fetales,
        'bebes_range': bebes_range,
        'bebes_existentes': bebes_existentes,
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
        FichaParto.objects.select_related(
            'ficha_obstetrica__paciente__persona',
            'sala_asignada',
            'posicion_fetal',
            'altura_presentacion',
            'estado_cervical',
            'estado_fetal',
            'caracteristicas_liquido',
            'resultado_ctg',
        ).prefetch_related('bebes_esperados'),
        pk=ficha_parto_pk
    )
    
    bebes = ficha.bebes_esperados.all().order_by('numero_bebe')
    
    context = {
        'ficha': ficha,
        'ficha_obstetrica': ficha.ficha_obstetrica,
        'bebes': bebes,
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
        'ficha_obstetrica__paciente__persona',
        'sala_asignada'
    ).order_by('-fecha_ingreso', '-hora_ingreso')
    
    # Búsqueda
    search_query = request.GET.get('q', '')
    if search_query:
        fichas = fichas.filter(
            Q(ficha_obstetrica__paciente__persona__Nombre__icontains=search_query) |
            Q(ficha_obstetrica__paciente__persona__Rut__icontains=search_query) |
            Q(numero_ficha_parto__icontains=search_query)
        )
    
    # Filtro por fecha
    fecha = request.GET.get('fecha', '')
    if fecha:
        fichas = fichas.filter(fecha_ingreso=fecha)
    
    # Filtro por sala
    sala = request.GET.get('sala', '')
    if sala:
        fichas = fichas.filter(sala_asignada_id=sala)
    
    # Salas para filtro
    salas = CatalogoSalaAsignada.objects.filter(activo=True)
    
    context = {
        'fichas': fichas,
        'titulo': 'Fichas de Ingreso a Parto',
        'search_query': search_query,
        'fecha_filtro': fecha,
        'sala_filtro': sala,
        'salas': salas,
    }
    
    return render(request, 'IngresoParto/lista_fichas_parto.html', context)


# ============================================
# FUNCIONES AUXILIARES
# ============================================

def procesar_bebes_esperados(request, ficha_parto, cantidad_bebes):
    """
    Procesa la información de bebés esperados desde el POST
    """
    # Eliminar bebés existentes y crear nuevos
    ficha_parto.bebes_esperados.all().delete()
    
    for i in range(1, cantidad_bebes + 1):
        sexo = request.POST.get(f'bebe_{i}_sexo', '')
        peso = request.POST.get(f'bebe_{i}_peso')
        posicion_id = request.POST.get(f'bebe_{i}_posicion')
        fcf = request.POST.get(f'bebe_{i}_fcf')
        obs = request.POST.get(f'bebe_{i}_obs', '')
        
        # Solo crear si hay algún dato
        if sexo or peso or posicion_id or fcf or obs:
            BebeEsperado.objects.create(
                ficha_parto=ficha_parto,
                numero_bebe=i,
                sexo_esperado=sexo if sexo else '',
                peso_estimado=int(peso) if peso else None,
                posicion_fetal_id=int(posicion_id) if posicion_id else None,
                frecuencia_cardiaca=int(fcf) if fcf else None,
                observaciones=obs
            )


# ============================================
# APIs AJAX
# ============================================

@login_required
def api_verificar_sala(request):
    """
    API para verificar disponibilidad de sala
    URL: /ingreso-parto/api/verificar-sala/
    """
    sala_id = request.GET.get('sala_id')
    
    if not sala_id:
        return JsonResponse({'error': 'ID de sala requerido'}, status=400)
    
    try:
        sala = CatalogoSalaAsignada.objects.get(pk=sala_id)
        
        # Contar fichas activas en esta sala hoy
        fichas_en_sala = FichaParto.objects.filter(
            sala_asignada=sala,
            fecha_ingreso=timezone.now().date(),
            activa=True
        ).count()
        
        disponible = fichas_en_sala < sala.capacidad
        
        return JsonResponse({
            'sala': sala.nombre,
            'capacidad': sala.capacidad,
            'ocupacion': fichas_en_sala,
            'disponible': disponible
        })
    except CatalogoSalaAsignada.DoesNotExist:
        return JsonResponse({'error': 'Sala no encontrada'}, status=404)


@login_required
def api_obtener_datos_obstetrica(request, ficha_obstetrica_pk):
    """
    API para obtener datos de la ficha obstétrica
    URL: /ingreso-parto/api/ficha-obstetrica/<pk>/
    """
    try:
        ficha = FichaObstetrica.objects.select_related('paciente__persona').get(pk=ficha_obstetrica_pk)
        
        return JsonResponse({
            'paciente': {
                'nombre': f"{ficha.paciente.persona.Nombre} {ficha.paciente.persona.Apellido_Paterno}",
                'rut': ficha.paciente.persona.Rut,
            },
            'edad_gestacional': {
                'semanas': ficha.edad_gestacional_semanas,
                'dias': ficha.edad_gestacional_dias
            },
            'cantidad_bebes': ficha.cantidad_bebes,
            'tipo_ingreso': ficha.tipo_ingreso,
            'tiene_patologia': ficha.preeclampsia_severa or ficha.eclampsia,
        })
    except FichaObstetrica.DoesNotExist:
        return JsonResponse({'error': 'Ficha no encontrada'}, status=404)