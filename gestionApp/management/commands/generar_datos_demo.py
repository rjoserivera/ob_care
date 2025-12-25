import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import transaction

# Modelos
from gestionApp.models import Persona, Paciente, CatalogoSexo, CatalogoNacionalidad, CatalogoPrevision
from matronaApp.models import (
    FichaObstetrica, MedicamentoFicha, CatalogoMedicamento, 
    CatalogoTipoPaciente, CatalogoARO, CatalogoViaAdministracion
)
from partosApp.models import (
    RegistroParto, CatalogoTipoParto, CatalogoClasificacionRobson,
    CatalogoPosicionParto, CatalogoEstadoPerine, CatalogoCausaCesarea
)
from recienNacidoApp.models import RegistroRecienNacido, CatalogoSexoRN, CatalogoComplicacionesRN
from ingresoPartoApp.models import (
    FichaParto, CatalogoEstadoCervical, CatalogoPosicionFetal, 
    CatalogoAlturaPresentacion, CatalogoEstadoFetal, CatalogoSalaAsignada
)
from gestionApp.models import CatalogoPuebloOriginario
from matronaApp.models import CatalogoConsultorioOrigen

class Command(BaseCommand):
    help = 'Genera datos de demostración completos para el año 2025'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cantidad',
            type=int,
            default=100,
            help='Cantidad de fichas a generar (default: 100)'
        )

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        
        self.stdout.write('=' * 70)
        self.stdout.write(self.style.SUCCESS(f'GENERANDO {cantidad} FICHAS COMPLETAS - ANO 2025'))
        self.stdout.write('=' * 70 + '\n')

        # 1. Preparar datos base (Catálogos y Usuarios)
        if not self.preparar_datos_base():
            return

        fichas_creadas = 0
        partos_creados = 0
        rn_creados = 0
        errores = 0

        for i in range(cantidad):
            try:
                with transaction.atomic():
                    self.stdout.write(f'\n--- Procesando registro {i + 1}/{cantidad} ---')
                
                # Generar fecha base (fecha de ingreso/creación)
                fecha_base = self.generar_fecha_2025()
                
                # 2. Crear Paciente
                paciente = self.crear_paciente(i, fecha_base)
                self.stdout.write(f'  [OK] Paciente: {paciente.persona.Nombre} {paciente.persona.Apellido_Paterno}')
                
                # 3. Crear Ficha Obstétrica
                ficha = self.crear_ficha_obstetrica(paciente, fecha_base)
                fichas_creadas += 1
                self.stdout.write(f'  [OK] Ficha Obstétrica creada')
                
                # 80% Probabilidad de tener parto registrado
                if random.random() < 0.8:
                    # 4. Crear Ficha de Ingreso a Parto
                    ficha_parto = self.crear_ficha_parto(ficha, fecha_base)
                    self.stdout.write(f'  [OK] Ficha de Ingreso a Parto creada')
                    
                    # 5. Crear Registro de Parto
                    fecha_parto_real = fecha_base + timedelta(hours=random.randint(2, 12))
                    registro_parto = self.crear_registro_parto(ficha, ficha_parto, fecha_parto_real)
                    partos_creados += 1
                    self.stdout.write(f'  [OK] Registro de Parto creada')
                    
                    # 6. Crear Recién Nacido(s)
                    num_rn = 2 if random.random() < 0.05 else 1
                    for n in range(num_rn):
                        fecha_nac = fecha_parto_real + timedelta(minutes=random.randint(0, 15))
                        self.crear_recien_nacido(registro_parto, fecha_nac)
                        rn_creados += 1
                    self.stdout.write(f'  [OK] {num_rn} Recién Nacido(s) creado(s)')
                    
                    # Cerrar ficha
                    if fecha_parto_real < timezone.now() - timedelta(days=7):
                        ficha.parto_completado = True
                        ficha.ficha_cerrada = True
                        ficha.fecha_cierre = fecha_parto_real + timedelta(days=2)
                        ficha.usuario_cierre = self.usuario_admin
                        ficha.save()
                
                # 7. Agregar Medicamentos
                if random.random() < 0.5:
                    self.agregar_medicamentos(ficha, fecha_base)
                    self.stdout.write(f'  [OK] Medicamentos agregados')

            except Exception as e:
                errores += 1
                self.stdout.write(self.style.ERROR(f'  [ERROR] ERROR en registro {i+1}: {str(e)}'))
                # import traceback
                # traceback.print_exc()
                continue
        
        # Resumen Final
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS('PROCESO FINALIZADO'))
        self.stdout.write('=' * 70)
        self.stdout.write(f'Total Fichas Obstétricas: {fichas_creadas}')
        self.stdout.write(f'Total Registros de Parto: {partos_creados}')
        self.stdout.write(f'Total Recién Nacidos:     {rn_creados}')
        self.stdout.write(f'Errores:                  {errores}')
        self.stdout.write('=' * 70)

    def preparar_datos_base(self):
        """Carga catálogos y usuarios necesarios en caché de la instancia"""
        # Usuarios
        self.usuario_admin = User.objects.filter(is_superuser=True).first()
        self.matrona = User.objects.filter(groups__name='Matrona').first() or self.usuario_admin
        
        # Catálogos Persona
        self.sexo_femenino = CatalogoSexo.objects.filter(nombre__icontains='Feme').first()
        if not self.sexo_femenino:
             self.sexo_femenino = CatalogoSexo.objects.first()
        
        self.nacionalidad_chilena = CatalogoNacionalidad.objects.filter(nombre__icontains='Chil').first() or CatalogoNacionalidad.objects.first()
        self.prevision_fonasa = CatalogoPrevision.objects.filter(nombre__icontains='FONASA').first() or CatalogoPrevision.objects.first()

        # Catálogos Parto
        self.tipos_parto = list(CatalogoTipoParto.objects.filter(activo=True))
        self.clasif_robson = list(CatalogoClasificacionRobson.objects.filter(activo=True))
        self.posiciones_parto = list(CatalogoPosicionParto.objects.filter(activo=True))
        self.estados_perine = list(CatalogoEstadoPerine.objects.filter(activo=True))
        
        # Catálogos Ingreso
        self.estados_cervicales = list(CatalogoEstadoCervical.objects.filter(activo=True))
        self.posiciones_fetales = list(CatalogoPosicionFetal.objects.filter(activo=True))
        self.alturas_presentacion = list(CatalogoAlturaPresentacion.objects.filter(activo=True))
        self.salas = list(CatalogoSalaAsignada.objects.filter(activo=True))
        self.aros = list(CatalogoARO.objects.filter(activo=True))

        # Catálogos Adicionales
        self.pueblos_originarios = list(CatalogoPuebloOriginario.objects.filter(activo=True))
        self.consultorios = list(CatalogoConsultorioOrigen.objects.filter(activo=True))

        # Catálogos RN
        self.sexos_rn = list(CatalogoSexoRN.objects.filter(activo=True))
        
        # Catálogos Medicamentos
        self.medicamentos_list = list(CatalogoMedicamento.objects.filter(activo=True))
        self.vias_admin = list(CatalogoViaAdministracion.objects.filter(activo=True))

        if not self.tipos_parto:
            self.stdout.write(self.style.ERROR('[ERROR] No hay tipos de parto configurados.'))
            return False
            
        return True

    def generar_fecha_2025(self):
        """Retorna fecha aleatoria en 2025 hasta hoy (o Dic 18)"""
        start = datetime(2025, 1, 1, tzinfo=timezone.get_current_timezone())
        end = datetime(2025, 12, 18, tzinfo=timezone.get_current_timezone())
        delta = end - start
        random_seconds = random.randint(0, int(delta.total_seconds()))
        return start + timedelta(seconds=random_seconds)

    def crear_paciente(self, i, fecha):
        # Listas para datos fake
        nombres = ['María', 'Ana', 'Sofia', 'Isabella', 'Camila', 'Valentina', 'Josefa', 'Martina']
        apellidos = ['González', 'Muñoz', 'Rojas', 'Díaz', 'Pérez', 'Soto', 'Contreras', 'Silva']
        
        nom = random.choice(nombres)
        pat = random.choice(apellidos)
        mat = random.choice(apellidos)
        
        rut_base = 15000000 + i * 100 + random.randint(0,99)
        rut = f"{rut_base}-{random.randint(0,9)}"
        
        # Verificar si existe Rut
        if Persona.objects.filter(Rut=rut).exists():
            rut = f"{rut_base+5000000}-{random.randint(0,9)}"

        persona = Persona.objects.create(
            Rut=rut,
            Nombre=nom,
            Apellido_Paterno=pat,
            Apellido_Materno=mat,
            Fecha_nacimiento=(fecha - timedelta(days=365*random.randint(18, 40))).date(),
            Sexo=self.sexo_femenino,
            Nacionalidad=self.nacionalidad_chilena,
            Direccion='Dirección Demo 123',
            Comuna='Santiago',
            Pueblos_originarios=random.choice(self.pueblos_originarios) if self.pueblos_originarios and random.random() < 0.3 else None,
            Activo=True
        )
        
        paciente, _ = Paciente.objects.get_or_create(
            persona=persona,
            defaults={
                'prevision': self.prevision_fonasa,
                'grupo_sanguineo': random.choice(['O+', 'A+', 'B+']),
                'numero_ficha_hospital': f"FH-{random.randint(10000,99999)}"
            }
        )
        return paciente

    def crear_ficha_obstetrica(self, paciente, fecha):
        # Ficha base
        ficha = FichaObstetrica.objects.create(
            paciente=paciente,
            numero_ficha=f"FO-{fecha.year}-{random.randint(1000, 99999)}",
            matrona_responsable=self.matrona,
            # Seccion 8: Embarazo actual
            fecha_ultima_regla=(fecha - timedelta(days=280)).date(), # Aprox termino
            fecha_probable_parto=fecha.date(),
            edad_gestacional_semanas=random.randint(37, 41),
            edad_gestacional_dias=random.randint(0, 6),
            cantidad_bebes=1,
            # Seccion 9: VIH
            vih_1_realizado=True,
            vih_1_resultado='NEGATIVO',
            vih_1_fecha=(fecha - timedelta(days=random.randint(90, 150))).date(),
            # VIH 2 (40% probabilidad)
            vih_2_realizado=True if random.random() < 0.4 else False,
            vih_2_resultado='NEGATIVO',
            vih_2_fecha=(fecha - timedelta(days=random.randint(30, 60))).date(),
            # Datos Antropométricos y Origen
            peso_actual=random.uniform(55, 95),
            talla_actual=random.randint(155, 175),
            consultorio_origen=random.choice(self.consultorios) if self.consultorios else None,
            clasificacion_aro=random.choice(self.aros) if self.aros else None,
            # Acompañante
            tiene_acompanante=True,
            nombre_acompanante="Juan Pérez" if random.random() < 0.5 else "Pedro Soto",
            rut_acompanante="12345678-9",
            parentesco_acompanante=random.choice(['ESPOSO', 'MADRE', 'HERMANA']),
            telefono_acompanante="+56912345678",
            # Contacto Emergencia
            nombre_contacto_emergencia="María González",
            telefono_emergencia="+56987654321",
            parentesco_contacto_emergencia="MADRE",
            # Metadata
            fecha_creacion=fecha
        )
        return ficha

    def crear_ficha_parto(self, ficha_obstetrica, fecha):
        sala = random.choice(self.salas) if self.salas else None
        
        ficha_parto = FichaParto.objects.create(
            ficha_obstetrica=ficha_obstetrica,
            numero_ficha_parto=f"IP-{random.randint(10000,99999)}",
            sala_asignada=sala,
            fecha_ingreso=fecha.date(),
            hora_ingreso=fecha.time(),
            edad_gestacional_semanas=ficha_obstetrica.edad_gestacional_semanas,
            edad_gestacional_dias=ficha_obstetrica.edad_gestacional_dias,
            # Evaluación Cervical
            dilatacion_cervical_cm=random.randint(3, 9),
            estado_cervical=random.choice(self.estados_cervicales) if self.estados_cervicales else None,
            borramiento=random.randint(50, 100),
            # Evaluación Fetal
            posicion_fetal=random.choice(self.posiciones_fetales) if self.posiciones_fetales else None,
            altura_presentacion=random.choice(self.alturas_presentacion) if self.alturas_presentacion else None,
            frecuencia_cardiaca_fetal=random.randint(120, 160),
            membranas_rotas=random.choice([True, False]),
            # VIH Intraparto
            vih_tomado_sala=True,
            vih_resultado='NEGATIVO',
            activa=True,
            creado_por=self.matrona
        )
        return ficha_parto

    def crear_registro_parto(self, ficha_obst, ficha_parto, fecha_hora):
        tipo = random.choice(self.tipos_parto) if self.tipos_parto else None
        robson = random.choice(self.clasif_robson) if self.clasif_robson else None
        
        parto = RegistroParto.objects.create(
            ficha_obstetrica=ficha_obst,
            ficha_ingreso_parto=ficha_parto,
            numero_registro=f"RP-{random.randint(100000, 999999)}",
            fecha_hora_parto=fecha_hora,
            edad_gestacional_semanas=ficha_obst.edad_gestacional_semanas,
            edad_gestacional_dias=ficha_obst.edad_gestacional_dias,
            tipo_parto=tipo,
            clasificacion_robson=robson,
            posicion_parto=random.choice(self.posiciones_parto) if self.posiciones_parto else None,
            tiempo_trabajo_parto_total_minutos=random.randint(120, 600),
            estado_perine=random.choice(self.estados_perine) if self.estados_perine else None,
            alumbramiento_dirigido=True,
            retira_placenta=True,
            profesional_responsable_nombre=self.matrona.first_name,
            profesional_responsable_apellido=self.matrona.last_name,
            # Ley Dominga
            ley_dominga_recuerdos="Huella, Foto, Ajuar" if random.random() < 0.9 else "",
            ley_dominga_justificacion="No aplica" if random.random() < 0.9 else "Rechaza recuerdo",
            activo=True
        )
        return parto

    def crear_recien_nacido(self, parto, fecha_hora):
        sexo = random.choice(self.sexos_rn) if self.sexos_rn else None
        peso = random.randint(2500, 4200)
        talla = random.uniform(48.0, 54.0)
        
        rn = RegistroRecienNacido.objects.create(
            registro_parto=parto,
            sexo=sexo,
            peso_gramos=peso,
            talla_centimetros=round(talla, 1),
            apgar_1_minuto=random.randint(7, 9),
            apgar_5_minutos=random.randint(9, 10),
            ligadura_tardia_cordon=True,
            tiempo_ligadura_minutos=random.randint(1, 3),
            apego_piel_con_piel=True,
            tiempo_primer_apego_minutos=random.randint(30, 60),
            lactancia_iniciada=True,
            fecha_nacimiento=fecha_hora.date(),
            hora_nacimiento=fecha_hora.time(),
            matrona_responsable=f"{self.matrona.first_name} {self.matrona.last_name}",
            activo=True
        )
        return rn

    def agregar_medicamentos(self, ficha, fecha):
        if not self.medicamentos_list:
            return
            
        med = random.choice(self.medicamentos_list)
        via = random.choice(self.vias_admin) if self.vias_admin else None
        
        MedicamentoFicha.objects.create(
            ficha=ficha,
            medicamento=med,
            dosis="1 ampolla",
            via_administracion=via,
            fecha_administracion=fecha + timedelta(hours=random.randint(1, 4)),
            responsable=self.matrona,
            observaciones="Administración durante trabajo de parto demo"
        )
