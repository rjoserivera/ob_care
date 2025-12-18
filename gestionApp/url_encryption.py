"""
gestionApp/url_encryption.py
Sistema de encriptación y ofuscación de URLs para mayor seguridad
"""

from django.conf import settings
from django.core.signing import Signer, BadSignature
from hashlib import sha256
import base64
import secrets


class URLEncryptor:
    """
    Clase para encriptar y desencriptar parámetros de URL
    Usa Django's signing framework para seguridad
    """
    
    def __init__(self):
        # Usar SECRET_KEY de Django para firmar
        self.signer = Signer(salt='url-encryption-salt')
    
    def encrypt_id(self, obj_id):
        """
        Encripta un ID numérico en un token seguro
        
        Args:
            obj_id: ID del objeto (int o str)
            
        Returns:
            str: Token encriptado y firmado
            
        Example:
            >>> encryptor = URLEncryptor()
            >>> token = encryptor.encrypt_id(123)
            >>> print(token)  # 'MTIz:1a2b3c4d5e6f...'
        """
        # Convertir a string y codificar en base64
        id_str = str(obj_id)
        encoded = base64.urlsafe_b64encode(id_str.encode()).decode()
        
        # Firmar para prevenir manipulación
        signed = self.signer.sign(encoded)
        
        return signed
    
    def decrypt_id(self, token):
        """
        Desencripta un token y retorna el ID original
        
        Args:
            token: Token encriptado
            
        Returns:
            int: ID original o None si el token es inválido
            
        Example:
            >>> encryptor = URLEncryptor()
            >>> obj_id = encryptor.decrypt_id('MTIz:1a2b3c4d5e6f...')
            >>> print(obj_id)  # 123
        """
        try:
            # Verificar firma
            unsigned = self.signer.unsign(token)
            
            # Decodificar base64
            decoded = base64.urlsafe_b64decode(unsigned.encode()).decode()
            
            # Convertir a int
            return int(decoded)
        except (BadSignature, ValueError, Exception):
            return None
    
    def generate_access_token(self, user_id, resource_id, resource_type='ficha'):
        """
        Genera un token de acceso único para un recurso específico
        
        Args:
            user_id: ID del usuario
            resource_id: ID del recurso
            resource_type: Tipo de recurso ('ficha', 'parto', 'paciente', etc.)
            
        Returns:
            str: Token de acceso único
        """
        # Crear un hash único basado en usuario, recurso y un salt aleatorio
        salt = secrets.token_hex(8)
        data = f"{user_id}:{resource_id}:{resource_type}:{salt}"
        
        # Generar hash SHA256
        hash_obj = sha256(data.encode())
        token = hash_obj.hexdigest()[:32]  # Usar solo los primeros 32 caracteres
        
        return token
    
    def create_secure_url_params(self, **kwargs):
        """
        Crea parámetros de URL seguros encriptando todos los valores
        
        Args:
            **kwargs: Pares clave-valor a encriptar
            
        Returns:
            dict: Diccionario con valores encriptados
            
        Example:
            >>> encryptor = URLEncryptor()
            >>> params = encryptor.create_secure_url_params(ficha_id=123, paciente_id=456)
            >>> print(params)  # {'f': 'MTIz:...', 'p': 'NDU2:...'}
        """
        encrypted_params = {}
        
        # Mapeo de nombres largos a cortos para ofuscación adicional
        name_mapping = {
            'ficha_id': 'f',
            'paciente_id': 'p',
            'parto_id': 'pt',
            'persona_id': 'ps',
            'medicamento_id': 'm',
            'rn_id': 'rn',
            'user_id': 'u',
        }
        
        for key, value in kwargs.items():
            # Usar nombre corto si existe, sino usar el original
            short_key = name_mapping.get(key, key)
            
            # Encriptar el valor
            encrypted_value = self.encrypt_id(value)
            
            encrypted_params[short_key] = encrypted_value
        
        return encrypted_params
    
    def decrypt_url_params(self, **kwargs):
        """
        Desencripta parámetros de URL
        
        Args:
            **kwargs: Pares clave-valor encriptados
            
        Returns:
            dict: Diccionario con valores desencriptados
        """
        decrypted_params = {}
        
        # Mapeo inverso
        name_mapping = {
            'f': 'ficha_id',
            'p': 'paciente_id',
            'pt': 'parto_id',
            'ps': 'persona_id',
            'm': 'medicamento_id',
            'rn': 'rn_id',
            'u': 'user_id',
        }
        
        for key, value in kwargs.items():
            # Usar nombre largo si existe
            long_key = name_mapping.get(key, key)
            
            # Desencriptar el valor
            decrypted_value = self.decrypt_id(value)
            
            if decrypted_value is not None:
                decrypted_params[long_key] = decrypted_value
        
        return decrypted_params


# Instancia global para uso en toda la aplicación
url_encryptor = URLEncryptor()


# Funciones de conveniencia
def encrypt_id(obj_id):
    """Función de conveniencia para encriptar un ID"""
    return url_encryptor.encrypt_id(obj_id)


def decrypt_id(token):
    """Función de conveniencia para desencriptar un token"""
    return url_encryptor.decrypt_id(token)


def create_secure_params(**kwargs):
    """Función de conveniencia para crear parámetros seguros"""
    return url_encryptor.create_secure_url_params(**kwargs)


def decrypt_params(**kwargs):
    """Función de conveniencia para desencriptar parámetros"""
    return url_encryptor.decrypt_url_params(**kwargs)
