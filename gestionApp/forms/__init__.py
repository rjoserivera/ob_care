"""
gestionApp/forms/__init__.py
Importaciones centralizadas de formularios de gestionApp
SIMPLIFICADO: Solo Persona y Paciente (sin Medico, Matrona, Tens)
"""

from .persona_form import PersonaForm, BuscarPersonaForm
from .paciente_form import PacienteForm

__all__ = [
    'PersonaForm',
    'BuscarPersonaForm',
    'PacienteForm',
]