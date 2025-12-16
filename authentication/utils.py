"""Utilidades compartidas para autenticación y redirecciones por rol."""
import unicodedata
from typing import Optional
from django.urls import reverse_lazy

ROLE_REDIRECT_MAP = {
    "administrador": "authentication:dashboard_admin",
    "admin": "authentication:dashboard_admin",
    "administradores": "authentication:dashboard_admin",

    "medico": "medico:menu_medico",  # Actualizado para usar vista correcta
    "medicos": "medico:menu_medico",

    "matrona": "matrona:menu_matrona",  # Actualizado para usar vista correcta
    "matronas": "matrona:menu_matrona",

    "tens": "tens:menu_tens",  # Actualizado para usar vista correcta
    "tecnico en enfermeria": "tens:menu_tens",
}

def _normalize_role_name(name: str) -> str:
    normalized = unicodedata.normalize("NFD", name)
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn").lower().strip()

def user_has_role(user, role_key: str) -> bool:
    normalized_role = _normalize_role_name(role_key)
    normalized_groups = {
        _normalize_role_name(name)
        for name in user.groups.values_list("name", flat=True)
    }
    return normalized_role in normalized_groups

def get_dashboard_url_for_user(user) -> Optional[str]:
    if not user.is_authenticated:
        return None

    if user.is_superuser or user.is_staff:
        return reverse_lazy("authentication:dashboard_admin")

    normalized_groups = {
        _normalize_role_name(name)
        for name in user.groups.values_list("name", flat=True)
    }

    for role_key, url_name in ROLE_REDIRECT_MAP.items():
        if role_key in normalized_groups:
            return reverse_lazy(url_name)

    return None
