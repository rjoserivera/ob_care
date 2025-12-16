# medicoApp/views.py
"""
Vistas para el módulo de Médico
Gestión del catálogo de patologías obstétricas
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from medicoApp.models import Patologias
from matronaApp.models import FichaObstetrica, MedicamentoFicha, IngresoPaciente


# ============================================
# VISTA PRINCIPAL DEL MÓDULO MÉDICO
# ============================================

from gestionApp.views_dashboards import DashboardMedicoView

# Reemplazamos la vista funcional por la vista basada en clases
menu_medico = DashboardMedicoView.as_view()


# ============================================
# GESTIÓN DE PATOLOGÍAS (SIMPLIFICADA)
# ============================================

def listar_patologias(request):
    """
    Listar todas las patologías con filtros
    El médico solo activa/desactiva las que usará el hospital
    """
    patologias = Patologias.objects.all().order_by('nivel_de_riesgo', 'nombre')
    
    # Filtros
    busqueda = request.GET.get('busqueda', '').strip()
    estado = request.GET.get('estado', '')
    nivel_riesgo = request.GET.get('nivel_riesgo', '')
    
    if busqueda:
        patologias = patologias.filter(
            Q(nombre__icontains=busqueda) |
            Q(codigo_cie_10__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )
    
    if estado:
        patologias = patologias.filter(estado=estado)
    
    if nivel_riesgo:
        patologias = patologias.filter(nivel_de_riesgo=nivel_riesgo)
    
    # Contar cuántas fichas usan cada patología
    patologias = patologias.annotate(
        num_fichas=Count('fichas_con_patologia')
    )
    
    context = {
        'patologias': patologias,
        'busqueda': busqueda,
        'estado': estado,
        'nivel_riesgo': nivel_riesgo,
    }
    
    return render(request, 'Medico/Data/Patologia_listar.html', context)


def detalle_patologia(request, pk):
    """Ver el detalle completo de una patología"""
    patologia = get_object_or_404(Patologias, pk=pk)
    
    # Contar en cuántas fichas se usa
    fichas_usando = patologia.fichas_con_patologia.filter(activa=True).count()
    
    context = {
        'patologia': patologia,
        'fichas_usando': fichas_usando,
    }
    
    return render(request, 'Medico/Data/Patologia_detalle.html', context)


def toggle_patologia(request, pk):
    """
    Activar/Desactivar una patología
    """
    patologia = get_object_or_404(Patologias, pk=pk)
    
    if request.method == 'POST':
        if patologia.estado == 'Activo':
            patologia.estado = 'Inactivo'
            mensaje = f"❌ Patología '{patologia.nombre}' desactivada. Ya no estará disponible para nuevas fichas."
        else:
            patologia.estado = 'Activo'
            mensaje = f"✅ Patología '{patologia.nombre}' activada. Ahora está disponible para asignar a pacientes."
        
        patologia.save()
        messages.success(request, mensaje)
        return redirect('medico:listar_patologias')
    
    return render(request, 'Medico/Formularios/Patologias_toggle.html', {
        'patologia': patologia
    })


# ============================================
# FUNCIONES DEPRECADAS (Ya no se usan)
# ============================================

def registrar_patologia(request):
    """
    DEPRECADA: Ahora las patologías vienen predefinidas
    Redirigir al listado
    """
    messages.info(
        request,
        "ℹ️ Las patologías vienen predefinidas en el sistema. "
        "Solo debe activar las que usará el hospital."
    )
    return redirect('medico:listar_patologias')


def editar_patologia(request, pk):
    """
    DEPRECADA: Ya no se editan patologías, solo se activan/desactivan
    """
    messages.info(
        request,
        "ℹ️ Las patologías tienen información predefinida y no se pueden editar. "
        "Solo puede activarlas o desactivarlas."
    )
    return redirect('medico:detalle_patologia', pk=pk)

# medicoApp/views.py

# ... (código existente de patologías)

# ============================================
# CONSULTA DE HISTORIAL CLÍNICO
# ============================================

def buscar_paciente_medico(request):
    """
    Buscar paciente por RUT o nombre para consultar historial clínico
    Reutiliza la misma lógica de búsqueda de otros módulos
    """
    query = request.GET.get('q', '').strip()
    pacientes = []
    
    if query:
        from gestionApp.models import Paciente
        from django.db.models import Q, Count
        
        pacientes = Paciente.objects.filter(
            Q(activo=True)
        ).filter(
            Q(persona__Rut__icontains=query) |
            Q(persona__Nombre__icontains=query) |
            Q(persona__Apellido_Paterno__icontains=query) |
            Q(persona__Apellido_Materno__icontains=query)
        ).select_related('persona').annotate(
            num_fichas=Count('fichas_obstetricas')
        )
    
    return render(request, 'Medico/Data/buscar_paciente.html', {
        'pacientes': pacientes,
        'query': query
    })


def ver_historial_clinico(request, paciente_pk):
    """
    Ver el historial clínico completo de un paciente
    Muestra todas las fichas obstétricas con sus detalles
    """
    from gestionApp.models import Paciente
    from matronaApp.models import FichaObstetrica
    from django.db.models import Prefetch, Count
    
    paciente = get_object_or_404(
        Paciente.objects.select_related('persona'),
        pk=paciente_pk,
        activo=True
    )
    
    # Obtener todas las fichas con información relacionada
    fichas = FichaObstetrica.objects.filter(
        paciente=paciente
    ).select_related(
        'matrona_responsable__persona'
    ).prefetch_related(
        'patologias',
        'medicamentos'
    ).annotate(
        num_medicamentos=Count('medicamentos', filter=Q(medicamentos__activo=True)),
        num_patologias=Count('patologias')
    ).order_by('-fecha_creacion')
    
    return render(request, 'Medico/Data/historial_clinico.html', {
        'paciente': paciente,
        'fichas': fichas,
        'total_fichas': fichas.count()
    })


# ============================================
# GESTIÓN DE FICHAS OBSTÉTRICAS
# ============================================

def calcular_edad(fecha_nacimiento):
    """Calcula la edad basada en la fecha de nacimiento"""
    from datetime import date
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return edad

def crear_ficha_obstetrica(request, paciente_pk):
    """
    Crear nueva ficha obstétrica - Versión Médico
    """
    from gestionApp.models import Paciente
    from matronaApp.models import FichaObstetrica
    from matronaApp.forms.ficha_obstetrica_form import FichaObstetricaForm
    from datetime import date

    paciente = get_object_or_404(Paciente, pk=paciente_pk, activo=True)
    persona = paciente.persona
    
    edad = calcular_edad(persona.Fecha_nacimiento)
    
    if request.method == 'POST':
        form = FichaObstetricaForm(request.POST)
        if form.is_valid():
            ficha = form.save(commit=False)
            ficha.paciente = paciente
            ficha.numero_ficha = f"FO-{FichaObstetrica.objects.count() + 1:06d}"
            ficha.save()
            messages.success(request, f'✅ Ficha Obstétrica {ficha.numero_ficha} creada exitosamente')
            return redirect('medico:detalle_ficha', ficha_pk=ficha.pk)
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
    return render(request, 'Medico/crear_ficha_obstetrica.html', context)


def crear_ficha_obstetrica_persona(request, persona_pk):
    """
    Crear ficha obstétrica desde persona - Versión Médico
    """
    from gestionApp.models import Persona, Paciente
    from matronaApp.models import FichaObstetrica
    from matronaApp.forms.ficha_obstetrica_form import FichaObstetricaForm
    
    persona = get_object_or_404(Persona, pk=persona_pk)
    
    paciente, created = Paciente.objects.get_or_create(
        persona=persona,
        defaults={'activo': True}
    )
    
    if not paciente.activo:
        paciente.activo = True
        paciente.save()
    
    edad = calcular_edad(persona.Fecha_nacimiento)
    
    if request.method == 'POST':
        form = FichaObstetricaForm(request.POST)
        if form.is_valid():
            ficha = form.save(commit=False)
            ficha.paciente = paciente
            ficha.numero_ficha = f"FO-{FichaObstetrica.objects.count() + 1:06d}"
            try:
                ficha.save()
                messages.success(request, f'✅ Ficha Obstétrica {ficha.numero_ficha} creada exitosamente')
                return redirect('medico:detalle_ficha', ficha_pk=ficha.pk)
            except Exception as e:
                messages.error(request, f'❌ Error al crear la ficha: {str(e)}')
        else:
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
    return render(request, 'Medico/crear_ficha_obstetrica.html', context)


def editar_ficha_obstetrica(request, ficha_pk):
    """Editar ficha obstétrica - Versión Médico"""
    from matronaApp.models import FichaObstetrica
    from matronaApp.forms.ficha_obstetrica_form import FichaObstetricaForm

    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk, activa=True)
    paciente = ficha.paciente
    persona = paciente.persona
    
    edad = calcular_edad(persona.Fecha_nacimiento)
    
    if request.method == 'POST':
        form = FichaObstetricaForm(request.POST, instance=ficha)
        if form.is_valid():
            ficha = form.save()
            messages.success(request, f'✅ Ficha {ficha.numero_ficha} actualizada')
            return redirect('medico:detalle_ficha', ficha_pk=ficha.pk)
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
    return render(request, 'Medico/crear_ficha_obstetrica.html', context)


def detalle_ficha_obstetrica(request, ficha_pk):
    """Ver detalle de ficha obstétrica - Versión Médico"""
    from matronaApp.models import FichaObstetrica

    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk)
    paciente = ficha.paciente
    persona = paciente.persona
    medicamentos = ficha.medicamentos.filter(activo=True)
    
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
    return render(request, 'Medico/detalle_ficha_obstetrica.html', context)


def lista_fichas_obstetrica(request):
    """Listar fichas obstétricas - Versión Médico"""
    from matronaApp.models import FichaObstetrica
    from django.core.paginator import Paginator
    from django.db.models import Q
    
    fichas = FichaObstetrica.objects.filter(activa=True).select_related(
        'paciente__persona',
        'matrona_responsable__persona'
    ).order_by('-fecha_creacion')
    
    busqueda = request.GET.get('q', '').strip()
    if busqueda:
        fichas = fichas.filter(
            Q(paciente__persona__Nombre__icontains=busqueda) |
            Q(paciente__persona__Apellido_Paterno__icontains=busqueda) |
            Q(paciente__persona__Apellido_Materno__icontains=busqueda) |
            Q(paciente__persona__Rut__icontains=busqueda)
        )
    
    paginator = Paginator(fichas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'Medico/lista_fichas.html', {
        'page_obj': page_obj,
        'fichas': page_obj,
        'busqueda': busqueda,
        'titulo': 'Fichas Obstétricas'
    })


def agregar_medicamento(request, ficha_pk):
    """Agregar medicamento - Redirección a Médico"""
    from matronaApp.models import FichaObstetrica
    from matronaApp.forms.ficha_obstetrica_form import MedicamentoFichaForm
    
    ficha = get_object_or_404(FichaObstetrica, pk=ficha_pk, activa=True)
    
    if request.method == 'POST':
        form = MedicamentoFichaForm(request.POST)
        if form.is_valid():
            medicamento = form.save(commit=False)
            medicamento.ficha = ficha
            medicamento.save()
            messages.success(request, f'✅ Medicamento {medicamento.medicamento} agregado')
            return redirect('medico:detalle_ficha', ficha_pk=ficha.pk)
    else:
        form = MedicamentoFichaForm()
    
    # Podríamos necesitar un template propio para esto también, pero por ahora podemos usar el de matrona
    # OJO: Si usamos el de matrona, se verá rosa. Idealmente deberíamos copiarlo.
    # Por ahora, usaré el de matrona pero cambiaré el redirect arriba.
    context = {
        'form': form,
        'ficha': ficha,
        'titulo': 'Agregar Medicamento'
    }
    return render(request, 'Medico/medicamento_form.html', context)


def eliminar_medicamento(request, medicamento_pk):
    """Eliminar medicamento - Redirección a Médico"""
    from matronaApp.models import MedicamentoFicha
    
    medicamento = get_object_or_404(MedicamentoFicha, pk=medicamento_pk)
    ficha = medicamento.ficha
    
    if request.method == 'POST':
        medicamento.delete()
        messages.success(request, f'✅ Medicamento eliminado')
        return redirect('medico:detalle_ficha', ficha_pk=ficha.pk)
    
    context = {
        'medicamento': medicamento,
        'ficha': ficha,
        'titulo': 'Eliminar Medicamento'
    }
    return render(request, 'Medico/medicamento_confirmar_delete.html', context)


def seleccionar_persona_ficha(request):
    """Seleccionar persona - Versión Médico"""
    from gestionApp.models import Persona, Paciente
    from django.core.paginator import Paginator
    from django.db.models import Q
    
    query = request.GET.get('q', '').strip()
    pacientes = Paciente.objects.filter(activo=True).select_related('persona').order_by('persona__Nombre')
    
    if query:
        pacientes = pacientes.filter(
            Q(persona__Nombre__icontains=query) |
            Q(persona__Rut__icontains=query) |
            Q(persona__Apellido_Paterno__icontains=query) |
            Q(persona__Apellido_Materno__icontains=query)
        )
            
    paginator = Paginator(pacientes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'Medico/seleccionar_persona_ficha.html', {
        'page_obj': page_obj,
        'pacientes': page_obj.object_list,
        'query': query,
        'titulo': 'Seleccionar Paciente'
    })