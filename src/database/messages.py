# src/database/messages.py
from datetime import datetime
from src.database.connection import conectar

def guardar_mensaje_en_vivo(sesion_id, rol, contenido):
    """Inserta de inmediato cada mensaje del chat (L4) para blindar los datos."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO nivel4_mensajes (sesion_id, rol, contenido, timestamp)
            VALUES (?, ?, ?, ?)
        """, (sesion_id, rol, contenido, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()

def obtener_mensaje_por_id(mensaje_id):
    """Busca quirúrgicamente un texto en el historial crudo (Comando :cite)."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT rol, contenido FROM nivel4_mensajes WHERE id = ?", (mensaje_id,))
        row = cursor.fetchone()
        return {"role": row[0], "content": row[1]} if row else None
