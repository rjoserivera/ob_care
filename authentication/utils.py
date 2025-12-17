"""Utilidades compartidas para autenticación y redirecciones por rol."""
import unicodedata
from typing import Optional
from django.urls import reverse_lazy

ROLE_REDIRECT_MAP = {
    "administrador": "authentication:dashboard_admin",
    "admin": "authentication:dashboard_admin",
    "administradores": "authentication:dashboard_admin",

    "medico": "authentication:dashboard_medico",
    "medicos": "authentication:dashboard_medico",

    "matrona": "authentication:dashboard_matrona",
    "matronas": "authentication:dashboard_matrona",

    "tecnico en enfermeria": "authentication:dashboard_tens",
    "tens": "authentication:dashboard_tens",
}

ROLE_ALIASES = {
    # Canonicals (Database is Singular)
    "administradores": "administrador",
    "admin": "administrador",
    "administrador": "administrador",

    "medicos": "medico",
    "medico": "medico",

    "matronas": "matrona",
    "matrona": "matrona",

    "tens": "tens",
    "tecnico en enfermeria": "tens",
}

def _normalize_role_name(name: str) -> str:
    normalized = unicodedata.normalize("NFD", name)
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn").lower().strip()

def user_has_role(user, role_key: str) -> bool:
    target_canonical = _normalize_role_name(role_key)
    
    # Resolve alias if exists for the TARGET role
    if target_canonical in ROLE_ALIASES:
        target_canonical = ROLE_ALIASES[target_canonical]
        
    # Get user groups and normalize them
    normalized_groups_raw = {
        _normalize_role_name(name)
        for name in user.groups.values_list("name", flat=True)
    }
    
    # Map user groups to their canonical forms
    user_groups_canonical = set()
    for g in normalized_groups_raw:
        if g in ROLE_ALIASES:
            user_groups_canonical.add(ROLE_ALIASES[g])
        else:
            user_groups_canonical.add(g)

    return target_canonical in user_groups_canonical

def get_dashboard_url_for_user(user) -> Optional[str]:
    if not user.is_authenticated:
        return None

    if user.is_superuser:
        return reverse_lazy("authentication:dashboard_admin")

    normalized_groups = {
        _normalize_role_name(name)
        for name in user.groups.values_list("name", flat=True)
    }

    for role_key, url_name in ROLE_REDIRECT_MAP.items():
        if role_key in normalized_groups:
            return reverse_lazy(url_name)

    return None
