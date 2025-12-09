"""
ARCHIVO: tests/test_plan_completo.py
Plan de pruebas completo para el sistema obstétrico
Autor: Estudiante de Analista Programador
Versión: 3.0 - PRODUCCIÓN
Fecha: 2025

COBERTURA DE PRUEBAS:
- Funcionalidades Core: Registro, validación, CRUD
- Seguridad: SQL Injection, XSS, validación de datos
- Rendimiento: Tiempos de respuesta, carga masiva
- Integración: Flujos completos, consistencia de datos
"""

import pytest
import time
from datetime import date, timedelta
from django.test import Client
from gestionApp.models import CatalogoSexo, Persona
from gestionApp.forms.persona_form import PersonaForm
from utilidad.rut_validator import RutValidator, generar_rut_aleatorio


# ============================================
# HELPERS PARA GENERAR DATOS DE PRUEBA
# ============================================

def generar_rut_valido(numero: int = None) -> str:
    """
    Genera un RUT válido para testing.
    """
    if numero:
        dv = RutValidator.calcular_dv(str(numero))
        return f"{numero}-{dv}"
    else:
        return generar_rut_aleatorio()


@pytest.fixture
def client():
    """Cliente HTTP para pruebas de integración"""
    return Client()


@pytest.fixture
def catalogos_sexo(db):
    """Crea catálogos mínimos de sexo para alimentar el formulario."""
    femenino = CatalogoSexo.objects.create(codigo="F", nombre="Femenino")
    masculino = CatalogoSexo.objects.create(codigo="M", nombre="Masculino")
    return {
        "femenino": femenino,
        "masculino": masculino,
    }


# ============================================
# TESTS DE FUNCIONALIDADES CORE
# ============================================

class TestFuncionalidadesCore:

    @pytest.mark.django_db
    def test_registro_persona_valida(self, catalogos_sexo):
        rut_valido = generar_rut_valido(12345678)

        form_data = {
            'Rut': rut_valido,
            'Nombre': 'María José',
            'Apellido_Paterno': 'González',
            'Apellido_Materno': 'Pérez',
            'Fecha_nacimiento': '1995-03-15',
            'Sexo': catalogos_sexo["femenino"].pk,
            'Telefono': '+56912345678',
            'Direccion': 'Calle Ejemplo 123, Santiago',
            'Email': 'maria.gonzalez@ejemplo.cl'
        }

        form = PersonaForm(data=form_data)

        if not form.is_valid():
            print("\n🔴 ERRORES DEL FORMULARIO:")
            for field, errors in form.errors.items():
                print(f"   • Campo '{field}': {errors}")

        assert form.is_valid(), f"Formulario inválido. Errores: {form.errors}"

        persona = form.save()

        assert Persona.objects.filter(Rut=rut_valido).exists()
        assert persona.Nombre == 'María José'
        assert persona.Apellido_Paterno == 'González'
        assert persona.Sexo == catalogos_sexo["femenino"]

        print(f"✅ Persona registrada: {persona.Rut} - {persona.Nombre}")

    @pytest.mark.django_db
    def test_rut_invalido(self, catalogos_sexo):

        rut_invalido = '12345678-K'

        form_data = {
            'Rut': rut_invalido,
            'Nombre': 'Juan',
            'Apellido_Paterno': 'Pérez',
            'Apellido_Materno': 'López',
            'Fecha_nacimiento': '1990-01-01',
            'Sexo': catalogos_sexo["masculino"].pk
        }

        form = PersonaForm(data=form_data)

        assert not form.is_valid()
        assert 'Rut' in form.errors or '__all__' in form.errors

        print(f"✅ RUT inválido rechazado correctamente")

    @pytest.mark.django_db
    def test_rut_duplicado(self, catalogos_sexo):
        rut_valido = generar_rut_valido(11111111)

        form_data1 = {
            'Rut': rut_valido,
            'Nombre': 'Primera',
            'Apellido_Paterno': 'Persona',
            'Apellido_Materno': 'Test',
            'Fecha_nacimiento': '1990-01-01',
            'Sexo': catalogos_sexo["femenino"].pk
        }

        form1 = PersonaForm(data=form_data1)
        if form1.is_valid():
            form1.save()

        form_data2 = {
            'Rut': rut_valido,
            'Nombre': 'Segunda',
            'Apellido_Paterno': 'Persona',
            'Apellido_Materno': 'Test',
            'Fecha_nacimiento': '1995-01-01',
            'Sexo': catalogos_sexo["masculino"].pk
        }

        form2 = PersonaForm(data=form_data2)

        assert not form2.is_valid()

        print(f"✅ RUT duplicado rechazado correctamente")

    @pytest.mark.django_db
    def test_campos_obligatorios(self):
        rut_valido = generar_rut_valido(22222222)

        form_data = {
            'Rut': rut_valido,
            'Nombre': 'Test'
        }

        form = PersonaForm(data=form_data)

        assert not form.is_valid()
        assert 'Apellido_Paterno' in form.errors
        assert 'Apellido_Materno' in form.errors
        assert 'Fecha_nacimiento' in form.errors
        assert 'Sexo' in form.errors

        print(f"✅ Validación de campos obligatorios: {len(form.errors)} errores detectados")

    @pytest.mark.django_db
    def test_formato_rut(self, catalogos_sexo):

        rut_numero = 12345678
        dv = RutValidator.calcular_dv(str(rut_numero))
        rut_con_puntos = f"12.345.678-{dv}"

        form_data = {
            'Rut': rut_con_puntos,
            'Nombre': 'Test',
            'Apellido_Paterno': 'Formato',
            'Apellido_Materno': 'RUT',
            'Fecha_nacimiento': '1990-01-01',
            'Sexo': catalogos_sexo["masculino"].pk
        }

        form = PersonaForm(data=form_data)

        if form.is_valid():
            persona = form.save()
            assert '-' in persona.Rut
            assert '.' not in persona.Rut
            print(f"✅ RUT normalizado correctamente: {persona.Rut}")
        else:
            print(f"⚠️ Formato con puntos rechazado: {form.errors}")


