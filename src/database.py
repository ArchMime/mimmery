# src/database.py
import sqlite3
import json
import os
from src.config import DB_PATH

def conectar():
    # Asegura que la carpeta data/ exista físicamente
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def inicializar_db():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sesiones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                etiqueta TEXT NOT NULL,
                nivel1_commit TEXT NOT NULL,
                nivel2_resumen TEXT NOT NULL,
                nivel3_crudo TEXT NOT NULL
            )
        """)
        conn.commit()

def obtener_proyectos_unicos():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT etiqueta FROM sesiones ORDER BY etiqueta ASC")
        return [row[0] for row in cursor.fetchall()]

def cargar_contexto_dinamico(proyecto, limite_n2, limite_n3):
    inicializar_db()
    with conectar() as conn:
        cursor = conn.cursor()
        
        # Modo Global vs Modo Proyecto
        if proyecto.lower() == "global":
            query_n1 = "SELECT fecha, etiqueta, nivel1_commit FROM sesiones ORDER BY fecha ASC"
            query_n2 = "SELECT nivel2_resumen FROM sesiones ORDER BY fecha DESC LIMIT ?"
            query_n3 = "SELECT nivel3_crudo FROM sesiones ORDER BY fecha DESC LIMIT ?"
            params_n1, params_n2, params_n3 = (), (limite_n2,), (limite_n3,)
        else:
            query_n1 = "SELECT fecha, etiqueta, nivel1_commit FROM sesiones WHERE etiqueta = ? ORDER BY fecha ASC"
            query_n2 = "SELECT nivel2_resumen FROM sesiones WHERE etiqueta = ? ORDER BY fecha DESC LIMIT ?"
            query_n3 = "SELECT nivel3_crudo FROM sesiones WHERE etiqueta = ? ORDER BY fecha DESC LIMIT ?"
            params_n1, params_n2, params_n3 = (proyecto,), (proyecto, limite_n2), (proyecto, limite_n3)

        # 1. Cargar Nivel 1 (Índice completo de commits)
        cursor.execute(query_n1, params_n1)
        n1_filas = cursor.fetchall()
        n1_texto = "\n".join([f"[{f[0]}] ({f[1]}): {f[2]}" for f in n1_filas])

        # 2. Cargar Nivel 2 (Resúmenes técnicos)
        cursor.execute(query_n2, params_n2)
        n2_texto = "\n---\n".join([f[0] for f in cursor.fetchall()])

        # 3. Cargar Nivel 3 (Mensajes crudos decodificados de JSON)
        cursor.execute(query_n3, params_n3)
        n3_texto = ""
        for fila in cursor.fetchall():
            mensajes = json.loads(fila[0])
            for msg in mensajes:
                n3_texto += f"{msg['role'].upper()}: {msg['content']}\n"
            n3_texto += "---\n"

        # Compilación estructurada del contexto inyectado
        contexto = "=== MEMORIA HISTÓRICA DEL ENTORNO ===\n\n"
        contexto += f"ÍNDICE COMPLETO DE SESIONES (Nivel 1):\n{n1_texto if n1_texto else 'Sin registros.'}\n\n"
        contexto += f"ÚLTIMOS {limite_n2} RESÚMENES TÉCNICOS (Nivel 2):\n{n2_texto if n2_texto else 'Sin registros.'}\n\n"
        contexto += f"ÚLTIMAS {limite_n3} CONVERSACIONES EN CRUDO (Nivel 3):\n{n3_texto if n3_texto else 'Sin registros.'}\n"
        contexto += "=====================================\n"
        return contexto

def guardar_sesion(proyecto, commit, resumen, historial_lista):
    from datetime import datetime
    with conectar() as conn:
        cursor = conn.cursor()
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        historial_json = json.dumps(historial_lista)
        cursor.execute("""
            INSERT INTO sesiones (fecha, etiqueta, nivel1_commit, nivel2_resumen, nivel3_crudo)
            VALUES (?, ?, ?, ?, ?)
        """, (fecha_actual, proyecto, commit, resumen, historial_json))
        conn.commit()
