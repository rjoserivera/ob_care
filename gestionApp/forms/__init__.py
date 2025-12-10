"""
Importaciones centralizadas de formularios de gestionApp
"""

from .persona_form import PersonaForm, BuscarPersonaForm  # ✅ AGREGADO BuscarPersonaForm
from .paciente_form import PacienteForm
from .medico_form import MedicoForm
from .matrona_form import MatronaForm
from .tens_form import TensForm

__all__ = [
    'PersonaForm',
    'BuscarPersonaForm',  # ✅ AGREGADO
    'PacienteForm',
    'MedicoForm',
    'MatronaForm',
    'TensForm',
]