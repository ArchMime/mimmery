# auditar_db.py
import sqlite3
import os
from src.config import DB_PATH

def auditar_completo():
    if not os.path.exists(DB_PATH):
        print(f"[!] No se encontró el archivo de base de datos en: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("               🔍 REPORTE DE INTEGRIDAD RELACIONAL DE LA BASE DE DATOS              ")
    print("="*80)

    # 1. LEER TABLA SESIONES
    print("\n[TABLA: sesiones]")
    cursor.execute("SELECT id, proyecto, fecha_inicio, fecha_fin, estado FROM sesiones")
    sesiones = cursor.fetchall()
    if not sesiones:
        print("  (Vacía)")
    for s in sesiones:
        print(f"  ▪️ ID: {s[0]} | Proyecto: {s[1].upper()} | Inicio: {s[2]} | Fin: {s[3]} | Estado: {s[4].upper()}")

    # 2. LEER TABLA NIVEL 1 (COMMITS)
    print("\n" + "-"*80)
    print("[TABLA: nivel1_commits (Índices Históricos L1)]")
    cursor.execute("SELECT id, sesion_id, commit_texto, timestamp FROM nivel1_commits")
    commits = cursor.fetchall()
    if not commits:
        print("  (Vacía)")
    for c in commits:
        print(f"  ▪️ ID: {c[0]} [Sesión FK: {c[1]}] ({c[3]})\n      ↳ \"{c[2]}\"")

    # 3. LEER TABLA NIVEL 2 (RESÚMENES)
    print("\n" + "-"*80)
    print("[TABLA: nivel2_resumenes (Decisiones Arquitectónicas L2)]")
    cursor.execute("SELECT id, sesion_id, resumen_tecnico, timestamp FROM nivel2_resumenes")
    resumenes = cursor.fetchall()
    if not resumenes:
        print("  (Vacía)")
    for r in resumenes:
        print(f"  ▪️ ID: {r[0]} [Sesión FK: {r[1]}] ({r[3]})\n{r[2]}")

    # 4. LEER TABLA NIVEL 3 (Q&A SANEADO)
    print("\n" + "-"*80)
    print("[TABLA: nivel3_qna (Diccionario Técnico L3)]")
    cursor.execute("SELECT id, sesion_id, pregunta, respuesta, timestamp FROM nivel3_qna")
    qnas = cursor.fetchall()
    if not qnas:
        print("  (Vacía)")
    for q in qnas:
        print(f"  ▪️ ID: {q[0]} [Sesión FK: {q[1]}] ({q[4]})")
        print(f"      ❓ Pregunta:  {q[2]}")
        print(f"      💡 Respuesta: {q[3]}")
        print("      " + "."*40)

    # 5. LEER TABLA NIVEL 4 (MENSAJES EN VIVO)
    print("\n" + "-"*80)
    print("[TABLA: nivel4_mensajes (Chat Crudo Completo L4)]")
    cursor.execute("SELECT id, sesion_id, rol, contenido, es_importante, timestamp FROM nivel4_mensajes")
    mensajes = cursor.fetchall()
    if not mensajes:
        print("  (Vacía)")
    for m in mensajes:
        pin = "📌" if m[4] == 1 else "  "
        print(f"  ▪️ ID: {m[0]:03d} [Sesión FK: {m[1]}] {pin} [{m[2].upper()}]: {m[3][:100]}...")

    print("\n" + "="*80)
    print("               🏁 FIN DEL REPORTE DE PERSISTENCIA JERÁRQUICA               ")
    print("="*80 + "\n")
    
    conn.close()

if __name__ == "__main__":
    auditar_completo()
