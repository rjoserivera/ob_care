# partosApp/forms/__init__.py
"""
Formularios de partosApp - Registro de partos
"""

# Formularios existentes en partosApp/forms/
from .paso6_profesionales_form import ProfesionalesForm
from .registro_parto_completo_form import RegistroPartoCompletoForm

# Todos los demás formularios son el form completo usado parcialmente
RegistroPartoBaseForm = RegistroPartoCompletoForm
TrabajoDePartoForm = RegistroPartoCompletoForm
InformacionPartoForm = RegistroPartoCompletoForm
PuerperioForm = RegistroPartoCompletoForm
AnestesiaAnalgesiaForm = RegistroPartoCompletoForm

# Formularios de RN y documentos (están en recienNacidoApp)
from recienNacidoApp.forms import RegistroRecienNacidoForm, DocumentosPartoForm

# Aliases para compatibilidad
DatosRecienNacidoForm = RegistroRecienNacidoForm
ApegoAcompanamientoForm = RegistroRecienNacidoForm

__all__ = [
    'RegistroPartoBaseForm',
    'TrabajoDePartoForm',
    'InformacionPartoForm',
    'PuerperioForm',
    'AnestesiaAnalgesiaForm',
    'ProfesionalesForm',
    'RegistroPartoCompletoForm',
    'RegistroRecienNacidoForm',
    'DatosRecienNacidoForm',
    'ApegoAcompanamientoForm',
    'DocumentosPartoForm',
]