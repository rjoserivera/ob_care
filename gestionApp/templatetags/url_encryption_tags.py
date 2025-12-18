"""
gestionApp/templatetags/url_encryption_tags.py
Template tags para usar URLs encriptadas en templates
"""

from django import template
from django.urls import reverse
from gestionApp.url_encryption import url_encryptor

register = template.Library()


@register.simple_tag
def encrypt_id(obj_id):
    """
    Template tag para encriptar un ID
    
    Uso en template:
        {% load url_encryption_tags %}
        {% encrypt_id ficha.id as encrypted_id %}
        <a href="/detalle/{{ encrypted_id }}/">Ver Detalle</a>
    """
    return url_encryptor.encrypt_id(obj_id)


@register.simple_tag
def secure_url(view_name, **kwargs):
    """
    Template tag para generar URLs con parámetros encriptados
    
    Uso en template:
        {% load url_encryption_tags %}
        {% secure_url 'matrona:detalle_ficha' ficha_id=ficha.id %}
    """
    # Encriptar todos los parámetros que terminan en '_id'
    encrypted_kwargs = {}
    
    for key, value in kwargs.items():
        if key.endswith('_id'):
            # Este es un ID, encriptarlo
            encrypted_kwargs[key] = url_encryptor.encrypt_id(value)
        else:
            # No es un ID, dejarlo como está
            encrypted_kwargs[key] = value
    
    # Generar la URL con los parámetros encriptados
    return reverse(view_name, kwargs=encrypted_kwargs)


@register.filter
def encrypt(value):
    """
    Filtro para encriptar un valor
    
    Uso en template:
        {% load url_encryption_tags %}
        <a href="/detalle/{{ ficha.id|encrypt }}/">Ver Detalle</a>
    """
    return url_encryptor.encrypt_id(value)


@register.simple_tag
def obfuscate_params(**kwargs):
    """
    Template tag para ofuscar múltiples parámetros
    
    Uso en template:
        {% load url_encryption_tags %}
        {% obfuscate_params ficha_id=123 paciente_id=456 as params %}
        <a href="/detalle/?f={{ params.f }}&p={{ params.p }}">Ver</a>
    """
    return url_encryptor.create_secure_url_params(**kwargs)
