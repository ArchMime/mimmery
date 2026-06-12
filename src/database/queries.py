# src/database/queries.py
from src.database.connection import conectar
from src.config import LIMITE_N1, LIMITE_N2, LIMITE_N3

def cargar_contexto_base_ordenado(proyecto, sesion_id_actual):
    """Compila el prompt maestro con límites estrictos de bajo consumo."""
    with conectar() as conn:
        cursor = conn.cursor()
        es_global = proyecto.lower() == "global"
        
        # --- NIVEL 1 ---
        if es_global:
            cursor.execute("SELECT n1.timestamp, s.proyecto, n1.commit_texto FROM nivel1_commits n1 JOIN sesiones s ON n1.sesion_id = s.id ORDER BY n1.id DESC LIMIT ?", (LIMITE_N1,))
        else:
            cursor.execute("SELECT n1.timestamp, s.proyecto, n1.commit_texto FROM nivel1_commits n1 JOIN sesiones s ON n1.sesion_id = s.id WHERE s.proyecto = ? ORDER BY n1.id DESC LIMIT ?", (proyecto, LIMITE_N1))
        n1_filas = cursor.fetchall()[::-1]
        n1_texto = "\n".join([f"[{f[0]}] ({f[1]}): {f[2]}" for f in n1_filas])

        # --- NIVEL 2 ---
        if es_global:
            cursor.execute("SELECT resumen_tecnico FROM nivel2_resumenes ORDER BY id DESC LIMIT ?", (LIMITE_N2,))
        else:
            cursor.execute("SELECT n2.resumen_tecnico FROM nivel2_resumenes n2 JOIN sesiones s ON n2.sesion_id = s.id WHERE s.proyecto = ? ORDER BY n2.id DESC LIMIT ?", (proyecto, LIMITE_N2))
        n2_texto = "\n---\n".join([f[0] for f in cursor.fetchall()[::-1]])

        # --- NIVEL 3 ---
        if es_global:
            cursor.execute("SELECT pregunta, respuesta FROM nivel3_qna ORDER BY id DESC LIMIT ?", (LIMITE_N3,))
        else:
            cursor.execute("SELECT n3.pregunta, n3.respuesta FROM nivel3_qna n3 JOIN sesiones s ON n3.sesion_id = s.id WHERE s.proyecto = ? ORDER BY n3.id DESC LIMIT ?", (proyecto, LIMITE_N3))
        n3_texto = "\n---\n".join([f"Q: {f[0]}\nA: {f[1]}" for f in cursor.fetchall()[::-1]])

        # --- NIVEL 4 ---
        cursor.execute("SELECT rol, contenido FROM nivel4_mensajes WHERE sesion_id = ? ORDER BY id DESC LIMIT 6", (sesion_id_actual,))
        n4_filas = cursor.fetchall()[::-1]
        n4_historial_lista = [{"role": row[0], "content": row[1]} for row in n4_filas]

        # --- ENSAMBLADO ---
        contexto_string = "=== MEMORIA HIERÁRQUICA DEL ENTORNO ===\n\n"
        contexto_string += f"ÍNDICE RECIENTE DE HITOS (Nivel 1):\n{n1_texto if n1_texto else 'Sin registros.'}\n\n"
        contexto_string += f"ÚLTIMAS DECISIONES ARQUITECTÓNICAS (Nivel 2):\n{n2_texto if n2_texto else 'Sin registros.'}\n\n"
        contexto_string += f"SOLUCIONES TÉCNICAS PREVIAS (Nivel 3):\n{n3_texto if n3_texto else 'Sin registros.'}\n"
        contexto_string += "=======================================\n"
        
        return contexto_string, n4_historial_lista
