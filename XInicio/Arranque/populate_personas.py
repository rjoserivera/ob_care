import os
import sys
import django
import random
from datetime import date

# Configuración de entorno
# Configuración de entorno
# Corregir la ruta al directorio raíz (ob_care) desde XInicio/Arranque
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')

django.setup()

from gestionApp.models import Persona, CatalogoSexo, CatalogoNacionalidad, CatalogoPuebloOriginario, CatalogoEstadoCivil

# ==========================================
# GENERADORES
# ==========================================

NOMBRES_HOMBRES = [
    "Juan", "Pedro", "Diego", "Jose", "Luis", "Carlos", "Jorge", "Manuel", "Victor", "Francisco",
    "Antonio", "Miguel", "David", "Daniel", "Javier", "Ricardo", "Fernando", "Roberto", "Pablo", "Alejandro",
    "Esteban", "Gonzalo", "Matias", "Ignacio", "Nicolas", "Sebastian", "Cristian", "Andres", "Felipe", "Rodrigo"
]

NOMBRES_MUJERES = [
    "Maria", "Ana", "Isabel", "Laura", "Carolina", "Andrea", "Camila", "Daniela", "Valentina", "Sofia",
    "Fernanda", "Gabriela", "Patricia", "Carmen", "Rosa", "Claudia", "Paula", "Loreto", "Veronica", "Teresa",
    "Natalia", "Javiera", "Constanza", "Francisca", "Isidora", "Agustina", "Florencia", "Martina", "Catalina", "Emilia"
]

APELLIDOS = [
    "Gonzalez", "Muñoz", "Rojas", "Diaz", "Perez", "Soto", "Contreras", "Silva", "Martinez", "Sepulveda",
    "Morales", "Rodriguez", "Lopez", "Fuentes", "Hernandez", "Torres", "Araya", "Flores", "Espinoza", "Valenzuela",
    "Castillo", "Tapia", "Reyes", "Gutierrez", "Castro", "Pizarro", "Alvarez", "Vasquez", "Sanchez", "Fernandez",
    "Ramirez", "Carrasco", "Gomez", "Cortes", "Herrera", "Nuñez", "Jara", "Vergara", "Rivera", "Figueroa"
]

COMUNAS_NUBLE = [
    "Chillán", "Chillán Viejo", "San Carlos", "Coihueco", "Pinto", "Bulnes", "Quillón", 
    "San Nicolás", "Yungay", "Ñiquén", "Treguaco", "Cobquecura", "Coelemu", "Ninhue",
    "Portezuelo", "Quirihue", "Ránquil", "San Fabián", "San Ignacio", "El Carmen", "Pemuco"
]

def generar_rut():
    """Genera un RUT válido"""
    # Rut de población general (8-26 mill)
    numero = random.randint(8000000, 26000000)
    cuerpo = str(numero)
    
    suma = 0
    multiplo = 2
    for d in reversed(cuerpo):
        suma += int(d) * multiplo
        multiplo += 1
        if multiplo > 7: multiplo = 2
    
    resto = suma % 11
    dv_calc = 11 - resto
    if dv_calc == 11: dv = '0'
    elif dv_calc == 10: dv = 'K'
    else: dv = str(dv_calc)
    
    return f"{cuerpo}-{dv}"

def populate_personas():
    CANTIDAD = 100
    print(f"🚀 INICIANDO CREACIÓN DE {CANTIDAD} PERSONAS...")
    
    # 1. Obtener Catálogos (Deben estar previamente poblados por populate_full_system)
    try:
        sexo_m = CatalogoSexo.objects.get(codigo='M')
        sexo_f = CatalogoSexo.objects.get(codigo='F')
        
        # Nacionalidades (Weighted preference for Chilean)
        nacionalidades = list(CatalogoNacionalidad.objects.filter(activo=True))
        if not nacionalidades:
             # Fallback simple
            nacionalidades = [CatalogoNacionalidad.objects.get_or_create(codigo='CL', defaults={'nombre': 'Chilena'})[0]]

        # Pueblos Originarios
        pueblos_orig = list(CatalogoPuebloOriginario.objects.filter(activo=True))
        if not pueblos_orig:
            pueblos_orig = [CatalogoPuebloOriginario.objects.get_or_create(codigo='NINGUNO', defaults={'nombre': 'Ninguno'})[0]]

        # Estado Civil
        estados_civil = list(CatalogoEstadoCivil.objects.filter(activo=True))
        if not estados_civil:
            estados_civil = [CatalogoEstadoCivil.objects.get_or_create(codigo='SOLTERA', defaults={'nombre': 'Soltera'})[0]]

    except Exception as e:
        print(f"❌ Error cargando catálogos: {e}")
        print("Asegúrate de ejecutar populate_full_system.py primero.")
        return

    creados = 0
    intentos = 0
    
    while creados < CANTIDAD and intentos < CANTIDAD * 5:
        intentos += 1
        
        # Generar datos básicos
        es_mujer = random.choice([True, False])
        if es_mujer:
            nombre = random.choice(NOMBRES_MUJERES)
            sexo = sexo_f
        else:
            nombre = random.choice(NOMBRES_HOMBRES)
            sexo = sexo_m
            
        ape_p = random.choice(APELLIDOS)
        ape_m = random.choice(APELLIDOS)
        
        rut = generar_rut()
        
        # Verificar duplicidad de RUT
        if Persona.objects.filter(Rut=rut).exists():
            continue
            
        # Selección de Catálogos (Weighted)
        # 90% Chilena
        nac = random.choices(nacionalidades, weights=[10 if n.codigo == 'CL' else 1 for n in nacionalidades], k=1)[0]
        
        # 80% Ningún pueblo originario
        pueblo = random.choices(pueblos_orig, weights=[10 if p.codigo == 'NINGUNO' else 1 for p in pueblos_orig], k=1)[0]
        
        est_civil = random.choice(estados_civil)

        try:
            Persona.objects.create(
                Rut=rut,
                Nombre=nombre,
                Apellido_Paterno=ape_p,
                Apellido_Materno=ape_m,
                Fecha_nacimiento=date(random.randint(1960, 2005), random.randint(1, 12), random.randint(1, 28)),
                Sexo=sexo,
                Nacionalidad=nac,
                Pueblos_originarios=pueblo,
                Estado_civil=est_civil,
                Telefono=f"+569{random.randint(10000000, 99999999)}",
                Direccion=f"Calle {random.choice(['Principal', 'Sur', 'Norte', 'Los Heroes', 'Prat', 'Carrera', 'O Higgins'])} {random.randint(100, 9999)}",
                Comuna=random.choice(COMUNAS_NUBLE),
                Email=f"{nombre.lower()[:3]}{ape_p.lower()}{random.randint(1,99)}@gmail.com", # Email más simple
                Activo=True
            )
            
            if (creados + 1) % 10 == 0:
                print(f"  ... {creados + 1} personas creadas")
                
            creados += 1
            
        except Exception as e:
            print(f"❌ Error creando persona {rut}: {e}")

    print(f"\n✨ {creados} PERSONAS CREADAS EXITOSAMENTE ✨")

if __name__ == '__main__':
    populate_personas()
