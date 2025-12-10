"""
matronaApp/views.py
Vistas para gestionar Fichas Obstétricas
ACTUALIZADO: Cálculo correcto de edad
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import date

from gestionApp.models import Paciente, Persona
from .models import FichaObstetrica, MedicamentoFicha
from .forms.ficha_obstetrica_form import FichaObstetricaForm, MedicamentoFichaForm


# ============================================
# FUNCIÓN HELPER: Calcular Edad
# ============================================

def calcular_edad(fecha_nacimiento):
    """Calcula la edad basada en la fecha de nacimiento"""
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year
    # Restar 1 si el cumpleaños aún no ha ocurrido este año
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return edad


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
    
    # ✅ CALCULAR EDAD CORRECTAMENTE
    edad = calcular_edad(persona.Fecha_nacimiento)
    
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
        'edad': edad,
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
    
    # ✅ CALCULAR EDAD CORRECTAMENTE
    edad = calcular_edad(persona.Fecha_nacimiento)
    
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
        'edad': edad,
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
    
    # ✅ CALCULAR EDAD CORRECTAMENTE
    edad = calcular_edad(persona.Fecha_nacimiento)
    
    context = {
        'ficha': ficha,
        'paciente': paciente,
        'persona': persona,
        'edad': edad,
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
    return render(request, 'Matrona/lista_fichas.html', context)


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
    Menu principal de matrona (Dashboard)
    URL: /matrona/
    """
    # Estadísticas
    total_fichas = FichaObstetrica.objects.filter(activa=True).count()
    fichas_recientes = FichaObstetrica.objects.filter(activa=True).order_by('-fecha_creacion')[:5]
    
    # Datos para el dashboard
    total_ingresos = 0  # Se obtendría de ingresos de paciente si existe
    total_medicamentos_asignados = MedicamentoFicha.objects.filter(activo=True).count()
    
    # Permisos específicos de matrona
    puede_ingresar_paciente = True
    puede_asignar_medicamentos = True
    puede_buscar_paciente = True
    puede_editar_ficha = True  # Matrona puede editar fichas
    puede_iniciar_parto = False  # Solo médico
    
    context = {
        'titulo': 'Dashboard Matrona',
        'total_fichas': total_fichas,
        'fichas_recientes': fichas_recientes,
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
# CREAR FICHA - A PARTIR DE PERSONA
# ============================================

@login_required
def crear_ficha_obstetrica_persona(request, persona_pk):
    """
    Crear nueva ficha obstétrica a partir de una Persona
    URL: /matrona/ficha/crear-persona/<persona_pk>/
    
    Si la persona no tiene un paciente creado, lo crea automáticamente
    """
    
    # Obtener la persona
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
    
    # ✅ CALCULAR EDAD CORRECTAMENTE
    edad = calcular_edad(persona.Fecha_nacimiento)
    
    if request.method == 'POST':
        form = FichaObstetricaForm(request.POST)
        if form.is_valid():
            ficha = form.save(commit=False)
            ficha.paciente = paciente
            ficha.numero_ficha = f"FO-{FichaObstetrica.objects.count() + 1:06d}"
            
            try:
                ficha.save()
                
                messages.success(
                    request,
                    f'✅ Ficha Obstétrica {ficha.numero_ficha} creada exitosamente'
                )
                return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
            except Exception as e:
                messages.error(request, f'❌ Error al crear la ficha: {str(e)}')
        else:
            # Mostrar errores específicos
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'❌ {field}: {error}')
    else:
        form = FichaObstetricaForm()
    
    context = {
        'form': form,
        'paciente': paciente,
        'persona': persona,
        'edad': edad,
        'titulo': 'Crear Ficha Obstétrica',
        'accion': 'crear'
    }
    return render(request, 'Matrona/crear_ficha_obstetrica.html', context)


# ============================================
# SELECCIONAR PERSONA - PARA CREAR FICHA
# ============================================

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
    return render(request, 'Matrona/seleccionar_persona_ficha.html', context)