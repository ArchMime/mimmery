# src/database/__init__.py
from src.database.connection import inicializar_db
from src.database.sessions import obtener_o_crear_sesion, finalizar_y_consolidar_sesion, obtener_proyectos_unicos
from src.database.messages import guardar_mensaje_en_vivo, obtener_mensaje_por_id
from src.database.queries import cargar_contexto_base_ordenado

# Dejamos la API limpia lista para usar
__all__ = [
    "inicializar_db",
    "obtener_o_crear_sesion",
    "finalizar_y_consolidar_sesion",
    "obtener_proyectos_unicos",
    "guardar_mensaje_en_vivo",
    "obtener_mensaje_por_id",
    "cargar_contexto_base_ordenado",
]
