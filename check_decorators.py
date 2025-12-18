# Script para verificar decoradores @decrypt_url_params en views.py

vistas_que_necesitan_decorador = [
    # Fichas
    ('crear_ficha_obstetrica', 'paciente_pk'),
    ('crear_ficha_obstetrica_persona', 'persona_pk'),
    ('editar_ficha_obstetrica', 'ficha_pk'),
    ('detalle_ficha_obstetrica', 'ficha_pk'),
    
    # Polling
    ('equipo_confirmado_partial', 'ficha_pk'),  # ✅ YA AGREGADO
    ('debug_rellenar_equipo', 'ficha_parto_id'),
    
    # Medicamentos
    ('agregar_medicamento', 'ficha_pk'),
    ('eliminar_medicamento', 'medicamento_pk'),
    
    # Parto
    ('iniciar_proceso_parto', 'ficha_pk'),  # ✅ YA AGREGADO
    ('proceso_parto_iniciado', 'ficha_pk'),
    ('sala_parto_view', 'ficha_parto_id'),
    ('guardar_registro_parto', 'ficha_parto_id'),
    ('guardar_registro_rn', 'ficha_parto_id'),
    ('cierre_parto_view', 'ficha_parto_id'),
    ('resumen_final_parto_view', 'ficha_parto_id'),
    ('detalle_registro_parto', 'ficha_parto_id'),
    
    # RN
    ('crear_asociacion_rn', 'ficha_parto_id'),
    ('ficha_rn_view', 'rn_id'),
    ('detalle_rn_view', 'rn_id'),
    
    # APIs
    ('agregar_registro_dilatacion', 'ficha_pk'),
    ('verificar_estado_dilatacion', 'ficha_pk'),
    ('registrar_dilatacion', 'ficha_id'),
    ('agregar_medicamento_ajax', 'ficha_pk'),
    ('eliminar_medicamento_ajax', 'medicamento_pk'),
    ('obtener_personal_requerido', 'ficha_pk'),
    ('asignar_personal_parto', 'ficha_parto_id'),
    ('finalizar_asignacion_parto', 'ficha_parto_id'),
    ('responder_asignacion', 'asignacion_id'),
    ('verificar_pin', 'ficha_parto_id'),
]

print("Vistas que necesitan @decrypt_url_params:")
print("=" * 60)
for vista, param in vistas_que_necesitan_decorador:
    print(f"- {vista}(request, {param})")
print(f"\nTotal: {len(vistas_que_necesitan_decorador)} vistas")
