"""
gestionApp/url_obfuscator.py
Sistema para generar y mantener rutas URL ofuscadas con caracteres aleatorios
"""

import hashlib
import base64
from django.conf import settings

class URLObfuscator:
    """
    Genera rutas URL ofuscadas basadas en un hash del nombre de la ruta
    Las rutas son consistentes (siempre generan el mismo hash para el mismo nombre)
    """
    
    @staticmethod
    def generate_route(route_name, length=8):
        """
        Genera una ruta ofuscada basada en el nombre de la ruta
        
        Args:
            route_name: Nombre interno de la ruta (ej: 'dashboard_admin')
            length: Longitud de la ruta generada (default: 8)
            
        Returns:
            String ofuscado (ej: 'a7f3k9m2')
        """
        # Usar SECRET_KEY + route_name para generar hash único
        secret = settings.SECRET_KEY
        combined = f"{secret}:{route_name}".encode('utf-8')
        
        # Generar hash SHA256
        hash_obj = hashlib.sha256(combined)
        hash_bytes = hash_obj.digest()
        
        # Convertir a base64 y limpiar caracteres especiales
        b64 = base64.urlsafe_b64encode(hash_bytes).decode('utf-8')
        
        # Tomar solo caracteres alfanuméricos en minúsculas
        clean = ''.join(c.lower() for c in b64 if c.isalnum())
        
        # Retornar los primeros 'length' caracteres
        return clean[:length]
    
    @staticmethod
    def generate_route_map():
        """
        Genera un mapa completo de rutas ofuscadas para toda la aplicación
        """
        routes = {
            # Autenticación
            'login': 'access',
            'logout': 'exit',
            'registro': 'join',
            
            # Dashboards
            'dashboard_admin': URLObfuscator.generate_route('dashboard_admin'),
            'dashboard_medico': URLObfuscator.generate_route('dashboard_medico'),
            'dashboard_matrona': URLObfuscator.generate_route('dashboard_matrona'),
            'dashboard_tens': URLObfuscator.generate_route('dashboard_tens'),
            
            # Gestión
            'gestion_personas': URLObfuscator.generate_route('gestion_personas'),
            'gestion_registrar': URLObfuscator.generate_route('gestion_registrar'),
            'gestion_buscar': URLObfuscator.generate_route('gestion_buscar'),
            
            # Matrona
            'matrona_fichas': URLObfuscator.generate_route('matrona_fichas'),
            'matrona_crear': URLObfuscator.generate_route('matrona_crear'),
            'matrona_sala': URLObfuscator.generate_route('matrona_sala'),
            'matrona_historial': URLObfuscator.generate_route('matrona_historial'),
            
            # Médico
            'medico_fichas': URLObfuscator.generate_route('medico_fichas'),
            'medico_consultas': URLObfuscator.generate_route('medico_consultas'),
            
            # TENS
            'tens_pacientes': URLObfuscator.generate_route('tens_pacientes'),
            'tens_tareas': URLObfuscator.generate_route('tens_tareas'),
        }
        
        return routes


# Generar rutas al importar el módulo
OBFUSCATED_ROUTES = URLObfuscator.generate_route_map()


# Función helper para obtener una ruta ofuscada
def get_obfuscated_route(route_name):
    """
    Obtiene la ruta ofuscada para un nombre de ruta dado
    
    Args:
        route_name: Nombre de la ruta (ej: 'dashboard_admin')
        
    Returns:
        Ruta ofuscada (ej: 'a7f3k9m2')
    """
    return OBFUSCATED_ROUTES.get(route_name, URLObfuscator.generate_route(route_name))


# Imprimir mapa de rutas para referencia
def print_route_map():
    """
    Imprime el mapa de rutas ofuscadas para documentación
    """
    print("\n" + "="*80)
    print("MAPA DE RUTAS OFUSCADAS")
    print("="*80)
    
    for route_name, obfuscated in sorted(OBFUSCATED_ROUTES.items()):
        print(f"{route_name:30} -> {obfuscated}")
    
    print("="*80 + "\n")


if __name__ == '__main__':
    # Ejecutar para ver el mapa de rutas
    print_route_map()
