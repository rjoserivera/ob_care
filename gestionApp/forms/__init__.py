"""
Importaciones centralizadas de formularios de gestionApp
"""

from .persona_form import PersonaForm
from .paciente_form import PacienteForm
from .medico_form import MedicoForm
from .matrona_form import MatronaForm
from .tens_form import TensForm

__all__ = [
    'PersonaForm',
    'PacienteForm',
    'MedicoForm',
    'MatronaForm',
    'TensForm',
]