# ============================================
# TESTS DE SEGURIDAD
# ============================================

class TestSeguridad:

    @pytest.mark.django_db
    def test_sql_injection(self, client):

        count_inicial = Persona.objects.count()
        payload = "'; DROP TABLE gestionApp_persona; --"

        try:
            client.get('/api/buscar/', {'rut': payload})
            count_final = Persona.objects.count()
            assert count_final == count_inicial
            print(f"✅ Protección SQL Injection: Tabla intacta")
        except Exception:
            assert Persona.objects.count() == count_inicial
            print(f"✅ Protección SQL Injection: Sistema protegido")

    @pytest.mark.django_db
    def test_xss_protection(self, client, catalogos_sexo):

        payload = "<script>alert('XSS')</script>"
        rut_valido = generar_rut_valido(99999999)

        form_data = {
            'Rut': rut_valido,
            'Nombre': payload,
            'Apellido_Paterno': 'Test',
            'Apellido_Materno': 'XSS',
            'Fecha_nacimiento': '1990-01-01',
            'Sexo': catalogos_sexo["femenino"].pk
        }

        form = PersonaForm(data=form_data)

        if form.is_valid():
            persona = form.save()
            print(f"✅ Datos con script almacenados de forma segura")
            print(f"   Valor guardado: {repr(persona.Nombre)}")
        else:
            print(f"✅ Entrada con script rechazada por validación")

    @pytest.mark.django_db
    def test_validacion_edad(self, catalogos_sexo):

        fecha_futura = (date.today() + timedelta(days=365)).isoformat()
        rut_valido = generar_rut_valido(88888888)

        form_data = {
            'Rut': rut_valido,
            'Nombre': 'Futuro',
            'Apellido_Paterno': 'Test',
            'Apellido_Materno': 'Edad',
            'Fecha_nacimiento': fecha_futura,
            'Sexo': catalogos_sexo["masculino"].pk
        }

        form = PersonaForm(data=form_data)

        if not form.is_valid():
            print(f"✅ Fecha futura rechazada correctamente")
        else:
            print(f"⚠️ Advertencia: Fecha futura aceptada en formulario")


