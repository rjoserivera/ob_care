"""
VALIDADOR DE RUT CHILENO - VERSIÓN CORREGIDA
Sistema completo de validación, formateo y separación de RUT
Compatible con Django y uso independiente
"""

import re
from django.core.exceptions import ValidationError
from typing import Dict


class RutValidator:
    """Clase para validar y manipular RUTs chilenos"""
    
    @staticmethod
    def limpiar(rut: str) -> str:
        """
        Limpia el RUT eliminando puntos, guiones y espacios.
        Convierte a mayúsculas.
        """
        if not rut:
            return ''
        return str(rut).replace('.', '').replace('-', '').replace(' ', '').upper()
    
    @staticmethod
    def separar(rut: str) -> Dict[str, str]:
        """
        Separa el RUT en cuerpo y dígito verificador.
        """
        rut_limpio = RutValidator.limpiar(rut)
        
        if len(rut_limpio) < 2:
            return {'cuerpo': '', 'dv': ''}
        
        return {
            'cuerpo': rut_limpio[:-1],
            'dv': rut_limpio[-1]
        }
    
    @staticmethod
    def calcular_dv(cuerpo: str) -> str:
        """
        Calcula el dígito verificador de un RUT.
        
        ALGORITMO MÓDULO 11:
        - Multiplicar cada dígito (de derecha a izquierda) por 2,3,4,5,6,7,2,3,4...
        - Sumar todos los productos
        - Calcular 11 - (suma % 11)
        - Si resultado es 11 → '0', si es 10 → 'K', sino el número
        """
        # Limpiar el cuerpo (solo números)
        cuerpo_limpio = re.sub(r'\D', '', str(cuerpo))
        
        if not cuerpo_limpio:
            return ''
        
        suma = 0
        multiplicador = 2
        
        # Recorrer de derecha a izquierda
        for digito in reversed(cuerpo_limpio):
            suma += int(digito) * multiplicador
            multiplicador += 1
            if multiplicador > 7:
                multiplicador = 2
        
        resto = suma % 11
        dv_calculado = 11 - resto
        
        # Retornar el DV correspondiente
        if dv_calculado == 11:
            return '0'
        elif dv_calculado == 10:
            return 'K'
        else:
            return str(dv_calculado)
    
    @staticmethod
    def validar(rut: str) -> bool:
        """
        Valida si un RUT es correcto.
        """
        rut_limpio = RutValidator.limpiar(rut)
        
        # Validar longitud mínima
        if len(rut_limpio) < 2:
            return False
        
        # Validar formato: 7-8 dígitos + dígito verificador
        if not re.match(r'^\d{7,8}[0-9Kk]$', rut_limpio):
            return False
        
        datos = RutValidator.separar(rut_limpio)
        dv_calculado = RutValidator.calcular_dv(datos['cuerpo'])
        
        return datos['dv'] == dv_calculado
    
    @staticmethod
    def formatear(rut: str) -> str:
        """
        Formatea un RUT con puntos y guión (12.345.678-9).
        """
        datos = RutValidator.separar(rut)
        
        if not datos['cuerpo'] or not datos['dv']:
            return rut
        
        # Agregar puntos cada 3 dígitos de derecha a izquierda
        cuerpo = datos['cuerpo']
        cuerpo_formateado = ''
        contador = 0
        
        for i in range(len(cuerpo) - 1, -1, -1):
            if contador == 3:
                cuerpo_formateado = '.' + cuerpo_formateado
                contador = 0
            cuerpo_formateado = cuerpo[i] + cuerpo_formateado
            contador += 1
        
        return f"{cuerpo_formateado}-{datos['dv']}"
    
    @staticmethod
    def normalizar(rut: str) -> str:
        """
        Normaliza el RUT al formato sin puntos pero con guión (12345678-9).
        Este es el formato que se guarda en la base de datos.
        """
        datos = RutValidator.separar(rut)
        
        if not datos['cuerpo'] or not datos['dv']:
            return rut
        
        return f"{datos['cuerpo']}-{datos['dv']}"


# ============================================
# FUNCIONES AUXILIARES PARA DJANGO
# ============================================

def validar_rut_chileno(value: str) -> str:
    """
    Validador de Django para campo RUT.
    Lanza ValidationError si el RUT no es válido.
    """
    if not value:
        raise ValidationError('El RUT es obligatorio.')
    
    rut_limpio = RutValidator.limpiar(value)
    
    # Validar formato
    if not re.match(r'^\d{7,8}[0-9Kk]$', rut_limpio):
        raise ValidationError(
            'Formato de RUT inválido. Use el formato: 12345678-9'
        )
    
    # Validar dígito verificador
    if not RutValidator.validar(value):
        raise ValidationError(
            'El dígito verificador del RUT es incorrecto.'
        )
    
    # Retornar normalizado
    return RutValidator.normalizar(value)


def normalizar_rut(rut: str) -> str:
    """
    Alias de RutValidator.normalizar para compatibilidad.
    """
    return RutValidator.normalizar(rut)


def validar_rut(value: str) -> str:
    """
    Alias de validar_rut_chileno para compatibilidad.
    """
    return validar_rut_chileno(value)


# ============================================
# GENERADOR DE RUT ALEATORIO (ÚTIL PARA TESTING)
# ============================================

def generar_rut_aleatorio() -> str:
    """
    Genera un RUT chileno válido aleatorio.
    Útil para pruebas y testing.
    """
    import random
    
    # Generar cuerpo aleatorio (entre 1.000.000 y 99.999.999)
    cuerpo = random.randint(1000000, 99999999)
    dv = RutValidator.calcular_dv(str(cuerpo))
    
    return RutValidator.formatear(f"{cuerpo}{dv}")


# ============================================
# TEST RÁPIDO
# ============================================

if __name__ == '__main__':
    print("=== TEST DEL VALIDADOR DE RUT ===\n")
    
    # Test con el RUT que falló
    rut_test = '13131793-K'
    print(f"RUT: {rut_test}")
    print(f"¿Es válido? {RutValidator.validar(rut_test)}")
    
    # Verificar cálculo
    cuerpo = '13131793'
    dv = RutValidator.calcular_dv(cuerpo)
    print(f"DV calculado para {cuerpo}: {dv}")