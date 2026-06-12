# src/database/connection.py
import sqlite3
import os
from src.config import DB_PATH

def conectar():
    """Garantiza la existencia del directorio y conecta a SQLite."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def inicializar_db():
    """Crea el modelo relacional robusto con tablas normalizadas por nivel."""
    with conectar() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sesiones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proyecto TEXT NOT NULL,
                fecha_inicio TEXT NOT NULL,
                fecha_fin TEXT,
                estado TEXT NOT NULL CHECK(estado IN ('activa', 'consolidada'))
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nivel1_commits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sesion_id INTEGER NOT NULL,
                commit_texto TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (sesion_id) REFERENCES sesiones(id) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nivel2_resumenes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sesion_id INTEGER NOT NULL,
                resumen_tecnico TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (sesion_id) REFERENCES sesiones(id) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nivel3_qna (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sesion_id INTEGER NOT NULL,
                pregunta TEXT NOT NULL,
                respuesta TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (sesion_id) REFERENCES sesiones(id) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nivel4_mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sesion_id INTEGER NOT NULL,
                rol TEXT NOT NULL CHECK(rol IN ('user', 'assistant')),
                contenido TEXT NOT NULL,
                es_importante INTEGER DEFAULT 0 CHECK(es_importante IN (0, 1)),
                timestamp TEXT NOT NULL,
                FOREIGN KEY (sesion_id) REFERENCES sesiones(id) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS flags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS qna_flags (
                qna_id INTEGER NOT NULL,
                flag_id INTEGER NOT NULL,
                PRIMARY KEY (qna_id, flag_id),
                FOREIGN KEY (qna_id) REFERENCES nivel3_qna(id) ON DELETE CASCADE,
                FOREIGN KEY (flag_id) REFERENCES flags(id) ON DELETE CASCADE
            )
        """)
        conn.commit()