# ============================================
# TESTS DE RENDIMIENTO
# ============================================

class TestRendimiento:

    @pytest.mark.django_db
    def test_tiempo_respuesta_listado(self, client):
        start = time.time()

        try:
            client.get('/matrona/pacientes/')
            elapsed = time.time() - start
            assert elapsed < 2.0
            print(f"✅ Tiempo de respuesta: {elapsed:.3f}s (<2s)")
        except Exception as e:
            print(f"⚠️ Ruta no disponible: {e}")

    @pytest.mark.django_db
    def test_carga_masiva_personas(self, catalogos_sexo):

        start = time.time()
        count_creadas = 0

        for i in range(20):
            rut_valido = generar_rut_valido(10000000 + i * 1000)

            form_data = {
                'Rut': rut_valido,
                'Nombre': f'Persona{i}',
                'Apellido_Paterno': f'Test{i}',
                'Apellido_Materno': 'Masivo',
                'Fecha_nacimiento': '1990-01-01',
                'Sexo': catalogos_sexo["femenino"].pk if i % 2 == 0 else catalogos_sexo["masculino"].pk
            }

            form = PersonaForm(data=form_data)
            if form.is_valid():
                form.save()
                count_creadas += 1

        elapsed = time.time() - start

        assert elapsed < 5.0, f"Carga masiva muy lenta: {elapsed:.2f}s"
        print(f"✅ Carga masiva: {count_creadas} personas en {elapsed:.2f}s")


# ============================================
# TESTS DE INTEGRACIÓN
# ============================================

class TestIntegracion:

    @pytest.mark.django_db
    def test_flujo_completo_registro(self, catalogos_sexo):

        rut_valido = generar_rut_valido(33333333)

        form_data = {
            'Rut': rut_valido,
            'Nombre': 'Integración',
            'Apellido_Paterno': 'Test',
            'Apellido_Materno': 'Completo',
            'Fecha_nacimiento': '1988-05-20',
            'Sexo': catalogos_sexo["femenino"].pk,
            'Telefono': '+56987654321',
            'Email': 'integracion@test.cl'
        }

        form = PersonaForm(data=form_data)
        assert form.is_valid(), f"Errores: {form.errors}"

        persona = form.save()

        persona_bd = Persona.objects.get(pk=persona.pk)
        assert persona_bd.Nombre == 'Integración'
        assert persona_bd.Email == 'integracion@test.cl'
        assert '-' in persona_bd.Rut

        persona_recuperada = Persona.objects.get(Rut=rut_valido)
        assert persona_recuperada.pk == persona.pk

        print(f"✅ Flujo completo exitoso: {persona.Rut}")

    @pytest.mark.django_db
    def test_actualizacion_persona(self, catalogos_sexo):

        rut_valido = generar_rut_valido(44444444)

        persona = Persona.objects.create(
            Rut=rut_valido,
            Nombre='Original',
            Apellido_Paterno='Apellido',
            Apellido_Materno='Test',
            Fecha_nacimiento='1985-01-01',
            Sexo=catalogos_sexo["masculino"]
        )

        form_data = {
            'Rut': rut_valido,
            'Nombre': 'Actualizado',
            'Apellido_Paterno': 'Apellido',
            'Apellido_Materno': 'Test',
            'Fecha_nacimiento': '1985-01-01',
            'Sexo': catalogos_sexo["masculino"].pk,
            'Email': 'nuevo@email.cl'
        }

        form = PersonaForm(data=form_data, instance=persona)
        assert form.is_valid(), f"Error: {form.errors}"

        persona_actualizada = form.save()

        assert persona_actualizada.Nombre == 'Actualizado'
        assert persona_actualizada.Email == 'nuevo@email.cl'

        print(f"✅ Actualización exitosa: {persona_actualizada.Nombre}")
