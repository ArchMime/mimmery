# src/database/sessions.py
from datetime import datetime
from src.database.connection import conectar, inicializar_db

def obtener_o_crear_sesion(proyecto):
    """Busca sesiones activas previas o inicializa una nueva."""
    inicializar_db()
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM sesiones 
            WHERE proyecto = ? AND estado = 'activa' 
            LIMIT 1
        """, (proyecto,))
        fila = cursor.fetchone()
        
        if fila:
            return fila[0], True
            
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO sesiones (proyecto, fecha_inicio, estado)
            VALUES (?, ?, 'activa')
        """, (proyecto, fecha_actual))
        conn.commit()
        return cursor.lastrowid, False

# Modificar esta función dentro de: src/database/sessions.py

def finalizar_y_consolidar_sesion(sesion_id, commit, resumen):
    """Cierra la sesión guardando los niveles de largo plazo L1 y L2 (L3 ya se guardó en vivo)."""
    from datetime import datetime
    from src.database.connection import conectar
    
    with conectar() as conn:
        cursor = conn.cursor()
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
            UPDATE sesiones 
            SET fecha_fin = ?, estado = 'consolidada' 
            WHERE id = ?
        """, (fecha_actual, sesion_id))
        
        cursor.execute("""
            INSERT INTO nivel2_resumenes (sesion_id, resumen_tecnico, timestamp) 
            VALUES (?, ?, ?)
        """, (sesion_id, resumen, fecha_actual))
        
        cursor.execute("""
            INSERT INTO nivel1_commits (sesion_id, commit_texto, timestamp) 
            VALUES (?, ?, ?)
        """, (sesion_id, commit, fecha_actual))
        
        conn.commit()


def obtener_proyectos_unicos():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT proyecto FROM sesiones ORDER BY proyecto ASC")
        return [row[0] for row in cursor.fetchall()]
